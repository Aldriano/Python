import cv2
import socket
import time
import threading
from cv2 import aruco
import numpy as np
import os

def receiveData():
    global response
    while True:
        try:
            response, _ = clientSocket.recvfrom(1024)
        except:
            break


def readStates():
    global battery
    while True:
        try:
            response_state, _ = stateSocket.recvfrom(256)
            if response_state != 'ok':
                response_state = response_state.decode('ASCII')
                list = response_state.replace(';', ':').split(':')
                battery = int(list[21])
        except:
            break


def sendCommand(command):
    global response
    timestamp = int(time.time() * 1000)

    clientSocket.sendto(command.encode('utf-8'), address)

    while response is None:
        if (time.time() * 1000) - timestamp > 5 * 1000:
            return False

    return response


def sendReadCommand(command):
    response = sendCommand(command)
    try:
        response = str(response)
    except:
        pass
    return response


def sendControlCommand(command):
    response = None
    for i in range(0, 5):
        response = sendCommand(command)
        if response == 'OK' or response == 'ok':
            return True
    return False

def loudAugImages(path):

    myList = os.listdir(path)
    noOfMarkers = len(myList)
    print(noOfMarkers)
    augDics = {}
    for imgPath in myList:
        key = int(os.path.splitext(imgPath)[0])
        imgAug = cv2.imread(f'{path}/{imgPath}')
        augDics[key] = imgAug
    return augDics

def findArucoMakers(img, markersize= 4, totalMarkers= 50, draw=True):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markersize}X{markersize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

    #print(ids)

    if draw:
        aruco.drawDetectedMarkers(img, bbox)

    return [bbox, ids]

def arucoAug(bbox, id, img, imgAug, drawId=True):

    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]

    h, w, c = imgAug.shape

    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
    cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    imgOut = img + imgOut

    if drawId:
        cv2.putText(imgOut, str(id), (int(tl[0]), int(tl[1])), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    return imgOut

# ———————————————–
# Main program
# ———————————————–

# connection info
UDP_IP = '192.168.10.1'
UDP_PORT = 8889
last_received_command = time.time()
STATE_UDP_PORT = 8890

address = (UDP_IP, UDP_PORT)
response = None
response_state = None

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind(('', UDP_PORT))
stateSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stateSocket.bind(('', STATE_UDP_PORT))

# start threads
recThread = threading.Thread(target=receiveData)
recThread.daemon = True
recThread.start()

stateThread = threading.Thread(target=readStates)
stateThread.daemon = True
stateThread.start()

# connect to drone
response = sendControlCommand("command")
print(f'command response: {response}')
response = sendControlCommand("streamon")
print(f'streamon response: {response}')

# drone information
battery = 0

# open UDP
print(f'opening UDP video feed, wait 2 seconds ')
videoUDP = 'udp://192.168.10.1:11111'
cap = cv2.VideoCapture(videoUDP)
time.sleep(2)
augDics = loudAugImages("img")

# open
i = 0
while True:
    i = i + 1
    start_time = time.time()

    try:
        secrets, img = cap.read()
        arucoFound = findArucoMakers(img)

        if len(arucoFound[0]) != 0:
            for bbox, id in zip(arucoFound[0], arucoFound[1]):
                if int(id) in augDics.keys():
                    img = arucoAug(bbox, id, img, augDics[int(id)])

        cv2.imshow("Img", img)

        sendReadCommand('battery?')
        #print(f'battery: {battery} % – i: {i} – {fpsInfo}')

    except Exception as e:
        print(f'exc: {e}')
        pass

    k = cv2.waitKey(1) % 256
    if k == 27:  # Esc key to stop
        break
    elif k == ord('u'):
        sendControlCommand("command")
        sendControlCommand("takeoff")
        sendControlCommand("command")
        response = sendControlCommand("streamon")
        print('you press %s' % chr(k))
    elif k == ord('d'):
        sendControlCommand("command")
        sendControlCommand("land")
        sendControlCommand("command")
        response = sendControlCommand("streamon")
    elif k == -1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k)  # else print its value

response = sendControlCommand("streamoff")
print(f'streamon response: {response}')
