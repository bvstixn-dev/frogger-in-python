import pygame
from object import *

class Obstacle(Object):
    def __init__(self, pos, size, image, group, speed):
        """
        Inicializa uhn obstaculo en el juego
        -------------------------------------------------------------------
        Parametros:
        - pos: Posicion del obstaculo en la pantalla (x, y)
        - size: Tamano del obstaculo (ancho, alto)
        - image: Ruta de imagen del obstaculo
        - group: Grupo de sprite al que pertenece el obstaculo
        - speed: Velocidad a la que se movera el obstaculo
        -------------------------------------------------------------------
        """
        super().__init__(pos, size, image, group)
        self.speed = speed
    
    
    def moveObstacle(self):
        """
        Mueve el obstaculo en la direccion determinada por su velocidad. Si el obstaculo sale de la pantalla, 
        se reposiciona en el lado opuesto
        """
        #Obtenemos la posicion actual del obstaculo
        x = self.pos[0]
        y = self.pos[1]
        
        #Actualiza la posicion horizontal del obstaculo 
        x += self.speed
        
        #Determina si el obstaculo sale por la derecha, vuelve aparecer por la izquierda
        if x >= 48*15: #Considerando que la pantalla es de 15 columnas de 48px
            x = -48
        #Determina si el obstaculo sale por la izquierda, vuelve aparecer por la derecha
        if x <= 48 * -2: #Espacio adicional para el movimiento del obstaculo
            x = 48 * 14 #Regresa al borde derecho de la pantalla
        
        #Actualizamos la posicion del obstaculo    
        self.pos = (x, y)
    
    def update(self):
        """
        Actualiza la imagen del obstaculo y mueve el obstaculo en cada cuadro
        """
        self.setImage()
        self.moveObstacle()