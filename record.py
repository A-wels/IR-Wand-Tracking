from time import sleep
import cv2
import numpy as np

cam = cv2.VideoCapture("http://192.168.178.40:8080/?action=stream")
index = 0

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
    if(index%3==0):
        cv2.imwrite("./train/file"+(str(index)+".png"),canvas)
    index+=1
