'''
Created on Jul 6, 2021

@author: yann
'''

import cv2
from facedetect import load_model, detect_faces, crop_faces
from cam import screenshot, draw_label, save_frames, data_path
from plantnet import send_request, get_most_probable_species, get_most_probable_species_confidence

if __name__ == '__main__':
    
    faceCascade = load_model()
    
    video_capture = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
    
        frame, faces = detect_faces(frame, faceCascade)
        # print(ret)
        # Display the resulting frame
    
        ch = cv2.waitKey(5)
        
        if ch == 27:
            break
        if ch == ord('c'): # calls screenshot function when 'c' is pressed
            
            frames_faces = crop_faces(frame, faces)
            save_frames(frames_faces, data_path+"face")
            scientificNames = []
            
            
            for idx, crop in enumerate(frames_faces) :
                json = send_request(data_path+"face"+str(idx)+".png")
                #print(idx)
                #cv2.imshow("crop"+str(idx), crop)            
            
                try:
                    species = get_most_probable_species(json)
                    confidence_score = get_most_probable_species_confidence(json)
                    scientificNames.append(species['scientificNameWithoutAuthor'])
                    
                    label = scientificNames[idx] + " " + confidence_score+"%"
                    print(str(idx) + " " + label)
                    draw_label(frame, faces[idx], scientificNames[idx] + " " + confidence_score+"%")
                    
                except TypeError:
                    draw_label(frame, faces[idx], "unknown species", False, (0, 0, 255))
            
            screenshot(frame, True)
            
        if ch == ord('q'): # calls screenshot function when 'c' is pressed
            break
        
        cv2.imshow('Video', frame)       
    
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()