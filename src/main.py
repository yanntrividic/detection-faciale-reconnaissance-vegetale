'''
Created on Jul 6, 2021
@author: yann
'''

import cv2
import numpy
from plantal_recognition.facedetect import detect_faces
from plantal_recognition.cam import screenshot
from plantal_recognition.face import analyze_faces
from plantal_recognition.detect_plant import detect_plant


def concat_arrays(arr1, arr2):
    if numpy.shape(arr1) == (0,) :
        return arr2
    elif numpy.shape(arr2) == (0,) :
        return arr1
    else :
        return numpy.concatenate((faces, found_plants), axis=0)

if __name__ == '__main__':
       
    video_capture = cv2.VideoCapture(0)
    #video_capture.resi
    prv_frame_faces_and_plants, crt_frame_plants_and_ppl = None, None
    
    
    while True:
        # Capture frame-by-frame
        prv_frame_faces_and_plants = crt_frame_plants_and_ppl
        ret, frame = video_capture.read()
    
        faces = detect_faces(frame) # faces detection

        if len(faces) == 0:
            faces = numpy.ndarray((0,))
                
        ch = cv2.waitKey(5)
        
        if ch == 27:
            break

        found_plants = detect_plant(ret, frame)
        crt_frame_plants_and_ppl = concat_arrays(faces, found_plants)
        
        crt_frame_plants_and_ppl = analyze_faces(frame, prv_frame_faces_and_plants, crt_frame_plants_and_ppl)

        if ch == ord('c'): # calls screenshot function when 'c' is pressed
            screenshot(frame, True)
            
        if ch == ord('q'): # calls screenshot function when 'c' is pressed
            break
        
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        
        #uncomment this line if you want the output to be fullscreen
        #cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow('frame', frame)  

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()