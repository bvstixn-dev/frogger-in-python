import pygame
import constantes
class Personaje():
    def __init__(self, x, y, image):
        self.flip_x = False
        self.flip_y = False
        self.image = image
        self.shape = self.image.get_rect()
        #Tamano de rectangulo
        #self.shape = pygame.Rect(0, 0, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
        self.shape.center = (x, y)
    def movimiento(self, delta_x, delta_y):
        #movimiento flip
        if delta_x < 0:
            self.flip_x = True
        if delta_x > 0:
            self.flip_x = False
        if delta_y < 0:
            self.flip_y = False
        if delta_y > 0:
            self.flip_y = True
        
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y
    
    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip_x, self.flip_y)
        ventana.blit(imagen_flip, self.shape)
        #pygame.draw.rect(ventana, constantes.COLOR_PERSONAJE, self.shape)
    