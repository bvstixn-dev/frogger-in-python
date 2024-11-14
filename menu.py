import pygame, cv2, sys, time, config, json
import numpy as np
from main import Game


class Menu:
    def __init__(self, screen):
        self.screen = screen
        
        
        #Cargar fondo del menu
        self.bg_image = pygame.image.load("assets/background.png")#ruta del fondo
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())#Escalar imagen
        
        #Cargar logo de frogger
        self.logo_image = pygame.image.load("assets/frogger_title.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (400, 150)) #Escalar imagen/logo
        
        #Cargar sonido
        self.select_sound = pygame.mixer.Sound("assets/music/sounds/select_sound.wav")
        self.push_start_sound = pygame.mixer.Sound("assets/music/sounds/push_start_sound.wav")
        
        #Fuentes para el menu
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
        #Opciones del menu
        self.options = ["Jugar", "Skins", "Opciones", "Salir"]
        self.selected_option = 0
        

        
        #Cargar prototipo de skin
        self.skins_image = pygame.image.load("assets/wireframes_skins.png")
        self.skins_image = pygame.transform.scale(self.skins_image, (400, 300))
        
        #rectangulo para el boton x (cierre)
        self.button_size = 40
        self.close_button_rect = pygame.Rect(600, 20, self.button_size, self.button_size)
        
        
        self.showing_skins = False
        self.showing_options = False
        
        
        self.config = config.load_settings()
        #variable de volumen
        self.level_volume = int(self.config.get("volume", 5) * 10)
        
        self.skins = ["default", "red", "purple", "yellow", "orange", "white", "blue"]
        self.current_skin = 0
        
        self.config = self.load_settings()
        self.option_index = 0
        
        
    
    def load_settings(self):
        # Cargar configuración desde JSON
        try:
            with open("config.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"volume": 0.2, "skin": "default", "score": 0}
    
    def save_settings(self):
        # Guardar configuración en JSON
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=4)
        
           
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
    
    def display_skins(self):
         # Dibujar fondo blanco
        self.screen.fill((255, 255, 255))
        
        # Título de "Cambiar Skin"
        title_text = self.font.render("Cambiar Skin", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Mostrar la imagen de la skin seleccionada
        skin_image = pygame.image.load(f"assets/froggy/{self.skins[self.current_skin]}/up.png")
        skin_image = pygame.transform.scale(skin_image, (200, 200))
        self.screen.blit(skin_image, (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 100))
        
        # Mostrar botón "X"
        pygame.draw.rect(self.screen, (255, 0, 0), self.close_button_rect)
        close_font = pygame.font.Font(None, 40)
        close_text = close_font.render('X', True, (255, 255, 255))
        self.screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y))
        
        # Mostrar las opciones de navegación
        nav_text = self.font.render("Usa izquierda/derecha", True, (0, 0, 0))
        nav_rect = nav_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(nav_text, nav_rect)

        pygame.display.flip()
    
    def display_options(self):
        
        self.screen.fill((50, 50, 50))
        font = self.font

        # Título opciones
        option_text = font.render("Presiona ESC para volver", True, (255, 255, 255))
        text_rect = option_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(option_text, text_rect)

        # Barra de volumen
        volume_text = font.render("Volumen: ", True, (255, 255, 255) if self.option_index == 0 else (150, 150, 150))
        volume_rect = volume_text.get_rect(center=(self.screen.get_width() // 2 - 85, 205))
        self.screen.blit(volume_text, volume_rect)

        # Dibujar la barra de volumen
        for i in range(11):
            color = (255, 255, 255) if i <= self.level_volume else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (self.screen.get_width() // 2 + i * 20, 190, 15, 30))

        # Opción de resetear score
        reset_text = font.render("Resetear Score", True, (255, 255, 255) if self.option_index == 1 else (150, 150, 150))
        reset_rect = reset_text.get_rect(center=(self.screen.get_width() // 2, 300))
        self.screen.blit(reset_text, reset_rect)

        pygame.display.update()
        
    def save_config(self, reset_score=False):
        """
        Guarda la configuración en config.json.
        Si reset_score es True, se reinicia solo el score; si no, se guarda solo el volumen actual.
        """
        # Cargar configuración actual
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        
        # Actualizar la configuración según sea necesario
        if reset_score:
            config["score"] = 0
            print("Score reseteado")  # Verificación en consola
        else:
            config["volume"] = self.level_volume / 10
            print(f"Configuración de volumen guardada: {self.level_volume / 10}")  # Verificación en consola
        
        # Guardar los cambios en config.json
        with open("config.json", "w") as config_file:
            json.dump(config, config_file)
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.option_index = (self.option_index + 1) % 2
            elif event.key == pygame.K_UP:
                self.option_index = (self.option_index - 1) % 2
            elif event.key == pygame.K_RETURN:
                if self.option_index == 1:  # Si estamos en la opción de "Resetear Score"
                    self.save_config(reset_score=True)
            # Cambiar el volumen solo si está seleccionada la opción de volumen
            if self.option_index == 0:
                if event.key == pygame.K_RIGHT and self.level_volume < 10:
                    self.level_volume += 1
                elif event.key == pygame.K_LEFT and self.level_volume > 0:
                    self.level_volume -= 1

        
    
    def run(self):
        while True:
            
            
            if self.showing_skins:
                self.display_skins()  # Mostrar pantalla de skins (como tienes implementado)
            elif self.showing_options:
                self.display_options()  # Mostrar pantalla de opciones
            else:
                self.display_menu()  # Mostrar menú principal
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.showing_skins and not self.showing_options:
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
                                #Skin
                                self.showing_skins = True
                            elif self.selected_option == 2:
                                #Opciones
                                self.showing_options = True
                            elif self.selected_option == 3:
                                pygame.quit()
                                sys.exit()
                #Opciones
                elif self.showing_options:
                    # Llama a handle_input para manejar los eventos dentro de la pantalla de opciones
                    self.handle_input(event)

                    # Salir de opciones con ESC y guardar solo el volumen
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.showing_options = False
                        self.save_config()  # Guardar solo el volumen al salir
                
                elif self.showing_skins:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.showing_skins = False
                            self.config["skin"] = self.skins[self.current_skin]  # Guardar skin seleccionada en el config
                            self.save_settings()  # Guardar cambios
                        elif event.key == pygame.K_LEFT:
                            self.current_skin = (self.current_skin - 1) % len(self.skins)  # Cambiar a la skin anterior
                        elif event.key == pygame.K_RIGHT:
                            self.current_skin = (self.current_skin + 1) % len(self.skins)  # Cambiar a la siguiente skin
                else:
                    # Interacción con la pantalla de prototipo o skins
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.close_button_rect.collidepoint(event.pos):
                            self.showing_skins = False
                    elif event.type == pygame.KEYDOWN:
                       
                        if event.key == pygame.K_ESCAPE:
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