import pygame
from object import *

class Obstacle(Object):
    def __init__(self, pos, size, image, group, speed):
        super().__init__(pos, size, image, group)
        self.speed = speed
    
    
    def moveObstacle(self):
        x = self.pos[0]
        y = self.pos[1]
        
        
        x += self.speed
        
        if x >= 48*15:
            x = -48
        if x <= 48 * -2:
            x = 48 * 14
            
        self.pos = (x, y)
    
    def update(self):
        self.setImage()
        self.moveObstacle()