import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, size, image_directory, group=None):
        """
        Inicializa un objeto en el juego como un sprite
        -------------------------------------------------------------------
        Parametros:
        - pos: Posicion incial del objeto en la pantalla (x, y)
        - size: Tamano del objeto (ancho, alto)
        - image_directory: Ruta de la imagen
        - group: Grupo de sprites al que pertenece el objeto
        -------------------------------------------------------------------
        """
        super().__init__(group) #Hereda la clase de Sprites de pygame y su atributo group para inicializar el sprite
        
        self.pos = pos #Almacena la posicion del objeto
        self.size = size #Almacena el tamano del objeto
        self.image_directory = image_directory #Almacena la ruta de imagen
        
        
        
        
    def setImage(self):
        """
        Carga la imagen desde la ruta especificada, la escala del tamano del objeto y configura la superficie y el rectangulo del sprite
        """
        self.image = pygame.image.load(self.image_directory) #Carga la imagen
        self.image = pygame.transform.scale(self.image, self.size) #Escala de la imagen
        #Crea una superficie transparente para el objeto
        self.surf = pygame.Surface(self.size).convert_alpha() 
        self.surf.fill((0,0,0,0)) #LLena la superficie con transparencia
        self.rect = self.surf.get_rect(topleft = self.pos) #Establece el rectangulo en la posicion incial
        self.surf.blit(self.image, (0,0)) #Dibuja la imagen en la superficie
        
    def update(self):
        """
        Actualiza la imagen del objeto
        se llama en cada cuadre para asegurarse que la imagen se muestre correctamente
        """
        self.setImage() #Llama a setImage() para actualizar la imagen