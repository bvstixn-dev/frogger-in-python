import pygame
import constantes

from personajes import Personaje
pygame.init()

jugador = Personaje(400, 550)

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

pygame.display.set_caption("Frogger in python")

#definir variables de movimiento del jugador
push_arriba = False
push_abajo = False
push_izquieda = False
push_derecha = False




run = True

while run:
    
    #calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0
    
    if push_derecha == True:
        delta_x = 5
    if push_izquieda == True:
        delta_x = -5
    if push_arriba == True:
        delta_y = -5
    if push_abajo == True:
        delta_y = 5
    
    
    
    #dibujar personaje
    jugador.dibujar(ventana)
    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #controles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("Izquierda")
            if event.key == pygame.K_d:
                print("Derecha")
            if event.key == pygame.K_w:
                print("Arriba")
            if event.key == pygame.K_s:
                print("abajo")
        
        
        
        
    pygame.display.update()


pygame.quit()