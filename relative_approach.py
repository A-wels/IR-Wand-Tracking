from typing import List, Tuple

import cv2
from cv2 import trace
import numpy as np
import time
from config import *
from modules.actions import toggle_hexalight
from util import calculate_distance_sum, recognize_gesture, show_trace, show_tracepoints
from modules.motor import trigger_motor
#cam = cv2.VideoCapture("http://192.168.178.40:8080/?action=stream")
cam = cv2.VideoCapture(0)


bg_buffer = []
recalc_bg = 10
background = None
gray_sub = None
last_time = None
tracepoints:List[Tuple] = []
MAX_SPEED = 20
shape = None
TARGET_FPS = 10
# keep four points: hold still at the beginning of the gesture
last_four = []
START_TIME = 0
directions: List[Tuple] = []

hexalight_on = False
CURRENT_ITERATIONS = 999
check, frame = cam.read()
while not check:
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

    #print("maxval: " + str(maxVal))
    # check if the wand was held still
    if CURRENT_ITERATIONS > ITERATIONS_AFTER_START:
        distance_of_last_positions = calculate_distance_sum(last_four)

    # Update the list of tracepoints
    if(maxVal > LAST_FOUR_THRESHOLD):
        last_four.append(maxLoc)

    if(maxVal > MAXVAL_THRESHOLD):
        if(distance_of_last_positions < START_DISTANCE_MOVEMENT):
          if not hexalight_on:
            toggle_hexalight()
            hexalight_on = True
            CURRENT_ITERATIONS = 0

          tracepoints.append(maxLoc)
        if(len(tracepoints) > MAX_TRACEPOINTS):
            tracepoints.pop(0)
        if(len(last_four) > 4):
            last_four.pop(0)
    else:
        if len(tracepoints) > 0:
            tracepoints.pop(0)
        if len(last_four) > 0:
            last_four.pop()
    
        

    if VERBOSE_OUTPUT:
        show_tracepoints(frame, tracepoints)
  #  cv2.imshow('blur', blur)
    if VERBOSE_OUTPUT:
        
        cv2.imshow('video', frame)

   # key = cv2.waitKey(1)
 
  #  tracepoints_array = np.array((tracepoints.pt[0], tracepoints.pt[1]), np.int32)
   
    if VERBOSE_OUTPUT:
       show_trace(gray, tracepoints)

    # recognize a gesture if the wand was held still for a while
    if CURRENT_ITERATIONS <= ITERATIONS_AFTER_START:
        gesture =  recognize_gesture(tracepoints.copy())

        if gesture.name == "ONE":
            trigger_motor()
            toggle_hexalight()
            hexalight_on = False
            CURRENT_ITERATIONS = 998
            tracepoints = []
            directions = []
        CURRENT_ITERATIONS += 1

    else:

        if hexalight_on:
            toggle_hexalight()
            hexalight_on = False


  #  if key == 27:
  #      break

cam.release()
cv2.destroyAllWindows() 
