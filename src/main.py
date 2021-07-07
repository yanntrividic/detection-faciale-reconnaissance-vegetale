'''
Created on Jul 6, 2021

@author: yann
'''

import cv2
from plantal_recognition.facedetect import load_model, detect_faces
from plantal_recognition.cam import screenshot
from plantal_recognition.face import analyze_faces

if __name__ == '__main__':
    
    faceCascade = load_model()
    
    video_capture = cv2.VideoCapture(0)
    faces_objects = None
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
    
        _, faces = detect_faces(frame, faceCascade)
        # print(ret)
        # Display the resulting frame
    
        ch = cv2.waitKey(5)
        
        if ch == 27:
            break

        faces_objects = analyze_faces(frame, faces_objects, faces)
        
        if ch == ord('c'): # calls screenshot function when 'c' is pressed
            screenshot(frame, True)
            
        if ch == ord('q'): # calls screenshot function when 'c' is pressed
            break
        
        #print(faces_objects)
        cv2.imshow('Video', frame)       
    
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()