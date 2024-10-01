import pygame, sys, random, time
from object import *
from frog import *
from lane import *
#video import
import cv2
import numpy as np



class Menu:
    def __init__(self, screen):
        self.screen = screen 
        
        #Cargar fondo del menu
        self.bg_image = pygame.image.load("assets/background.png")#ruta del fondo
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())#Escalar imagen
        
        #Cargar logo de frogger
        self.logo_image = pygame.image.load("assets/logo_frogger.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (200, 100)) #Escalar imagen/logo
        
        #Cargar sonido
        self.select_sound = pygame.mixer.Sound("assets/music/sounds/select_sound.wav")
        self.push_start_sound = pygame.mixer.Sound("assets/music/sounds/push_start_sound.wav")
        
        #Fuentes para el menu
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
        #Opciones del menu
        self.options = ["Jugar", "Multijugador", "Skins", "Salir"]
        self.selected_option = 0
    
    def play_video_opencv(video_path, screen):
        video = cv2.VideoCapture(video_path)
        
        if not video.isOpened():
            print("Error no se pudo abrir el video")
            sys.exit()
        #importamos el sonido
        pygame.mixer.init()
        sound = pygame.mixer.Sound("assets/music/sounds/test_intro.wav")
        sound.play()
        
        
        
        fps = video.get(cv2.CAP_PROP_FPS)
        clock = pygame.time.Clock()
        
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
            
            frame_surface = pygame.transform.scale(frame_surface, screen.get_size())
            
            
            screen.blit(frame_surface, (0, 0))
            pygame.display.update()
            
            clock.tick(fps)
            
            for event in pygame.event.get():
                if event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        video.release()
                        pygame.quit()
                        sys.exit()
            pygame.time.delay(int(1000 / 30))
            
        video.release()
        
           
    def display_menu(self):
        #Dibujar el fondo
        self.screen.blit(self.bg_image, (0, 0))
        
        #dibujar el logo en el centro superior
        logo_rect = self.logo_image.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(self.logo_image, logo_rect)
        
        
        #dibujar las opciones del menu
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = (255, 255, 255)
            else:
                color = (50, 50, 50)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 300 + i * 100))
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
    
    def run(self):
        while True:
            self.display_menu() #Llamamos a la funcion para mostrar el menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                        self.select_sound.play() #reproducir sonido
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                        self.select_sound.play() #reproducir sonido
                    elif event.key == pygame.K_RETURN:
                        self.push_start_sound.play()
                        if self.selected_option == 0:
                            time.sleep(2)
                            return #Jugar
                        elif self.selected_option == 1:
                            print("Multijugador seleccionado") #Logica de multijugador
                        elif self.selected_option == 2:
                            print("Skins seleccionadas") #Logica de skins
                        elif self.selected_option == 3: 
                            pygame.quit()
                            sys.exit()
            
                
            

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
        ################################################
        #Iniciarlizar vidas y puntaje
        self.lives = 3
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf")
        
        
        
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
        self.frog = Frog((336, 672), (48, 48), "assets/froggy/up.png", self.frog_group, [self.car_group, self.river_group], self.river_speeds, self)
    
    def displayHUD(self):
        """
        Muestra las vidas, el puntaje y el maximo en la pantalla"""
        #print(f"Current score: {self.score}, High score: {self.high_score}") # Verificamos puntaje
        lives_surface = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        
        self.DISPLAY.blit(lives_surface, (10, 10))
        self.DISPLAY.blit(score_surface, (150,10))
        self.DISPLAY.blit(high_score_surface, (450, 10))
     
    
    
    
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
            ########################Mostrar HUD
            self.displayHUD()
                
            
            #Refresa la pantalla con nuevos dibujos
            pygame.display.update()
    #####################################
    def lose_life(self):
        """Reduce las vidas y reinicia la posicion de la rana"""
        self.lives -= 1
        print(f"Lives left: {self.lives}")
        if self.lives == 0:
            self.game_over()
        else:
            self.frog.reset_position()
            print("Froggy vuelve a su posicion original")
            
            
            
    def increase_score(self, points):
        """Aumenta el puntaje del jugador"""
        print("Test de incremento de score...")
        self.score += points
        print(f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            
    
    def game_over(self):
        """Termina el juego y reinicia los valores """
        print("Game over")
        self.lives = 4
        self.score = 0
        self.frog.reset_position        
    #######################################       



if __name__ == "__main__":
    #Creamos un objeto con todos los atributos (Dimension de la ventana, Titulo de la ventana y color)
    pygame.init()
    screen_dimensions = (672, 768)
    screen_caption = "Frogger en python!"
    screen_color = (0, 0, 0)
    
    #Configura la ventana
    screen = pygame.display.set_mode(screen_dimensions)
    pygame.display.set_caption(screen_caption)
    
    
    
    #Crea el menu y corre el juego
    game = Game(screen_dimensions, screen_caption, screen_color)
    menu = Menu.play_video_opencv("assets/video/test_intro.mp4", screen)
    menu = Menu(game.DISPLAY)
    
    
    menu.run()
    game.run()
    
    
    
    """
    game = Game((672, 768), "Frogger en python!", (0,0,0)) # Pantalla de 14x16 bloques, (48 px por bloque)
    menu = Menu(game.DISPLAY)
    menu.play_video("assets/video/videoo.mp4")
    menu.run()
    #llamamos al metodo de la clase Game para correr el juego
    game.run()"""
    
    
    
    