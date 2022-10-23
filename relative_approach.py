from typing import List, Tuple

import cv2
from cv2 import trace
import numpy as np
import time
from config import *
from modules.actions import toggle_hexalight
from util import recognize_gesture, show_trace, show_tracepoints
from modules.motor import trigger_motor
#cam = cv2.VideoCapture("http://192.168.178.40:8080/?action=stream")
cam = cv2.VideoCapture(0)


bg_buffer = []
recalc_bg = 10
MAX_TRACEPOINTS = 10
background = None
gray_sub = None
last_time = None
tracepoints:List[Tuple] = []
MAX_SPEED = 20
shape = None
TARGET_FPS = 10

directions: List[Tuple] = []

check, frame = cam.read()
while not check:
    print(check)
    check,frame = cam.read()
shape = frame.shape




def get_background(frames:List) -> np.ndarray:
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
    if len(bg_buffer) > recalc_bg:
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
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(gray)

    # Update the list of tracepoints
    print(maxVal)
    if(maxVal > 130):
     tracepoints.append(maxLoc)
     if(len(tracepoints) > MAX_TRACEPOINTS):
        tracepoints.pop(0)
    elif len(tracepoints) > 0:
        tracepoints.pop(0)

    if VERBOSE_OUTPUT:
        show_tracepoints(frame, tracepoints)
  #  cv2.imshow('blur', blur)
    if VERBOSE_OUTPUT:
        
        cv2.imshow('video', frame)

    key = cv2.waitKey(1)
 
  #  tracepoints_array = np.array((tracepoints.pt[0], tracepoints.pt[1]), np.int32)
   
    if VERBOSE_OUTPUT:
       show_trace(gray, tracepoints)

    # recognize a gesture
    gesture =  recognize_gesture(tracepoints.copy())

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
