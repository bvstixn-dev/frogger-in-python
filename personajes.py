import pygame
import constantes
class Personaje():
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
        self.shape.center = (x, y)
    
    
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, (0, 128, 0), self.shape)