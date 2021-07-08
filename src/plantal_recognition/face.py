'''
Created on Jul 7, 2021

@author: yann
'''

import math
from .bar import ProgressBar
from .cam import draw_label, data_path, save_frame
from .plantnet import send_request, get_most_probable_species, get_most_probable_species_confidence
from .facedetect import crop_faces

error_thresh = 10000
nb_faces = 2

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
        
        #print(score)
        
        if score < error_thresh:
            self.rect = rect
            frame = self.progress_bar.update(frame, rect)
            
            if self.progress_bar.is_full() and self.label is None:
                save_frame(crop_faces(frame, [self.rect])[0], data_path+"face"+str(self.nb)+".png")
                self.label = self.get_label()
                print(self)
                
            if self.label is not None :
                self.draw_label(frame)
                
            return True # Si la valeur retournée est True, alors on considère que l'update a pu avoir lieu

        else :
            return False
        
    def get_score(self, rect):
        if self.rect is not None :
            old_x, old_y, old_w, old_h = self.rect
        else :
            old_x, old_y, old_w, old_h = (float('inf'), float('inf'), float('inf'), float('inf'))
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
            
        return label
    
    def draw_label(self, frame):
        draw_label(frame, self.rect, self.label)
    
    def compare_rect(self, rect):
        my_x, my_y, my_w, my_h = self.rect
        x, y, w, h = rect
        return my_x == x and my_y == y and my_w == w and my_h == h

def assign_rect_to_faces(frame, rects, old_faces):
    scores = []
    #print("in the assign function")

    for idx, face in enumerate(old_faces):
        scores.append([])
        for rect in rects:
            scores[idx].append((face.get_score(rect), rect, face))
        scores[idx] = sorted(scores[idx], key=lambda x: x[0]) # a voir si la valeur est retournée ou si la liste est triée en elle-même
        print(scores[idx])
        old_faces[idx] = scores[idx]

    
    return old_faces
    
      
def assign_best_suited_face(frame, rect, old_faces):
    print(old_faces)
    score1, score2 = old_faces[0].get_score(rect), old_faces[1].get_score(rect)
    if score1 < score2:
        old_faces[0].update(frame, (score1, rect, old_faces[0]))
        old_faces[1] = Face(None, 1)
    else :
        old_faces[1].update(frame, (score2, rect, old_faces[1]))
        old_faces[0] = Face(None, 0)
    return old_faces      
            
def analyze_faces(frame, old_faces, rects, nb_faces):
    '''
    takes as input an array of Face object and a series of frames that correspond to a found face
    '''
    
    if len(rects) == 0:
        faces = init_faces(nb_faces)
    
    elif len(rects) == 1 :
        return assign_best_suited_face(frame, rects[0], old_faces)
      
    elif len(rects) == 2 :
        return assign_rect_to_faces(frame, rects, old_faces)
      
    
    # if old_faces is None or len(old_faces) != len(faces): #si old_faces est vide, on le crée
    #     faces_objects = []
    #     for idx, face in enumerate(faces): 
    #         faces_objects.append(Face(face, idx))
    #     return faces_objects
    #
    # elif len(old_faces) < len(faces): #s'il y a moins de faces dans old_faces que dans ce qui est détecté, on en ajoute une
    #     for i in range(len(faces) - len(old_faces)):
    #         old_faces.append(Face((250, )*4,
    #                               len(old_faces) + i))
    #
    # #maintenant on peut juste essayer d'update
    
    return assign_rect_to_faces(frame, faces, old_faces)

def init_faces(nb):
    faces = []
    for i in range(nb):
        faces.append(Face(None, i))
    return faces
        