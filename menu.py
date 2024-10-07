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
        
