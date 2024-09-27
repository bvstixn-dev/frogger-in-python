import constantes
import pygame
class Obstaculo:
    def __init__(self, x, y, image):
        self.shape = pygame.Rect(0, 0, constantes.ANCHO_OBTACULO, constantes.ALTO_OBTACULO)
        self.shape.center = (x, y)
        