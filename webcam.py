import cv2
import numpy as np
import os
from datetime import datetime
from math import dist

cam = cv2.VideoCapture("http://192.168.178.40:8080/?action=stream")


BACKGROUND_PATH = "./results/background_images"

bg_buffer = []
recalc_bg = 50
background = None
gray_sub = None
last_time = 0
tracepoints = []

MAX_SPEED = 150
def get_background(frames):
   # list_of_grayscale_images = []
   # for f in frames:
   #     list_of_grayscale_images.append( cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))

    background = np.min(frames, axis=0).astype(dtype=np.uint8)
    return background



while True:
    check, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    """
    bg_buffer.append(gray)
    if len(bg_buffer) > recalc_bg:
        bg_buffer.pop(0)
        background = get_background(bg_buffer)
        cv2.imshow("bg", background)    
    if background is not None:
        gray_sub = gray-background
    else:
        gray_sub = gray


    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 150
    params.maxThreshold = 255

    params.filterByColor = True
    params.blobColor = 255


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 150

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.4

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.4

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)


    # Detect blobs.
    keypoints = detector.detect(gray_sub)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob

    #frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if len(keypoints) > 1:
        current_time = datetime.now()
        if len(tracepoints) > 1:
            elapsed = current_time - last_time
            p1 = (int(tracepoints[-1].pt[0]), int(tracepoints[-1].pt[1]))
            p2 = (int(tracepoints[-2].pt[0]), int(tracepoints[-2].pt[1]))

            distance = dist(p1, p2)
            if(distance / elapsed.total_seconds() >= MAX_SPEED):
                print("too fast")

            if(len(tracepoints) > recalc_bg):
                tracepoints.pop(0)
            tracepoints.append(keypoints[0])
        else:
            last_time = current_time
            tracepoints.append(keypoints[0])

    #frame = cv2.drawKeypoints(frame, tracepoints, frame)
"""


    blur = cv2.GaussianBlur(gray, (15,15), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    image = frame.copy()
    cv2.circle(image, maxLoc,5, (255, 0, 0), 2)
    tracepoints.append(maxLoc)
    if(len(tracepoints) > recalc_bg):
        tracepoints.pop(0)
    if len(tracepoints) > 1:
        #cv2.polylines(image, np.array(tracepoints), False, (0,255,0))
        for t in tracepoints:
                cv2.circle(image, t,5, (255, 0, 0), 2)

   
    cv2.imshow('video', image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows() 
