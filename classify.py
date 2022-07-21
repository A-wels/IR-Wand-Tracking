from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
import numpy as np
import os
from keras.models import load_model
import cv2
import numpy as np
import os
from datetime import datetime
from math import dist
import time
from actions import toggle_hexalight

cam = cv2.VideoCapture("http://192.168.178.40:8080/?action=stream")

model = load_model('model_saved.h5')

BACKGROUND_PATH = "./results/background_images"

bg_buffer = []
recalc_bg = 50
MAX_TRACEPOINTS = 20
background = None
gray_sub = None
last_time = 0
tracepoints = []
interval_drop_tp = 2
index_drop = 0
MAX_SPEED = 20
last_spells = []
cooldown = False

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
        gray = gray-background
        cv2.imshow('substracted', gray)
    else:
        continue
    
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    if(maxVal > 130):
     tracepoints.append(maxLoc)
     if(len(tracepoints) > MAX_TRACEPOINTS):
        tracepoints.pop(0)
    elif(len(tracepoints) > 1):
        tracepoints.pop(0)

    if len(tracepoints) > 1:
        #cv2.polylines(image, np.array(tracepoints), False, (0,255,0))
        for t in tracepoints:
                cv2.circle(frame, (int(t[0]), int(t[1])),5, (255, 0, 0), 2)

   
  #  cv2.imshow('blur', blur)
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    canvas = np.zeros(gray.shape, dtype=np.uint8)
    canvas.fill(255)
  #  tracepoints_array = np.array((tracepoints.pt[0], tracepoints.pt[1]), np.int32)
    if(len(tracepoints) > 1):
        line_index = 0
        for p in tracepoints[1:]:
            canvas = cv2.line(canvas, (int(tracepoints[line_index][0]),int(tracepoints[line_index][1])), (int(p[0]),int(p[1])), (0,0,0))
            line_index +=1
           # canvas = cv2.polylines(canvas, [tracepoints_array], False, (0,0,0), 1)
    cv2.imshow("white",canvas)


    canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2RGB)
    img = np.array(canvas)
    img = img / 255.0
    img = img.reshape(1,320,240,3)
    label = model.predict(img)
   # print(label[0][0])
    if(len(last_spells) > 10):
     last_spells.pop(0)
    if(label[0][0] <  3.5310984e-07):
        print("CIRCLE ")#+ str(label[0][0]))
        last_spells.append("CIRCLE")
        print(last_spells)
        print(cooldown)
        if(last_spells.count("CIRCLE") > 3 and not cooldown):
            toggle_hexalight()
            cooldown = True
        elif(last_spells.count("") > 9):
            cooldown = False
            
    else:
        last_spells.append("")



    if key == 27:
        break

cam.release()
cv2.destroyAllWindows() 

 

