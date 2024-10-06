import pygame, sys, random, time
from object import *
from frog import *
from lane import *
from safe_zone import *
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
        self.logo_image = pygame.image.load("assets/frogger_title.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (200, 100)) #Escalar imagen/logo
        
        #Cargar sonido
        self.select_sound = pygame.mixer.Sound("assets/music/sounds/select_sound.wav")
        self.push_start_sound = pygame.mixer.Sound("assets/music/sounds/push_start_sound.wav")
        
        #Fuentes para el menu
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
        #Opciones del menu
        self.options = ["Jugar", "Multijugador", "Skins", "Salir"]
        self.selected_option = 0
        
        #cargar prototipo
        self.prototipo_image = pygame.image.load("assets/wireframes_multijugador.png")
        self.prototipo_image = pygame.transform.scale(self.prototipo_image, (400, 300))# ajusta segun necesario
        
        #Cargar prototipo de skin
        self.skins_image = pygame.image.load("assets/wireframes_skins.png")
        self.skins_image = pygame.transform.scale(self.skins_image, (400, 300))
        
        #rectangulo para el boton x (cierre)
        self.button_size = 40
        self.close_button_rect = pygame.Rect(600, 20, self.button_size, self.button_size)
        
        #estados
        self.showing_prototipo = False
        self.showing_skins = False
        
        
        
    
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #Salir del video con esc
                        video.release
                        sound.stop()
                        return
            
            #pygame.time.delay(int(1000 / 30))
        
        sound.stop()
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
    def display_prototipo(self):
        # Dibujar el fondo en blanco
        self.screen.fill((255, 255, 255))
        
        # Escalar la imagen del prototipo para que ocupe toda la pantalla
        scaled_prototipo_image = pygame.transform.scale(self.prototipo_image, self.screen.get_size())
        self.screen.blit(scaled_prototipo_image, (0, 0))  # Ajuste para que ocupe toda la pantalla
        
        # Dibujar el botón "X"
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)  # Botón rojo
        close_font = pygame.font.Font(None, 40)
        close_text = close_font.render('X', True, (255, 255, 255))
        self.screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y))
        pygame.display.flip()
    def display_skins(self):
            # Dibujar el fondo en blanco
        self.screen.fill((255, 255, 255))
        
        # Escalar la imagen de skins para que ocupe toda la pantalla
        scaled_skins_image = pygame.transform.scale(self.skins_image, self.screen.get_size())
        self.screen.blit(scaled_skins_image, (0, 0))  # Ajuste para que ocupe toda la pantalla
        
        # Dibujar el botón "X"
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)  # Botón rojo
        close_font = pygame.font.Font(None, 40)
        close_text = close_font.render('X', True, (255, 255, 255))
        self.screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y))
        
        pygame.display.flip()
        
    def run(self):
        while True:
            if not self.showing_prototipo and not self.showing_skins:
                self.display_menu()  # Mostrar menú principal
            elif self.showing_prototipo:
                self.display_prototipo()  # Mostrar pantalla de prototipo
            elif self.showing_skins:
                self.display_skins()  # Mostrar pantalla de skins
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.showing_prototipo and not self.showing_skins:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                            self.select_sound.play()  # Reproducir sonido
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                            self.select_sound.play()  # Reproducir sonido
                        elif event.key == pygame.K_RETURN:
                            self.push_start_sound.play()
                            if self.selected_option == 0:
                                time.sleep(2)
                                return  # Jugar
                            elif self.selected_option == 1:
                                # Mostrar prototipo para "Multijugador"
                                self.showing_prototipo = True
                            elif self.selected_option == 2:
                                # Mostrar prototipo para "Skins"
                                self.showing_skins = True
                            elif self.selected_option == 3:
                                pygame.quit()
                                sys.exit()
                else:
                    # Interacción con la pantalla de prototipo o skins
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.close_button_rect.collidepoint(event.pos):
                            self.showing_prototipo = False
                            self.showing_skins = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.showing_prototipo = False
                            self.showing_skins = False
        

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
        pygame.mixer.init() #Iniciamos el modulo o motor de sonido
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
        
        #Cargar sonidos
        
        #Almacena todos los grupos de sprites para actualizarlos y dibujarlos
        self.all_group = [self.object_group, self.car_group, self.river_group, self.frog_group]
        
        #Diccionario para almacenar las velocidades de las lineas del rio
        self.river_speeds = {}

        #iconos
        self.lives_icon = pygame.image.load("assets/froggy/icon.png")  # Cargar imagen de la vida (48x48)
        self.lives_icon = pygame.transform.scale(self.lives_icon, (32, 32))  # Redimensionar la imagen
        
        #Tiempo
        self.time_limit = 30 #limite x seg
        self.time_left = self.time_limit #tiempo restante
        self.start_time = pygame.time.get_ticks() # inicio del cronometro
        
        
        
        #Iniciarlizar vidas y puntaje
        self.lives = 3
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf")
        
        self.load_sounds()
        #Configuracion inicial de los objetos del juego
        self.assetSetup()
    
    def increase_live(self):
        self.lives += 1
        
    
    
    def display_timer(self):
        """"Muestra la barra de tiempo en la pantalla"""
        time_ratio = self.time_left / self.time_limit
        timer_width = int(300 * time_ratio) #Definimos el tiempo

        # Posición de la barra: inferior derecha
        x_pos = self.DISPLAY.get_width() - 210  # Ancho de la barra + margen
        y_pos = self.DISPLAY.get_height() - 50  # Altura de la barra

        # Crear superficie de fondo de la barra
        timer_background = pygame.Surface((200, 20))  # Fondo de la barra
        timer_background.fill((255, 0, 0))  # Color rojo

        # Crear superficie para la barra de tiempo
        timer_surface = pygame.Surface((timer_width, 20))  # Barra de tiempo
        timer_surface.fill((0, 255, 0))  # Color verde

        # Mostrar las superficies
        self.DISPLAY.blit(timer_background, (x_pos, y_pos))  # Fondo de la barra
        self.DISPLAY.blit(timer_surface, (x_pos, y_pos))  # Barra de tiempo
            
    def update_timer(self):
        """Actualiza el temporizador y verifica se se ha agota"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Tiempo en seg
        self.time_left = self.time_limit - elapsed_time
        
        
        print(f"Time left: {self.time_left}")  # Verifica el tiempo restante
        
        
        if self.time_left <= 0:
            self.lose_life()
            self.reset_timer()
        
    def reset_timer(self):
        """Reinicia el temporizador"""
        self.time_left = self.time_limit
        self.start_time = pygame.time.get_ticks()
        
                
    def show_start_game(self):
        """Muestra el texto 'start game' antes de iniciar el juego"""
        start_surface = self.font.render('Start Game', True, (255, 0, 0))
        
        self.DISPLAY.blit(start_surface, (self.DISPLAY.get_width() // 2 - start_surface.get_width() // 2, self.DISPLAY.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000) # 3 seg
    
    def load_sounds(self):
        """Carga la musica"""
        pygame.mixer.music.load("assets/music/sounds/MainTheme.ogg")
        pygame.mixer.music.play(-1)
        
        self.hop_sound = pygame.mixer.Sound("assets/music/sounds/Hop.ogg")
        self.drown_sound = pygame.mixer.Sound("assets/music/sounds/Drown.ogg")
        self.die_land_sound = pygame.mixer.Sound("assets/music/sounds/Die-on-Land.ogg")
        self.success_sound = pygame.mixer.Sound("assets/music/sounds/credit.ogg")
    
    def assetSetup(self):
        """
        Configura los objectos iniciales, incluyendo el fondo, el pasto y los autos
        """
        
        #Fondo/Background
        Object((0,0), (672, 768), "assets/background.png", self.object_group)
        
        # Pasto seguro(Agregamos huecos)
        #FIX 
        #for x in range(0, 572, 128): #Creamos huecos con separacion
            #SafeZone((x, 48), (48, 48), "assets/grass/green.png", self.object_group, self)
        def assetSetup(self):
            for x in range(0, 384, 48):
                SafeZone((x, 48), (48, 48), "assets/grass/green.png", self.object_group, self)



        
        
        #Pasto/grass zonas donde la rana esta segura
        for x in range(14):
            Object((x*48, 384), (48, 48), "assets/grass/purple.png", self.object_group)
            Object((x*48, 672), (48, 48), "assets/grass/purple.png", self.object_group)
        
        
        
        #Pasto/grass ubicado en el area superior
        for x in range(28):
            Object((x*24, 72), (24, 72), "assets/grass/green.png", self.object_group)
            
        #Valocidades aleatorias para los autos y rio
        speeds = [-2.25, -2, -1.75, -1.5, -1.25, 1.25, 1.5, 1.75, 2, 2.25]
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
        #self.frog = Frog((336, 672), (48, 48), "assets/froggy/up.png", self.frog_group, [self.car_group, self.river_group], self.river_speeds, self)
        self.frog = Frog((336, 672), (48, 48), "assets/froggy/up.png", self.frog_group, [self.car_group, self.river_group], self.river_speeds, self)

    def displayHUD(self):
        """
        Muestra las vidas, el puntaje y el maximo en la pantalla"""
        for i in range(self.lives):
            self.DISPLAY.blit(self.lives_icon, (10 + i * 40, 730))  # Dibuja iconos de vida
        #print(f"Current score: {self.score}, High score: {self.high_score}") # Verificamos puntaje
        lives_surface = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        
        
        self.DISPLAY.blit(lives_surface, (10, 10))
        self.DISPLAY.blit(score_surface, (150,10))
        self.DISPLAY.blit(high_score_surface, (450, 10))
        
     
    
    
    
    def run(self):
        """Bucle principal del juego, maneja los eventos de entrada, actualiza los objetos y refresca la pantalla"""
        self.DISPLAY.fill((0, 0, 0))
        self.show_start_game() # mostrar texto al iniciar el juego
        
        
        
        while True:
            #Rellena la pantalla con el color de fondo
            self.DISPLAY.fill(self.screen_color)
            
            #Movimiento de la rana segun la tecla presionada
            self.frog.keyups = []
            
            self.update_timer()
            self.display_timer()
            
            
            
            
        
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
                    if isinstance(sprite, SafeZone):
                        sprite.check_frog(self.frog) #Verifica si la rana ha entrado
                group.draw(self.DISPLAY)
            
            #Mostrar HUD
            self.displayHUD()
            
            
            #Refresa la pantalla con nuevos dibujos
            pygame.display.update()
            
    
    def lose_life(self):
        """Reduce las vidas y reinicia la posicion de la rana"""
        self.lives -= 1
        print(f"Lives left: {self.lives}")
        if self.lives == 0:
            self.game_over()
        else:
            self.frog.reset_position()
            self.reset_timer()
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
        self.display_game_over_message()
        pygame.time.wait(3000) # 3 seg
        self.lives += 3
        self.score = 0
        self.frog.reset_position()
        
    def display_game_over_message(self):
        """Muestra el mensaje 'game over' """
        game_over_surface = self.font.render("Game Over", True, (255, 0, 0))
        self.DISPLAY.blit(game_over_surface, (280, 350))
        pygame.display.update()



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
    
    menu = Menu.play_video_opencv("assets/video/test_intro.mp4", screen)
    
    #una vez finalizado el video, inicializa el juego
    game = Game(screen_dimensions, screen_caption, screen_color)
    
    #llama al menu de opciones
    menu = Menu(game.DISPLAY)
    menu.run()
    
    #comienzo del juego
    game.run()
    
    
    
    """
    game = Game((672, 768), "Frogger en python!", (0,0,0)) # Pantalla de 14x16 bloques, (48 px por bloque)
    menu = Menu(game.DISPLAY)
    menu.play_video("assets/video/videoo.mp4")
    menu.run()
    #llamamos al metodo de la clase Game para correr el juego
    game.run()"""
    
    
    
    