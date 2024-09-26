import pygame
import constantes
class Personaje():
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
        self.shape.center = (x, y)
    def movimiento(self, delta_x, delta_y):
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y
    
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, constantes.COLOR_PERSONAJE, self.shape)
    
    