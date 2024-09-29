import pygame

from object import *

class Frog(Object):
    def __init__(self, pos, size, image_directory, group, collision_groups, river_speeds):
        """
        Inicializa la rana en el juego
        -------------------------------------------------------------------
        Parametros:
        pos: Posicion inicial de la rana (x, y)
        size: Tamano de la rana (ancho, alto)
        image_directory: Ruta de la imagen de la rana
        group: Grupo de sprites a la que pertenece la rana
        colission_group: Grupo de sprites con las que la rana puede colisionar
        river_speed: Velocidades diferentes en el carril del rio
        -------------------------------------------------------------------
        """
        super().__init__(pos, size, image_directory, group)
        
        self.keyups = [] #Almacena las teclas que han sido soltadas
        
        self.collision_groups = collision_groups #Grupos con los que puede colisionar
        self.river_speeds = river_speeds #Velocidades del rio
        self.x_speed = 0 #velocidad horizontal inicial
    
    def moveFrog(self):
        """
        Mueve la rana segun las teclas precionadas y actualiza su posicion
        Si la pantalla sale de la pantalla, llama a la funcion killFrog().
        """
        x = self.pos[0]
        y = self.pos[1]
        
        #Controles de movimiento
        if pygame.K_UP in self.keyups:
            self.image_directory = "assets/froggy/up.png"
            y -= 48 #Mueve hacia arriba
        
        if pygame.K_DOWN in self.keyups:
            self.image_directory = "assets/froggy/down.png"
            y += 48 #Mueve hacia abajo
            
        
        if pygame.K_LEFT in self.keyups:
            self.image_directory = "assets/froggy/left.png"
            x -= 48 #Movimiento hacia la izquierda
       
        if pygame.K_RIGHT in self.keyups:
            self.image_directory = "assets/froggy/right.png"
            x += 48 #Movimiento hacia la derecha
        
        x += self.x_speed #Aplica la velocidad horizontal
        
        #Verifica los limites de la pantalla y mata a la rana si sale
        if x <= -48 or x > 48*14 or y > 48*16:
            self.killFrog()
            return
        #Actualiza la posicion de la rana
        self.pos = (x, y)
    
    def checkCollisions(self):
        """
        Verifica si la rana ha colisionado con algun obstaculo.
        Si hay una colision y la rana esta en un carril del rio, se aplica la velocidad del rio,
        y en caso contrario, se llama a la funcion killFrog()
        """
        
        self.setImage() #Establece la imagen actual de la rana
        
        #Variable de colision
        collided = False
        for sprite_group in self.collision_groups:
            if pygame.sprite.spritecollideany(self, sprite_group):
                collided = True #Detecta la colision
        
        lane = self.pos[1] // 48 #Determina en que carril se encuentra la rana
        if collided:
            if lane < 8: #Si esta en una lane de rio
                self.x_speed = self.river_speeds[lane] #Establece la velocidad del rio
            else:
                self.killFrog() #Mata a la rana si esta en la calle
        else:
            self.x_speed = 0 #Resetea la velocidad horizontal
            if lane < 8: #Si esta en una lane de rio pero no hay colision entonces mata a la rana
                self.killFrog()
                
    
    
    def killFrog(self):
        """
        Resetea la rana a su posicion inicial y establece su imagen
        """
        self.x_speed = 0 #resetea la velocidad horizontal
        
        #restablece la posicion y la imagen de la rana
        self.pos = (336, 672)
        self.image_directory = "assets/froggy/up.png"
        self.setImage() #establece la imagen
        
    
    def update(self):
        self.setImage() #actualiza la imagen
        self.moveFrog() #Mueve a la rana
        self.checkCollisions() #Verifica colisiones