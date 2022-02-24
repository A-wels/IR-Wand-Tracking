import cv2
import numpy as np
import os


cam = cv2.VideoCapture("http://192.168.178.40:8080/?action=stream")


BACKGROUND_PATH = "./results/background_images"

bg_buffer = []
recalc_bg = 50
background = None
gray_sub = None

def get_background(frames):
   # list_of_grayscale_images = []
   # for f in frames:
   #     list_of_grayscale_images.append( cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))

    background = np.min(frames, axis=0).astype(dtype=np.uint8)
    return background



while True:
    check, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
    params.minArea = 0.05
    params.maxArea = 200

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

    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15,15), 0)
    

    
    (T, gray) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    filteredContours = []
    for c in contours:
        if cv2.contourArea(c) > 50 and cv2.contourArea(c) < 200:
            filteredContours.append(c)
            print("Contour Found")
    gray = cv2.drawContours(gray, filteredContours, -1, (0, 255, 0), 3)    
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    cv2.circle(gray, maxLoc, 41, (255, 0, 0), 2)    


    """
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows() 
