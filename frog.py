import pygame

from object import *
from safe_zone import *

class Frog(Object):
    def __init__(self, pos, size, image_directory, group, collision_groups, river_speeds, game):
        """
        Inicializa la rana en el juego
        -------------------------------------------------------------------
        Parametros:
        - pos: Posicion inicial de la rana (x, y)
        - size: Tamano de la rana (ancho, alto)
        - image_directory: Ruta de la imagen de la rana
        - group: Grupo de sprites a la que pertenece la rana
        - colission_group: Grupo de sprites con las que la rana puede colisionar
        - river_speed: Velocidades diferentes en el carril del rio
        -------------------------------------------------------------------
        """
        super().__init__(pos, size, image_directory, group)
        
        self.keyups = [] #Almacena las teclas que han sido soltadas
        
        self.collision_groups = collision_groups #Grupos con los que puede colisionar
        self.river_speeds = river_speeds #Velocidades del rio
        self.x_speed = 0 #velocidad horizontal inicial
        self.game = game #Referencia al juego para manejar las vidas y el puntaje
        self.image = pygame.image.load(image_directory)
        self.image = pygame.transform.scale(self.image, size)  # Escala la imagen al tamaño especificado
        self.rect = self.image.get_rect(topleft=pos)
        
        
        
        
        
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
            pygame.mixer.Sound.play(self.game.hop_sound)
        
        if pygame.K_DOWN in self.keyups:
            self.image_directory = "assets/froggy/down.png"
            y += 48 #Mueve hacia abajo
            pygame.mixer.Sound.play(self.game.hop_sound)
            
        
        if pygame.K_LEFT in self.keyups:
            self.image_directory = "assets/froggy/left.png"
            x -= 48 #Movimiento hacia la izquierda
            pygame.mixer.Sound.play(self.game.hop_sound)
            
       
        if pygame.K_RIGHT in self.keyups:
            self.image_directory = "assets/froggy/right.png"
            x += 48 #Movimiento hacia la derecha
            pygame.mixer.Sound.play(self.game.hop_sound)
        
        x += self.x_speed #Aplica la velocidad horizontal
        #Comprobar si frogger llega a la parte superior de la pantalla
        if y < 130:
            print("Test de si frog llego al objetivo")
            self.game.increase_score(100) #Anadimos los puntos
            self.reset_position()
            self.game.increase_live()
            
        
        #Verifica los limites de la pantalla y mata a la rana si sale
        """if x <= -48 or x > 48*14 or y > 48*16:
            self.killFrog()
            return"""
        #Actualiza la posicion de la rana
        
        self.pos = (x, y)
    
    def reset_position(self):
        """Reinicia la posicion de la rana al inicio"""
        self.pos = (336, 672)
        self.x_speed = 0
    
    
    def checkCollisions(self):
        """
        Verifica si la rana ha colisionado con algun obstaculo.
        Si hay una colision y la rana esta en un carril del rio, se aplica la velocidad del rio,
        y en caso contrario, se llama a la funcion killFrog()
        """
        
        self.setImage() #Establece la imagen actual de la rana
        
        for sprite in self.game.object_group:
            if isinstance(sprite, SafeZone):
                sprite.check_frog(self)
                return #Si frogeger llega al hueco, no necesita seguri verificando colisiones
                
        
        
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
                pygame.mixer.Sound.play(self.game.die_land_sound)
        else:
            self.x_speed = 0 #Resetea la velocidad horizontal
            if lane < 8: #Si esta en una lane de rio pero no hay colision entonces mata a la rana
                self.killFrog()
                pygame.mixer.Sound.play(self.game.die_land_sound)
                
    
    
    def killFrog(self):
        """
        Resetea la rana a su posicion inicial y establece su imagen
        
        self.x_speed = 0 #resetea la velocidad horizontal
        
        #restablece la posicion y la imagen de la rana
        self.pos = (336, 672)
        self.image_directory = "assets/froggy/up.png"
        self.setImage() #establece la imagen
        """
        #Accion cuando muere la rana
        self.game.lose_life()
    
    def update(self):
        self.setImage() #actualiza la imagen
        self.moveFrog() #Mueve a la rana
        self.checkCollisions() #Verifica colisiones