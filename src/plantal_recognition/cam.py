'''
Created on Jul 6, 2021

@author: yann
https://subscription.packtpub.com/book/application_development/9781785283932/3/ch03lvl1sec28/accessing-the-webcam
'''

import cv2

data_path = '../data/'
screenshot_path = data_path+'screenshot.png'
font = cv2.FONT_HERSHEY_SIMPLEX

def screenshot(frame, save=False):
    cv2.imshow("screenshot", frame) # shows the screenshot directly
    if save :
        save_frame(frame)
        
def draw_label(frame, face, label, save=False, color=(0, 255, 0)):
    offset = 30
    size = 0.7
    
    x, y, _, h = face
    y += offset + h
    
    cv2.putText(frame, label, (x, y), font, size, color, 2)
    if save:
        save_frame(frame)
    return frame

def save_frame(frame, path=None):
    if not path :
        cv2.imwrite(screenshot_path, frame) # or saves it to disk
    else:
        cv2.imwrite(path, frame) # or saves it to disk

def save_frames(frames, name):
    for idx, frame in enumerate(frames):
        save_frame(frame, name+str(idx)+".png") 
        
        
        
        
        