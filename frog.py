import pygame

from object import *

class Frog(Object):
    def __init__(self, pos, size, image_directory, group, collision_groups, river_speeds):
        super().__init__(pos, size, image_directory, group)
        #ojo aca
        self.keyups = []
        
        self.collision_groups = collision_groups
        self.river_speeds = river_speeds
        self.x_speed = 0
    
    def moveFrog(self):
        x = self.pos[0]
        y = self.pos[1]
        
        if pygame.K_UP in self.keyups:
            self.image_directory = "assets/froggy/up.png"
            y -= 48
        if pygame.K_DOWN in self.keyups:
            self.image_directory = "assets/froggy/down.png"
            y += 48
            
        if pygame.K_LEFT in self.keyups:
            self.image_directory = "assets/froggy/left.png"
            x -= 48
        if pygame.K_RIGHT in self.keyups:
            self.image_directory = "assets/froggy/right.png"
            x += 48
        x += self.x_speed
        if x <= -48 or x > 48*14 or y > 48*16:
            self.killFrog()
            return
        
        self.pos = (x, y)
    
    def checkCollisions(self):
        self.setImage()
        
        collided = False
        for sprite_group in self.collision_groups:
            if pygame.sprite.spritecollideany(self, sprite_group):
                collided = True
        
        lane = self.pos[1]//48
        if collided:
            if lane < 8:
                self.x_speed = self.river_speeds[lane]
            else:
                self.killFrog()
        else:
            self.x_speed = 0
            if lane < 8:
                self.killFrog()
                
    
    
    def killFrog(self):
        self.x_speed = 0
        
        self.pos = (336, 672)
        self.image_directory = "assets/froggy/up.png"
        self.setImage()
        
    
    def update(self):
        self.setImage()
        self.moveFrog()
        self.checkCollisions()