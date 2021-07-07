'''
Created on Jul 7, 2021

@author: yann
'''

import math
from .bar import ProgressBar
from .cam import draw_label, data_path, save_frame
from .plantnet import send_request, get_most_probable_species, get_most_probable_species_confidence
from pickle import TRUE
from pip._internal.cli.cmdoptions import progress_bar
from .facedetect import crop_faces

error_thresh = 10000

class Face(object):
    '''
    classdocs
    '''
    
    def __init__(self, rect, nb):
        '''
        Constructor
        '''
        self.progress_bar = ProgressBar() 
        self.label = None
        self.rect = rect
        self.nb = nb
    
    def __repr__(self):
        return(str(self.nb)+" - "+str(self.label)+", "+str(self.progress_bar.get_value()) + "%")
    
    def update(self, frame, score_rect_tuple):
        score, rect, _ = score_rect_tuple
        
        print(score)
        
        if score < error_thresh:
            self.rect = rect
            frame = self.progress_bar.update(frame, rect)
            
            if self.progress_bar.is_full() and self.label is None:
                save_frame(crop_faces(frame, [self.rect])[0], data_path+"face"+str(self.nb)+".png")
                self.label = self.get_label()
                
            if self.label is not None :
                self.draw_label(frame)
                
            return True # Si la valeur retournée est True, alors on considère que l'update a pu avoir lieu

        else :
            return False
        
    def get_score(self, rect):
        old_x, old_y, old_w, old_h = self.rect
        x, y, w, h = rect
        return math.sqrt((old_x - x)**2 + (old_y - y)**2 + (old_x + old_w - x - w)**2 + (old_x + old_h - x - h)**2) 
    
    def get_label(self):
        #TODO : adapter ça :
        
        json = send_request(data_path+"face"+str(self.nb)+".png")
        #print(idx)
        #cv2.imshow("crop"+str(idx), crop)            
        
        try:
            species = get_most_probable_species(json)['scientificNameWithoutAuthor']
            confidence_score = get_most_probable_species_confidence(json)
                
            label = species + " " + confidence_score+"%"            
        
        except TypeError:
            label = "unknown species"
            
        print(str(self.nb) + " " + str(self.label))
        return label
    
    def draw_label(self, frame):
        draw_label(frame, self.rect, self.label)
    
    def compare_rect(self, rect):
        my_x, my_y, my_w, my_h = self.rect
        x, y, w, h = rect
        return my_x == x and my_y == y and my_w == w and my_h == h

def assign_rect_to_faces(frame, rects, old_faces):
    scores = []
    print("in the assign function")

    for rect in rects:
        for face in old_faces:
            scores.append((face.get_score(rect), rect, face))
    
    scores = sorted(scores, key=lambda x: x[0]) # a voir si la valeur est retournée ou si la liste est triée en elle-même
    print(scores)
    
    new_faces = [] # on va créer un nouveau tableau pour les old_faces qui passent l'update
    
    for face in old_faces: # la meilleure valeur est utilisée pour la face correspondante
        for score in scores:
            if face == score[2] : 
                result = face.update(frame, score)
                if result :
                    new_faces.append(face)
                break
    
    return new_faces
            
def analyze_faces(frame, old_faces, faces):
    '''
    takes as input an array of Face object and a series of frames that correspond to a found face
    '''
    
    if old_faces is None or len(old_faces) != len(faces): #si old_faces est vide, on le crée
        faces_objects = []
        for idx, face in enumerate(faces): 
            faces_objects.append(Face(face, idx))
        return faces_objects
    
    elif len(old_faces) < len(faces): #s'il y a moins de faces dans old_faces que dans ce qui est détecté, on en ajoute une
        for i in range(len(faces) - len(old_faces)):
            old_faces.append(Face((250, )*4,
                                  len(old_faces) + i))
    
    #maintenant on peut juste essayer d'update
    
    return assign_rect_to_faces(frame, faces, old_faces)
        