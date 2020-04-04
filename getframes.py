# -*- coding: utf-8 -*-


import cv2
import os



if not os.path.exists('images_A'):
    os.makedirs('images_A')
    
vidcap = cv2.VideoCapture('ev_20200217_090037A_10A.avi')
success,image = vidcap.read()
count = 0

while success:
  cv2.imwrite(os.path.join('images_A', '20200201_A_frame%d.tiff') % count, image)   
  success,image = vidcap.read()
  print ('Read a new frame: ', success)
  count += 1
  

close = cv2.VideoCapture.release('ev_20200201_081406A_05A.avi')