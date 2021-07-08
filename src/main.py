'''
Created on Jul 6, 2021

@author: yann
'''

import cv2
import numpy
from plantal_recognition.facedetect import load_model, detect_faces
from plantal_recognition.cam import screenshot
from plantal_recognition.face import analyze_faces, init_faces
from plantal_recognition.detect_plant import detect_plant

def concat_arrays(arr1, arr2):
    if numpy.shape(arr1) == (0,) :
        return arr2
    elif numpy.shape(arr2) == (0,) :
        return arr1
    else :
        return numpy.concatenate((faces, found_plants), axis=0)

if __name__ == '__main__':
    
    faceCascade = load_model()
    
    video_capture = cv2.VideoCapture(0)
    faces_objects = init_faces(2)
    print(faces_objects)
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
    
        _, faces = detect_faces(frame, faceCascade)
        if len(faces) == 0:
            faces = numpy.ndarray((0,))
            
        # print(ret)
        # Display the resulting frame
    
        ch = cv2.waitKey(5)
        
        if ch == 27:
            break

        found_plants = detect_plant(ret, frame)

        #print("faces " + str(type(faces)) + " " + str(numpy.shape(faces)) + " " + str(faces))
        #print("plants " + str(type(found_plants)) + " " + str(numpy.shape(found_plants)) + " " + str(found_plants))


        faces_objects = analyze_faces(frame, faces_objects, concat_arrays(faces, found_plants), 2)
        
        if ch == ord('c'): # calls screenshot function when 'c' is pressed
            screenshot(frame, True)
            
        if ch == ord('q'): # calls screenshot function when 'c' is pressed
            break
        
        #print(faces_objects)
        cv2.imshow('Video', frame)       
    
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()