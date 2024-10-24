import pygame, cv2, sys, time
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
        self.options = ["Jugar", "Multijugador", "Skins", "Opciones", "Salir"]
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
        #self.showing_prototipo = False
        self.showing_skins = False
        
        
        
        
        #Lobbies simulados
        self.lobbies = [("Jugador 1", "192.168.1.2"), ("Jugador 2", "192.168.1.3")]
        self.selected_lobby = 0
        
        #estado del menu
        self.showing_lobbies = False
        
        
    def display_lobbies(self):
        #Fondo blanco 
        self.screen.fill((255, 255, 255))
        
        #Dibujar titulo
        title_surface = self.font.render("Lobbies", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        
        #Dibujar lobbies simulados
        for i, lobby in enumerate(self.lobbies):
            color = (0, 0, 0) if i == self.selected_lobby else (100, 100, 100)
            lobby_text = f"{lobby[0]} {lobby[1]}"
            lobby_surface = self.font.render(lobby_text, True, color)
            lobby_rect = lobby_surface.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(lobby_surface, lobby_rect)
            
            #Dibujar caja negra 
            pygame.draw.rect(self.screen, (200, 200, 200), lobby_rect) # Gris claro para ver
            self.screen.blit(lobby_surface, lobby_rect)
            
        #Dibujar boton 'crear lobby'
        create_lobby_text = "Crear lobby"
        create_lobby_surface = self.font.render(create_lobby_text, True, (0, 0, 0))
        create_lobby_rect = create_lobby_surface.get_rect(center=(self.screen.get_width() // 2, 400))
        self.screen.blit(create_lobby_surface, create_lobby_rect)
        
        #dibujar x para salir
        pygame.draw.rect(self.screen, (255, 0 ,0), self.close_button_rect)
        close_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
        close_text = close_font.render("X", True, (255, 255, 255))
        self.screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y))
        
        pygame.display.flip()
        
        
        
    
    
    
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
    #def display_prototipo()
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
    
    def display_options(self):
        
        self.DISPLAY.fill((50, 50, 50))
        
        font = self.font
        option_text = font.render("Opciones - Presiona ESC para volver XD", True, (255, 255, 255))
        text_rect = option_text.get_rect(center=(self.DISPLAY.get_width() // 2, self.DISPLAY.get_heigh() // 2 - 100))
        self.DISPLAY.blit(option_text, text_rect)
        
        pygame.display.update()
    
    def run(self):
        while True:
            if not self.showing_lobbies and not self.showing_skins:
                self.display_menu()  # Mostrar menú principal
            elif self.showing_lobbies:
                self.display_lobbies()  # Mostrar pantalla de prototipo
            elif self.showing_skins:
                self.display_skins()  # Mostrar pantalla de skins
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.showing_lobbies and not self.showing_skins:
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
                                #Multijugador
                                self.showing_lobbies = True
                            elif self.selected_option == 2:
                                #Skin
                                self.showing_skins = True
                            elif self.selected_option == 3:
                                #Opciones
                                self.showing_options = True
                            elif self.selected_option == 4:
                                pygame.quit()
                                sys.exit()
                else:
                    # Interacción con la pantalla de prototipo o skins
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.close_button_rect.collidepoint(event.pos):
                            self.showing_lobbies = False
                            self.showing_skins = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            self.selected_lobby = (self.selected_lobby + 1) % len(self.lobbies)
                        elif event.key == pygame.K_UP:
                            self.selected_lobby = (self.selected_lobby - 1) % len(self.lobbies)
                        elif event.key == pygame.K_ESCAPE:
                            self.showing_lobbies = False
                        elif event.key == pygame.K_ESCAPE:
                            self.showing_prototipo = False
                            self.showing_skins = False
        
