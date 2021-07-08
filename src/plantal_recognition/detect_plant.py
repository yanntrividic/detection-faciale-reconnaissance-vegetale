'''
Created on Jul 7, 2021
@author: yann
based on:
https://jeanvitor.com/tensorflow-object-detecion-opencv/
https://github.com/krupa3/Fruits-and-vegetables-recognition
'''
    
# How to load a Tensorflow model using OpenCV
# Jean Vitor de Paulo Blog - https://jeanvitor.com/tensorflow-object-detecion-opencv/
 
import cv2
import numpy
 
 
thres = 0.5 # Threshold to detect object
 
classNames= []
classFile = '../models/coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip(' ').split('\n')
# print(classNames)
configPath = '../models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = '../models/frozen_inference_graph.pb'
 
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True) 

def detect_plant(success, img):
    
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    if len(classIds) != 0:
        for classId, _, box in zip(classIds.flatten(),confs.flatten(),bbox):
            found_plants = []
            if(classNames[classId-1]=='potted plant'):
                cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                #print("Potted plant found "+str(box)+" "+str(confidence)+"%")
                found_plants.append(box)
        return convert_box_coor(found_plants)
    #print("Non-vegetal detected")
    return numpy.empty(shape=(0,))
                     
def convert_box_coor(boxes):
    #print("boxes = " + str(boxes))
    if boxes is not None:
        new_coor = []        
        for box in boxes:
            print("box "+str(box))
            new_coor.append((box))
        #print("new_coor" + " " + str(new_coor))
        return numpy.array(new_coor)
    else:
        return numpy.empty(shape=(0,))