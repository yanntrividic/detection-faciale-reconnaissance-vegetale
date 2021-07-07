'''
Created on Jul 7, 2021

@author: yann
'''

import math
from .bar import ProgressBar
from .cam import draw_label

error_thresh = 100

class Face(object):
    '''
    classdocs
    '''


    def __init__(self, rect):
        '''
        Constructor
        '''
        self.progress_bar = ProgressBar() 
        self.label = None
        self.rect = rect
    
    def update(self, rects):
        scores = []
        for rect in rects :
            scores.append(self.get_score(rect))
        
        best = min(scores)
        
        if min(scores) < error_thresh:
            self.rect = rects.index(best)
            self.progress_bar.update()
            
            if self.progress_bar.is_full():
                self.label = self.get_label()
                
            if self.label is not None :
                self.draw_label()
        
    def get_score(self, rect):
        old_x, old_y, old_w, old_h = self.rect
        x, y, w, h = rect
        return math.sqrt((old_x - x)^2 + (old_y - y)^2 + (old_x + old_w - x - w)^2 + (old_x + old_h - x - h)^2) 
    
    def get_label(self):
        #TODO : adapter ça :
        
        # json = send_request(data_path+"face"+str(idx)+".png")
        # #print(idx)
        # #cv2.imshow("crop"+str(idx), crop)            
        #
        # try:
        #     species = get_most_probable_species(json)
        #     confidence_score = get_most_probable_species_confidence(json)
        #     scientificNames.append(species['scientificNameWithoutAuthor'])
        #
        #     label = scientificNames[idx] + " " + confidence_score+"%"
        #     print(str(idx) + " " + label)
        #     draw_label(frame, faces[idx], scientificNames[idx] + " " + confidence_score+"%")
        #
        # except TypeError:
        #     draw_label(frame, faces[idx], "unknown species", False, (0, 0, 255))
            
        pass
    
    def draw_label(self, frame):
        draw_label(frame, self.rect, self.label)
        