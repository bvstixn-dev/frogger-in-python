import pygame
import constantes

from personajes import Personaje


#iniciar pygame
pygame.init()


#Configuracion de la ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("Frogger in python")

#sprites del juego

#animaciones = []
#for i in range (2):
 #   print(i)


player_image = pygame.image.load("assets/froggy/up.png")
player_image = pygame.transform.scale(player_image, (player_image.get_width()*constantes.SCALA_PERSONAJE,
                                                     player_image.get_height()*constantes.SCALA_PERSONAJE))

#definir variables de movimiento del jugador
push_arriba = False
push_abajo = False
push_izquieda = False
push_derecha = False
#Aparicion y ubicacion del jugador
jugador = Personaje(400, 550, player_image)
#Establecer un reloj para controlar los FPS
reloj = pygame.time.Clock()
#Obstaculo

    
#Bucle del juego
run = True
while run == True:
    ventana.fill(constantes.COLOR_BG)
    #que corra a 60 fps
    reloj.tick(constantes.FPS)
    #calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0
    
    if push_derecha == True:
        delta_x = constantes.VELOCIDAD
    if push_izquieda == True:
        delta_x = -constantes.VELOCIDAD
    if push_arriba == True:
        delta_y = -constantes.VELOCIDAD
    if push_abajo == True:
        delta_y = constantes.VELOCIDAD
    """
    if push_derecha:
        delta_x = constantes.VELOCIDAD
    elif push_izquieda:
        delta_x = -constantes.VELOCIDAD
    if push_arriba:
        delta_y = -constantes.VELOCIDAD
    elif push_abajo:
        delta_y = constantes.VELOCIDAD
    """
    #verificar ubicacion
    print(delta_x, delta_y)
    
    #mover al jugador
    jugador.movimiento(delta_x, delta_y)    
    
    #dibujar personaje
    jugador.dibujar(ventana)
    
    #comprobar colision
    obstaculo = pygame.Rect(300, 300, constantes.ANCHO_OBTACULO, constantes.ALTO_OBTACULO)
    pygame.draw.rect(ventana, (255, 0, 0), obstaculo)
    if jugador.shape.colliderect(obstaculo):
        print("!COLISION DETECTADA")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #controles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                #push_izquieda = True
                jugador.movimiento(-constantes.TAMANO_BLOQUE, 0)
                
            if event.key == pygame.K_d:
                #push_derecha = True
                jugador.movimiento(constantes.TAMANO_BLOQUE, 0)
            if event.key == pygame.K_w:
                #push_arriba = True
                jugador.movimiento(0, -constantes.TAMANO_BLOQUE)
            if event.key == pygame.K_s:
                #push_abajo = True
                jugador.movimiento(0, constantes.TAMANO_BLOQUE)
        #Soltar tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                push_izquieda = False
            if event.key == pygame.K_d:
                push_derecha = False
            if event.key == pygame.K_w:
                push_arriba = False
            if event.key == pygame.K_s:
                push_abajo = False
        
    #Actualizar eventos
    pygame.display.update()


pygame.quit()