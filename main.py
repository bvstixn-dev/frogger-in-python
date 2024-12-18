import pygame, sys, random, config, json
from object import *
from frog import *
from lane import *
from menu import *



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
        self.lives = 7
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 25)
        
        
        #Configuracion inicial de los objetos del juego
        
        
        #cordenada de los huecos
        self.holes = [(26, 96),(174, 96),(322, 96),(468, 96),(606, 96)]
        
        self.occupied_holes = []
        
        self.max_holes = 5
        
        self.level = 1
        
        with open('config.json') as f:
            config = json.load(f)
        self.skin = config.get("skin", "default")
        self.warning_sound_played = False
        
        self.volume = config.get("volume", 0.2)
        #Cargamos el sonido
        self.load_sounds()
        self.assetSetup()
        
    def run(self):
        """Bucle principal del juego, maneja los eventos de entrada, actualiza los objetos y refresca la pantalla"""
        self.DISPLAY.fill((0, 0, 0))
        self.show_start_game() #Funcion paramostrar texto al iniciar el juego
        
        self.frog.change_skin(self.skin)
        while True:
            #Rellena la pantalla con el color de fondo
            self.DISPLAY.fill(self.screen_color)
            
            #Movimiento de la rana segun la tecla presionada
            self.frog.keydowns = []
            
            #Manejo de eventos (cerrar ventana, teclas presionadas)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    
                    self.frog.keydowns.append(event.key) # Almacena las teclas que se sueltan
            
            #Actualiza y dibuja todos los grupos de sprites
            for group in self.all_group:
                for sprite in group:
                    sprite.update()
                group.draw(self.DISPLAY)
            
            
            clock = pygame.time.Clock()
            fps = 60
            clock.tick(fps)
            #Mostrar HUD
            self.displayHUD()
            self.update_timer()
            self.draw_time_bar()
            
            #Refresa la pantalla con nuevos dibujos
            pygame.display.update()
        
    
    def load_sounds(self):
        """Carga la musica"""
        pygame.mixer.music.load("assets/music/sounds/MainTheme.ogg")
        pygame.mixer.music.play(-1) #La musica se repite en bucle
        pygame.mixer.music.set_volume(self.volume)

        
        self.hop_sound = pygame.mixer.Sound("assets/music/sounds/Hop.ogg")
        self.hop_sound.set_volume(self.volume)
        self.drown_sound = pygame.mixer.Sound("assets/music/sounds/Drown.ogg")
        self.drown_sound.set_volume(self.volume)
        self.die_land_sound = pygame.mixer.Sound("assets/music/sounds/Die-on-Land.ogg")
        self.die_land_sound.set_volume(self.volume)
        self.success_sound = pygame.mixer.Sound("assets/music/sounds/credit.ogg")
        self.success_sound.set_volume(self.volume)
        self.fail_sound = pygame.mixer.Sound("assets/music/sounds/fail_sound.ogg")
        self.fail_sound.set_volume(self.volume)
        self.warning_sound = pygame.mixer.Sound("assets/music/sounds/warning_sound.ogg")
        self.warning_sound.set_volume(self.volume)
    
    def reset_holes(self):
        #Limpiar huecos ocupados
        self.occupied_holes.clear() 
        #actualiza la pantalla
        self.reset_holes_graphics() 
        
    def reset_holes_graphics(self):
        for hole in self.holes:
            for obj in self.object_group:  
                if isinstance(obj, Object) and obj.position == hole:  #Compreba si el objeto es la rana y está en el hueco
                    self.object_group.remove(obj)  # Eliminar el sprite de la rana
                    break  # Salir del bucle después de eliminar la rana en el hueco
    
    def show_time_message(self):
        #configurar fuente y tamano
        font = self.font
        
        texto = f"Time {self.level}"
        
        texto = font.render(texto, True, (255, 0 ,0)) #rojo
        
        text_rect = texto.get_rect(center=(self.DISPLAY.get_width() // 2, self.DISPLAY.get_height() //2))
        
        self.DISPLAY.blit(texto, text_rect)
        
        pygame.display.update()
        
        pygame.time.delay(1000)
    
    def check_if_in_hole(self):
        "Checkea si la rana llego en un hueco, en ese caso, dibuja una rana en el hueco"
        
        frog_rect = self.frog.rect #cuadrado de la rana para la colision
        
        for hole_pos in self.holes:
            #Se crea un cuadrado de colision para el hueco
            hole_rect = pygame.Rect(hole_pos[0], hole_pos[1], self.frog.size[0], self.frog.size[1])
            #Comprobamos si la rana colisiona en algun hueco
            if frog_rect.colliderect(hole_rect):
                if hole_pos not in self.occupied_holes: #Verifica si esta ocupado el hueco
                        
                    #Dibuja una rana en el hueco
                    Object(hole_pos, self.frog.size, "assets/grass/ranita.png", self.object_group)
                    
                    #Sonido de completado
                    pygame.mixer.Sound.play(self.success_sound)
                    
                    #mensaje en el centro de la pantalla
                    self.show_time_message()
                    
                    #Incremento de score
                    self.increase_score(100)
                    
                    
                    self.level += 1
                    
                    #Marcar como ocupado
                    self.occupied_holes.append(hole_pos)
                    if len(self.occupied_holes) >= self.max_holes:
                        self.reset_holes()  # Reiniciar los huecos
                        self.reset_holes_graphics()  # Limpiar gráficos de los huecos
                    
                    
                    #reinicio de contador
                    self.reset_timer()
                    
                    #reinicio de posicion
                    self.frog.reset_position()
                else:
                    self.frog.killFrog()
                    self.lose_life()
                    pygame.mixer.Sound.play(self.fail_sound)
                    print("Testeo de perder vida")
                    break
                
                
            
    
    
    def increase_live(self):
        self.lives + 1
    
    def adjust_speed(self):
        """
        Ajusta las velocidades de los obstáculos en función del nivel, añadiendo una variación aleatoria.
        """
        base_speeds = [-1.5, -1.2, -1.0, -0.8, -0.6, 4.0, 4.5, 5.0, 5.5, 6.0]
        speed_multiplier = 1 + (self.level * 0.5)  # Incremento gradual con el nivel
        random.shuffle(base_speeds)  # Desordena para variación aleatoria
        print(base_speeds)
        return [speed * speed_multiplier for speed in base_speeds]
    
    def assetSetup(self, level=1):
        """
        Configura los objectos iniciales, incluyendo el fondo, el pasto y los autos
        """
        
         # Obtiene velocidades ajustadas para los obstáculos
        speeds = self.adjust_speed()
        
        print(speeds)
        #Fondo/Background
        Object((0,0), (672, 768), "assets/background.png", self.object_group)
        
        
        #Pasto/grass zonas donde la rana esta segura
        for x in range(14):
            Object((x*48, 384), (48, 48), "assets/grass/purple.png", self.object_group)
            Object((x*48, 672), (48, 48), "assets/grass/purple.png", self.object_group)
        
        #Hueco
        Object((0, 72), (100, 72), "assets/grass/hueco.png", self.object_group) 
        #pasto
        Object((100, 72), (24, 72), "assets/grass/green.png", self.object_group)
        Object((124, 72), (24, 72), "assets/grass/green.png", self.object_group)
        
        #Hueco
        Object((148, 72), (100, 72), "assets/grass/hueco.png", self.object_group)
        #Pasto
        Object((248, 72), (24, 72), "assets/grass/green.png", self.object_group)
        Object((272, 72), (24, 72), "assets/grass/green.png", self.object_group)
        
        #Hueco
        Object((296, 72), (100, 72), "assets/grass/hueco.png", self.object_group)
        #Pasto
        Object((396, 72), (24, 72), "assets/grass/green.png", self.object_group)
        Object((420, 72), (24, 72), "assets/grass/green.png", self.object_group)
        
        #Hueco
        Object((444, 72), (100, 72), "assets/grass/hueco.png", self.object_group)
        #Pasto
        Object((544, 72), (24, 72), "assets/grass/green.png", self.object_group)
        Object((568, 72), (24, 72), "assets/grass/green.png", self.object_group)
        #Hueco
        Object((592, 72), (80, 72), "assets/grass/hueco.png", self.object_group)  
        
        #Carriles del rio
        for y in range(5):
            y_pos = y*48 + 144
            speed = speeds.pop() 
            #Objeto del carril
            new_lane = Lane((0, y_pos), self.river_group, speed, "river")
            self.river_speeds[y_pos // 48] = new_lane.speed
            
            
        
        
        #Carriles de la calle
        for y in range(5):
            y_pos = y*48 + 432
            speed = speeds.pop() 
            
            
            Lane((0, y_pos), self.car_group, speed, "street")
        
        #Inicializamos la rana frogger(posicion inicial(2 argumentos), su tamano, su imagen, su agrupacion de sprites y colisiones
        self.frog = Frog((312, 672), (48, 48), "default", self.frog_group, [self.car_group, self.river_group], self.river_speeds, self)
    
    
    def draw_time_bar(self):
        # Calcular el porcentaje del tiempo restante
        time_ratio = max(0, self.time_left / self.time_limit)  # Aseguramos que nunca sea negativo

        #Dimensiones de la barra de tiempo
        width = 300  
        height = 20  
        #Ancho de la barra basado en el tiempo restante
        current_width = int(width * time_ratio)
        # Posición de la barra (inferior de la pantalla)
        x_pos = self.DISPLAY.get_width() - width - 70  #10 px de margen desde la derecha
        y_pos = self.DISPLAY.get_height() - height - 10  #10 px de margen desde el fondo

        if self.time_left <= 10:
            bar_color = (255, 0, 0)
            if not self.warning_sound_played:
                pygame.mixer.Sound.play(self.warning_sound)  # Reemplaza con tu objeto de sonido
                self.warning_sound_played = True  # Marca que el sonido se ha reproducido
                
        else:
            bar_color = (0, 255, 0)
            self.warning_sound_played = False  # Restablece la variable cuando se sale de la condición
            
        # Dibujar la parte restante de la barra (en verde)
        pygame.draw.rect(self.DISPLAY, bar_color, (x_pos + (width - current_width), y_pos, current_width, height))
        
        #Cargar y reescalar el icono
        time_icon = pygame.image.load("assets/icons/time.png")
        time_icon = pygame.transform.scale(time_icon, (55, 20))
        
        #Dibujar en pantalla
        self.DISPLAY.blit(time_icon, (x_pos + 305, y_pos ))
        
    def update_timer(self):
        
        """Actualiza el contador, una vez que finalice, la rana pierde una vida"""
        #Calculo del tiempo
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Convertir a segundos
        self.time_left = self.time_limit - elapsed_time  # Calcular el tiempo restante

        if self.time_left <= 0:
            pygame.mixer.Sound.play(self.fail_sound)
            self.lose_life()  # Si el tiempo se acaba, perder una vida
            self.reset_timer()  # Reiniciar el temporizador
        
    def reset_timer(self):
        """Reinicia el temporizador"""
        #Ojo con esta linea, creo que es innecesaria
        self.time_left = self.time_limit
        self.start_time = pygame.time.get_ticks()
        
                
    def show_start_game(self):
        """Muestra el texto 'start game' antes de iniciar el juego"""
        #Creamos la variable con sus respectivos atributos
        start_surface = self.font.render('Start Game', True, (255, 0, 0))
        
        #Dibujamos en pantalla
        self.DISPLAY.blit(start_surface, (self.DISPLAY.get_width() // 2 - start_surface.get_width() // 2, self.DISPLAY.get_height() // 2))
        
        #Actualizamos el dibujo
        pygame.display.update()
        
        pygame.time.delay(1500) # 1.5 seg

    def displayHUD(self):
        """Muestra las vidas, el puntaje y el maximo en la pantalla"""
        for i in range(self.lives):
            self.DISPLAY.blit(self.lives_icon, (10 + i * 40, 730))  # Dibuja iconos de vida
        
        score_surface = self.font.render(f"1-UP", True, (255, 255, 255))
        score_num_surface = self.font.render(f"{str(self.score).zfill(5)}", True, (255, 0, 0))
        
        high_score_surface = self.font.render(f"HI-SCORE", True, (255, 255, 255))
        high_score_num_surface = self.font.render(f"{str(self.high_score).zfill(5)}", True, (255, 0, 0))
        
        #Dibujar hud (var, pos (x, y))
        self.DISPLAY.blit(score_surface, (100,10))
        self.DISPLAY.blit(score_num_surface, (80, 40))
        
        self.DISPLAY.blit(high_score_surface, (400, 10))
        self.DISPLAY.blit(high_score_num_surface, (455, 40))
        
        #DEBBUGING
        #print(f"Current score: {self.score}, High score: {self.high_score}") # Verificamos puntaje
        #lives_surface = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        #self.DISPLAY.blit(lives_surface, (10, 10))
        
        # Cargar configuración solo la primera vez
        if not hasattr(self, 'loaded_high_score'):
            self.load_config()
            self.loaded_high_score = True

        # Actualizar y guardar high score si se supera el actual
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def load_config(self):
        """Carga el high score y el volumen desde config.json."""
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.high_score = config.get("score", 0)
                self.level_volume = int(config.get("volume", 0.5) * 10)  # Cargar volumen inicial
        except FileNotFoundError:
            self.high_score = 0
            self.level_volume = 8  # Valores predeterminados si no existe el archivo
    def save_high_score(self):
        """Guarda el high score actual en config.json sin afectar otras configuraciones."""
        try:
            with open("config.json", "r+") as config_file:
                config = json.load(config_file)
                config["score"] = self.high_score  # Solo actualizar el high score
                config_file.seek(0)
                json.dump(config, config_file)
                config_file.truncate()  # Limpiar el contenido residual
            print(f"High score guardado: {self.high_score}")  # Mensaje de verificación
        except FileNotFoundError:
            # Si el archivo no existe, crear uno nuevo
            with open("config.json", "w") as config_file:
                json.dump({"score": self.high_score, "volume": self.level_volume / 10}, config_file)
            print("Archivo config.json creado y high score guardado.")
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
        #Si el puntaje es mayor que el record actual, se reasigna la variable
        if self.score > self.high_score:
            self.high_score = self.score
            
    
    def game_over(self):
        """Termina el juego y reinicia los valores """
        print("Game over")
        self.save_high_score()
        self.display_game_over_message()
        
        #Volvemos a incrementar las vidas y reiniciar el puntaje para comenzar de nuevo
        self.lives += 7
        self.score = 0
        self.frog.reset_position()
        pygame.time.wait(2000) #2seg
        
    def display_game_over_message(self):
        """Dibuja 'game over' en la pantalla"""
        game_over_surface = self.font.render("Game Over", True, (255, 0, 0))
        self.DISPLAY.blit(game_over_surface, (240, 397))
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
    config = config.load_settings()
    print("setting loaded: ", config)
    
    
    #Crea el menu y corre el juego
    
    menu = Menu.play_video_opencv("assets/video/test_intro.mp4",  screen)
    
    #una vez finalizado el video, inicializa el juego
    game = Game(screen_dimensions, screen_caption, screen_color)
    
    #llama al menu de opciones
    menu = Menu(game.DISPLAY)
    menu.run()
    
    #comienzo del juego
    game.run()
    
    
    
    