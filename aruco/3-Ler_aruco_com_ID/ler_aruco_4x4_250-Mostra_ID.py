# Import required packages
import cv2
from cv2 import aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters_create()

# Create video capture object 'capture' to be used to capture frames from the first 
# connected camera:
capture = cv2.VideoCapture(0)

while True:
    # Capture frame by frame from the video capture object 'capture':
    ret, frame = capture.read()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame,aruco_dict,parameters=parameters)

    out = aruco.drawDetectedMarkers(frame, corners, ids)

    print("ids= ",ids)

    cv2.imshow('frame', frame)  # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release everything:
capture.release()
cv2.destroyAllWindows()

