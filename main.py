import pygame, sys, random
from object import *
from frog import *
from lane import *

class Game:
    def __init__(self, screen_dimensions, screen_caption, screen_color):
        """
        Inicializamos nuesta configuracion de frogger, configura las dimensiones de la pantalla, el titulo de la ventana y los grupos de sprites
        -------------------------------------------------------------------
        Parametros:
        - screen_dimensions: ancho y alto de la ventana del juego(pixeles)
        - screen_caption: titulo de la ventana del juego
        - screen_color: color de fondo de la pantalla (RGB)
        -------------------------------------------------------------------
        """
        pygame.init()
        pygame.display.set_mode(screen_dimensions)
        pygame.display.set_caption(screen_caption)
        
        
        self.screen_color = screen_color
        self.DISPLAY = pygame.display.get_surface() #Superficie donde se dibujara el juego
        
        
        #Grupos de sprites (objetos)
        self.object_group = pygame.sprite.Group()
        self.car_group = pygame.sprite.Group()
        self.river_group = pygame.sprite.Group()
        self.frog_group = pygame.sprite.Group()
        
        
        #Almacena todos los grupos de sprites para actualizarlos y dibujarlos
        self.all_group = [self.object_group, self.car_group, self.river_group, self.frog_group]
        
        #Diccionario para almacenar las velocidades de las lineas del rio
        self.river_speeds = {}
        
        #Configuracion inicial de los objetos del juego
        self.assetSetup()
    
    def assetSetup(self):
        """
        Configura los objectos iniciales, incluyendo el fondo, el pasto y los autos
        """
        
        #Fondo/Background
        Object((0,0), (672, 768), "assets/background.png", self.object_group)
        
        
        #Pasto/grass zonas donde la rana esta segura
        for x in range(14):
            Object((x*48, 384), (48, 48), "assets/grass/purple.png", self.object_group)
            Object((x*48, 672), (48, 48), "assets/grass/purple.png", self.object_group)
        
        #Pasto/grass ubicado en el area superior
        for x in range(28):
            Object((x*24, 72), (24, 72), "assets/grass/green.png", self.object_group)
            
        #Valocidades aleatorias para los autos y rio
        speeds = [-1.25, -1, -.75, -.5, -.25, .25, .5, .75, 1, 1.25]
        random.shuffle(speeds)
        
        #Carriles del rio
        for y in range(5):
            y_pos = y*48 + 144
            new_lane = Lane((0, y_pos), self.river_group, speeds.pop(), "river")
            self.river_speeds[y_pos // 48] = new_lane.speed
            #possible error
        
        #Carriles de la calle
        for y in range(5):
            y_pos = y*48 + 432
            Lane((0, y_pos), self.car_group, speeds.pop(), "street")
        
        #Inicializamos la rana frogger(posicion inicial(2 argumentos), su tamano, su imagen, su agrupacion de sprites y colisiones)
        self.frog = Frog((336, 672), (48, 48), "assets/froggy/up.png", self.frog_group, [self.car_group, self.river_group], self.river_speeds)
        
        
    
    
    
    def run(self):
        """Bucle principal del juego, maneja los eventos de entrada, actualiza los objetos y refresca la pantalla"""
        while True:
            #Rellena la pantalla con el color de fondo
            self.DISPLAY.fill(self.screen_color)
            
            #Movimiento de la rana segun la tecla presionada
            self.frog.keyups = []
            
            #Manejo de eventos (cerrar ventana, teclas presionadas)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    self.frog.keyups.append(event.key) # Almacena las teclas que se sueltan
            
            #Actualiza y dibuja todos los grupos de sprites
            for group in self.all_group:
                for sprite in group:
                    sprite.update()
                group.draw(self.DISPLAY)
            
            #Refresa la pantalla con nuevos dibujos
            pygame.display.update()
            

#Creamos un objeto con todos los atributos (Dimension de la ventana, Titulo de la ventana y color)
game = Game((672, 768), "Frogger en python!", (0,0,0)) # Pantalla de 14x16 bloques, (48 px por bloque)
#llamamos al metodo de la clase Game para correr el juego
game.run()