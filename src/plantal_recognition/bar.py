'''
Created on Jul 7, 2021

@author: yann
'''

import cv2
import math

lineThickness = 1

class ProgressBar(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.percentage = 0
        
    def update(self, frame, left_x, top_y, width):
        self.percentage += 5
        self.draw(frame, left_x, top_y, width)
    
    def is_full(self):
        return (self.percentage == 100)
    
    def draw(self, currentframe, left_x, top_y, width):
        cv2.line(currentframe, (left_x, top_y), (math.ceil(width * self.percentage/100), top_y), (0, 255, 0), lineThickness)