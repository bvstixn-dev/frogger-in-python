import pygame
from object import *
from frog import *
from object import *
class SafeZone(pygame.sprite.Sprite):
    def __init__(self, position, size, image_path, group, game):
        super().__init__(group)
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(position, size)
        self.game = game
        self.is_occupied = False
        
    def check_frog(self, frog):
        if not self.is_occupied and self.rect.colliderect(frog.rect):
            self.is_occupied = True
            self.game.increase_score(100)
            frog.reset_position()
            pygame.mixer.Sound.play(self.game.success_sound)
            self.image_directory = "assets/grass/ranita.png"
            self.setImage()
    