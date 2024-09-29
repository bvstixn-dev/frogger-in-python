import pygame, sys, random
from object import *
from frog import *
from lane import *

class Game:
    def __init__(self, screen_dimensions, screen_caption, screen_color):
        pygame.init()
        pygame.display.set_mode(screen_dimensions)
        pygame.display.set_caption(screen_caption)
        
        self.screen_color = screen_color
        self.DISPLAY = pygame.display.get_surface()
        
        #sprite group
        
        self.object_group = pygame.sprite.Group()
        self.car_group = pygame.sprite.Group()
        self.river_group = pygame.sprite.Group()
        self.frog_group = pygame.sprite.Group()
        
        
        
        self.all_group = [self.object_group, self.car_group, self.river_group, self.frog_group]
        #ojo
        self.river_speeds = {}
        #self.river_group = {}
        #
        self.assetSetup()
    
    def assetSetup(self):
        
        Object((0,0), (672, 768), "assets/background.png", self.object_group)
        #Pasto/grass
        for x in range(14):
            Object((x*48, 384), (48, 48), "assets/grass/purple.png", self.object_group)
            Object((x*48, 672), (48, 48), "assets/grass/purple.png", self.object_group)
        
        for x in range(28):
            Object((x*24, 72), (24, 72), "assets/grass/green.png", self.object_group)
            
        #lanes
        speeds = [-1.25, -1, -.75, -.5, -.25, .25, .5, .75, 1, 1.25]
        random.shuffle(speeds)
        
        #river lanes
        for y in range(5):
            y_pos = y*48 + 144
            new_lane = Lane((0, y_pos), self.river_group, speeds.pop(), "river")
            self.river_speeds[y_pos // 48] = new_lane.speed
            #possible error
        #street lanes
        for y in range(5):
            y_pos = y*48 + 432
            Lane((0, y_pos), self.car_group, speeds.pop(), "street")
        
        
        
        
        self.frog = Frog((336, 672), (48, 48), "assets/froggy/up.png", self.frog_group, [self.car_group, self.river_group], self.river_speeds)
        
        
    
    
    
    def run(self):
        while True:
            self.DISPLAY.fill(self.screen_color)
            self.frog.keyups = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    self.frog.keyups.append(event.key)
            
            for group in self.all_group:
                for sprite in group:
                    sprite.update()
                group.draw(self.DISPLAY)
            pygame.display.update()
            

game = Game((672, 768), "Frogger en python!", (0,0,0)) #14x16
game.run()