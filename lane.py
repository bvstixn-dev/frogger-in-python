import random, pygame
from obstacle import *
class Lane:
    def __init__(self, pos, group, speed, lane_type):
        """
        Inicializamos una nueva instancia del carril(lane)
        -------------------------------------------------------------------
        Parametos:
        - pos (tuple): Posicion (x, y) del carril en la pantalla
        - group (pygame.sprite.Group): El grupo que pertenece al carril
        - speed (float): La velocidad de los obstaculos en el carril
        - lane_type (str): El tipo de carril ('street' o 'river')
        -------------------------------------------------------------------
        """
        
        self.pos = pos              #Posicion del carril
        self.group = group          #Grupo de sprites el que anadira al carril
        self.speed = speed          #Velocidad de movimiento de los obstaculos
        self.lane_type = lane_type  #tipo de carril: 'street' | 'river'
        
        #configura los obstaculos del carril
        self.setupObstacles()
    
    def update(self, delta_tiempo):
        
        for obstacle in self.group:
            obstacle.pos = (obstacle.pos[0] + self.speed * delta_tiempo, obstacle.pos[1])
            obstacle.rect.topleft = obstacle.pos
    
    def setupObstacles(self):
        """
        Configura los obstaculos en el carril dependiendo de su tipo('street' | 'river') y direccion('left' | 'right')
        """
        #determina la direccion del movimiento de los obstaculos
        if self.speed > 0:
            self.direction = "right"
        else:
            self.direction = "left"
        
        #Configura los obstaculos dependiendo del tipo de carril
        if self.lane_type == "street":
            # Selecciona una imagen del coche aleatorio
            car = random.randint(1,3)
            image_directory = f"assets/{self.lane_type}/{self.direction}/{car}.png"
            
            #Crea tres coches en posiciones fijas en el carril
            Obstacle(self.pos, (48, 48), image_directory, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 5*48, self.pos[1]), (48, 48), image_directory, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 10*48, self.pos[1]), (48, 48), image_directory, self.group, self.speed).setImage()
        #Si el carril es de tipo rio('river'), se crean tortugas y troncos
        elif self.lane_type == "river":
            if self.direction == "left":
                #Define las imagenes para las tortugas segun la direccion
                left, middle, right = f"assets/{self.lane_type}/{self.direction}/turtle.png", f"assets/{self.lane_type}/{self.direction}/turtle.png", f"assets/{self.lane_type}/{self.direction}/turtle.png"
            #Selecciona imagenes del tronco segun la direccion
            elif self.direction == "right":
                left, middle, right = f"assets/{self.lane_type}/{self.direction}/left.png", f"assets/{self.lane_type}/{self.direction}/middle.png", f"assets/{self.lane_type}/{self.direction}/right.png"
                
            # Crea 3 tortugas o troncos en posiciones fijas en el carril
            Obstacle(self.pos, (48, 48), left, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 48, self.pos[1]), (48, 48), middle, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 2*48, self.pos[1]), (48, 48), right, self.group, self.speed).setImage()
            
            #crea tres tortugas o troncos adicionales en el carril
            Obstacle((self.pos[0] + 7*48, self.pos[1]), (48, 48), left, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 8*48, self.pos[1]), (48, 48), middle, self.group, self.speed).setImage()
            Obstacle((self.pos[0] + 9*48, self.pos[1]), (48, 48), right, self.group, self.speed).setImage()
            