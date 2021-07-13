'''
Created on Jul 7, 2021

@author: yann
'''

import cv2
import math

lineThickness = 3
offset = 20
increment = 20

class ProgressBar(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.percentage = 0
        
    def update(self, frame, rect):
        if self.percentage < 100:
            self.percentage += 20
            frame = self.draw(frame, rect)
        return frame
    
    def is_full(self):
        return (self.percentage == 100)
    
    def get_value(self):
        return self.percentage
    
    def draw(self, currentframe,rect):
        left_x, top_y, width, height = rect
        cv2.line(currentframe, (left_x, top_y + offset + height), 
                 (math.ceil(left_x + width * self.percentage/100), top_y + offset + height), (0, 255, 0), lineThickness)
        return currentframe