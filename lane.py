import random, pygame
from obstacle import *
class Lane:
    def __init__(self, pos, group, speed, lane_type):
        self.pos = pos
        self.group = group
        self.speed = speed
        self.lane_type = lane_type
        
        self.setupObstacles()
    
    def setupObstacles(self):
        if self.speed > 0:
            self.direction = "right"
        else:
            self.direction = "left"
        
        if self.lane_type == "street":
            car = random.randint(1,2)
            image_directory = f"assets/{self.lane_type}/{self.direction}/{car}.png"
            
            Obstacle(self.pos, (48, 48), image_directory, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 5*48, self.pos[1]), (48, 48), image_directory, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 10*48, self.pos[1]), (48, 48), image_directory, self.group, self.speed).setImage()
        
        elif self.lane_type == "river":
            if self.direction == "left":
                left, middle, right = f"assets/{self.lane_type}/{self.direction}/turtle.png", f"assets/{self.lane_type}/{self.direction}/turtle.png", f"assets/{self.lane_type}/{self.direction}/turtle.png"
            
            elif self.direction == "right":
                left, middle, right = f"assets/{self.lane_type}/{self.direction}/left.png", f"assets/{self.lane_type}/{self.direction}/middle.png", f"assets/{self.lane_type}/{self.direction}/right.png"
                
            
            Obstacle(self.pos, (48, 48), left, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 48, self.pos[1]), (48, 48), middle, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 2*48, self.pos[1]), (48, 48), right, self.group, self.speed).setImage()
            
            Obstacle((self.pos[0] + 7*48, self.pos[1]), (48, 48), left, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 8*48, self.pos[1]), (48, 48), middle, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 9*48, self.pos[1]), (48, 48), right, self.group, self.speed).setImage()
        