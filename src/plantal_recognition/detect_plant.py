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
 
 
thres = 0.70 # Threshold to detect object
 
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip(' ').split('\n')
# print(classNames)
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
 
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True) 

def detect_plant(success, img):
    
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
            cv2.rectangle(img,box,color=(0,255,0),thickness=2)
            prev = 'person'
            if(classNames[classId-1]!=prev and (classNames[classId-1]=='banana' or classNames[classId-1]=='apple' or classNames[classId-1]=='orange')):
                print("added",classNames[classId-1],"list updated")
                prev = classNames[classId-1]
                with open('items_list.csv', mode='a',newline='') as items_list:
                    items_writer = csv.writer(items_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    today = date.today()
                    dateTimeObj = datetime.now()
                    day = ""
                    day += str(dateTimeObj.day)+"-"+str(dateTimeObj.month)+"-"+str(dateTimeObj.year)+" "+str(dateTimeObj.hour)+":"+str(dateTimeObj.minute)
                    # date = datetime.datetime().strftime(today,"%d-%m-%Y, %H:%M")
                    if(classNames[classId-1]=='banana'):
                        expiry = today + timedelta(days=3)
                        items_writer.writerow([classNames[classId-1], day, expiry])
                    elif(classNames[classId-1]=='apple'):
                        expiry = today + timedelta(days=5)
                            items_writer.writerow([classNames[classId-1], day, expiry])