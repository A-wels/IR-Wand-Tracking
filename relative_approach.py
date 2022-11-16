from typing import List, Tuple

import cv2
import numpy as np
import time
from config import *
from modules.actions import toggle_hexalight
from util import recognize_gesture, show_trace, show_tracepoints
from modules.motor import trigger_motor


cam = cv2.VideoCapture(0)


bg_buffer = []
background = None
last_time = None
tracepoints:List[Tuple] = []
shape = None
directions: List[Tuple] = []



# read a new frame in order to get the shape of frames
check, frame = cam.read()
while not check:
    check,frame = cam.read()
shape = frame.shape

# get the minimum value for all pixels in the background list
def get_background(frames: List) -> np.ndarray:
    background = np.min(frames, axis=0).astype(dtype=np.uint8)
    return background



while True:

    # maintain a steady framerate by delaying 
    time1 = time.time()
    if last_time is not None:
        last_exec_time = time1 - last_time
        if(last_exec_time < 1/TARGET_FPS):
            sleeptime = 1/TARGET_FPS - last_exec_time
            time.sleep(sleeptime)
    last_time = time1

    check, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    # background substraction
    bg_buffer.append(gray)
    if len(bg_buffer) > RECALC_BG:
        bg_buffer.pop(0)
        background = get_background(bg_buffer)
        if VERBOSE_OUTPUT:
            cv2.imshow("bg", background)  

    if background is not None:
        gray = gray-background
        if VERBOSE_OUTPUT:
            cv2.imshow('substracted', gray)
    else:
        continue

    # blur the image and locate max
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(gray)

    # Update the list of tracepoints
    if(maxVal > MAXVAL_THRESHOLD):
        tracepoints.append(maxLoc)
        if(len(tracepoints) > MAX_TRACEPOINTS):
            tracepoints.pop(0)

    else:
        if len(tracepoints) > 0:
            tracepoints.pop(0)

        

    if VERBOSE_OUTPUT:
        show_tracepoints(frame, tracepoints)
        cv2.imshow('video', frame)
        show_trace(gray, tracepoints)
        key = cv2.waitKey(1)

    # recognize a gesture if the wand was held still for a while
    gesture =  recognize_gesture(tracepoints.copy())

    # match the gesture name and act accordingly
    if gesture.name == "ONE":
        toggle_hexalight()
        trigger_motor()
        toggle_hexalight()
        tracepoints = []
        directions = []


    if key == 27:
        break

cam.release()
cv2.destroyAllWindows() 
