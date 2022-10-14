import cv2
from cv2 import trace
import numpy as np
from typing import List, Tuple
from gestures import Gesture
import math
from config import *
import requests

def toggle_hexalight():
    url = "http://192.168.178.101:8123/api/webhook/wled-wz"
    x = requests.post(url)
    print("Hexalight toggle")

# Calculate atan2 from the difference between the two points. Result is used as a 'direction'
def get_direction(old: Tuple, new: Tuple) -> Tuple[float, float]:
    distance = math.dist(old, new)
    theta = math.atan2(new[0]-old[0],new[1]-old[1])
  #  if VERBOSE_OUTPUT:
  #      print("Distance " + str(distance))
  #      print("Theta " + str(theta))
  #      print("\n")
    return theta, distance

# draw the tracepoints into a framea
def show_tracepoints(frame: np.ndarray, tracepoints: List[Tuple]) -> None:
    if len(tracepoints) > 1:
          for t in tracepoints:
                cv2.circle(frame, (int(t[0]), int(t[1])),5, (255, 0, 0), 2)

# draw the trace on a white canvas
def show_trace(frame: np.ndarray, tracepoints: List[Tuple]) -> None:
    canvas = np.zeros(frame.shape, dtype=np.uint8)
    canvas.fill(255)
    if(len(tracepoints) > 1):

        line_index = 0
        for index, p in enumerate(tracepoints[1:]):
            canvas = cv2.line(canvas, (int(tracepoints[line_index][0]),int(tracepoints[line_index][1])), (int(p[0]),int(p[1])), (0,0,0))
            line_index +=1
           # canvas = cv2.polylines(canvas, [tracepoints_array], False, (0,0,0), 1)
   
    cv2.imshow("white",canvas)

# take a list of recognized points and select a fitting gesture
def recognize_gesture(tracepoints: List[Tuple]) -> Gesture:
    if(len(tracepoints) > 3):
        
        # while the angle of movement does not harshly change, keep going
        direction = get_direction(tracepoints[0], tracepoints[1])
        last_theta = direction [0]
        new_theta = last_theta
        distance_sum = direction[1]
        last_distance = direction[1]
        tracepoints.pop(0)
        thetas = []

        directions = []
        if(last_distance > 4 and len(tracepoints) > 3):
            while len(tracepoints) > 2:
                new_dir = True
                while(len(tracepoints) > 2 and new_theta >= last_theta - THETA_ALLOWED_VARIANCE and new_theta <= last_theta + THETA_ALLOWED_VARIANCE or new_dir):
                    new_dir = False
                    thetas.append(new_theta)
                    direction = get_direction(tracepoints[0], tracepoints[1])
                    last_distance = direction[1]
                    if(last_distance > 4):
                        distance_sum += direction[1]
                        last_theta = new_theta
                        new_theta = abs(direction[0])
                       # print(new_theta)
                    tracepoints.pop(0)
                # if the direction was change, save the current averages and save them. Remove the next entry to account for inaccuracies in tracking
                if len(tracepoints) > 2:    
                    directions.append((np.average(thetas), distance_sum))
                    thetas = []
                    distance_sum = 0
                    tracepoints.pop(0)
                    direction = get_direction(tracepoints[0], tracepoints[1])
                    new_theta = abs(direction[0])
                    new_dir = True

                    # print("CHANGE IN DIRECTION: " + str(last_theta) + " to " + str(new_theta))

     #   print(directions)

        # match to gesture
        possible = True
        for g in Gesture:
            if(g.name != Gesture.NO_GESTURE_RECOGNIZED.name and len(g.value) == len(directions)):
                for index, d in enumerate(directions):
                    theta_diff = g.value[index][0] - d[0]
                    print("theta diff:  "+ str(theta_diff))
                    if(abs(theta_diff)) > GESTURE_THRESHOLD:
                        possible = False
                        break
                print("\n")
                if possible:
                    print("GESTURE DETECTED: " + g.name)
                    return g
    return Gesture.NO_GESTURE_RECOGNIZED
                

            

