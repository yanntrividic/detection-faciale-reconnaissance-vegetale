'''
Created on Jul 6, 2021

@author: yann
https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
'''

import cv2

cascPath = "../data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def load_model():
    cascPath = "../data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    return faceCascade

def detect_faces(frame, model):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = model.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame, faces
    
def crop_faces(frame, faces):
    cropped_frames = []

    for (x, y, w, h) in faces :
        cropped_frames.append(frame[y:y+h, x:x+w])
    
    return cropped_frames

