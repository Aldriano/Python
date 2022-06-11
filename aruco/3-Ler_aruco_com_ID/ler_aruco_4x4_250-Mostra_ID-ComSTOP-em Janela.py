import cv2
from cv2 import aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters_create()

capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
    out = aruco.drawDetectedMarkers(frame, corners, ids)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print("ids= ",ids)
    if ids is not None:
        cv2.imshow('ID Detected' + format(ids[0]), frame)
capture.release()
cv2.destroyAllWindows()



