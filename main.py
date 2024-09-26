import pygame
import constantes

from personajes import Personaje


pygame.init()

jugador = Personaje(400, 550)

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

pygame.display.set_caption("Frogger in python")





run = True

while run:
    
    #dibujar personaje
    jugador.dibujar(ventana)
    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


pygame.quit()