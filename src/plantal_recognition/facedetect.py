'''
Created on Jul 6, 2021

@author: yann

Originally based on https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81 but was later replaced because of tremendous biases in the model
Now, the model used is from Adam Geitgey's github repo, and more specifically based on this script : https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam.py
'''

import cv2
import face_recognition
import numpy as np
from plantal_recognition.cam import save_frame

cascPath = "../data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def load_model():
    cascPath = "../data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    return faceCascade

# def detect_faces(frame, model):
#     '''
#     Vieille version de l'algo, qui ne prend pas en compte la diversité des visages
#     '''
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     faces = model.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(30, 30)
#     )
#
#     # Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#
#     #print(type(faces))
#     return faces

def detect_faces(frame):
    '''
    Cette fonction est basée sur un CNN et reconnait l'extrême majorité des visages
    '''
    # Resize frame of video to 1/4 size for faster face recognition processing
    save_frame(frame, "../data/last_frame.png")
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    
    # the hog model doesn't work with this program. I suspect this is because of some API conflicting with requests
    face_locations = face_recognition.face_locations(rgb_small_frame, 1, "cnn")  
    final_faces = []

    # Display the results
    for (top, right, bottom, left) in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        final_faces.append((left, top, right - left, bottom - top))

    #print(type(np.asarray(np.array(final_faces, dtype=np.int32))))
    return np.array(final_faces, dtype=np.int32)
    
def crop_faces(frame, faces):
    cropped_frames = []

    for (x, y, w, h) in faces :
        cropped_frames.append(frame[y:y+h, x:x+w])
    
    return cropped_frames

