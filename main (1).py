import pygame
import os
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Jetpack Joyride")

moneda_image1 = pygame.image.load(os.path.join('moneda.png')).convert_alpha()
jetpack_image = pygame.image.load(os.path.join('boy.png')).convert_alpha()
obstacle_image = pygame.image.load(os.path.join('jetpack_2-removebg-preview (1).png')).convert_alpha()
background_image = pygame.image.load(os.path.join('B21rglpIUAEAa4Z.jpg')).convert_alpha()
game_over_image = pygame.image.load(os.path.join('1258544.jpg')).convert_alpha()
moneda_image = pygame.image.load(os.path.join('moneda.png')).convert_alpha()

monedas = [] 
obstaculos = [] 
GENERAR_MONEDAS_EVENTO = pygame.USEREVENT + 1
GENERAR_OBSTACULO_EVENTO = pygame.USEREVENT + 2

def dibujar_texto (surface, text, size,x,y):
    font= pygame.font.SysFont("serif",size)
    text_surface= font.render(text, True, [255,255,255])
    text_rect= text_surface.get_rect()
    text_rect.midtop=(x,y)
    surface.blit(text_surface,text_rect)

def generar_fila_de_monedas(y):
    fila_de_monedas = []
    for i in range(random.randint(5, 10)):
        x = 800 + i * moneda_image.get_width()  # Coloca las monedas en una fila
        fila_de_monedas.append(pygame.Rect(x, y, moneda_image.get_width(), moneda_image.get_height()))
    return fila_de_monedas

def generar_obstaculo(y):
    x = 800  
    return pygame.Rect(x, y, obstacle_image.get_width(), obstacle_image.get_height())

pygame.time.set_timer(GENERAR_MONEDAS_EVENTO, random.randint(4000, 8000))  # Generar evento cada 4 a 8 segundos para las monedas
pygame.time.set_timer(GENERAR_OBSTACULO_EVENTO, random.randint(8000, 15000))  # Generar evento cada 10 a 15 segundos para el obstáculo

y_positions = [random.randint(100, 500) for _ in range(5)]  # Lista de posiciones en Y para las filas de monedas
monedas.extend(generar_fila_de_monedas(y_positions[0]))  # Genera la primera fila de monedas

jetpack_x = 50
jetpack_y = 300
jetpack_width = jetpack_image.get_width()
jetpack_height = jetpack_image.get_height()

scaled_image = pygame.transform.scale(background_image, (800, 600))
scaled_image2 = pygame.transform.scale(game_over_image, (800, 600))

screen.blit(scaled_image, (0, 0))

clock = pygame.time.Clock()
score = 0
running = True

gravity = 6  

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GENERAR_MONEDAS_EVENTO:
            monedas.extend(generar_fila_de_monedas(y_positions[random.randint(0, 4)]))
        elif event.type == GENERAR_OBSTACULO_EVENTO:
            y = random.choice([pos for pos in y_positions if pos not in [moneda_rect.y for moneda_rect in monedas]])
            obstaculos.append(generar_obstaculo(y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jetpack_x > 0:
        jetpack_x -= 5
    if keys[pygame.K_RIGHT] and jetpack_x < 700 - jetpack_width:
        jetpack_x += 5
    if keys[pygame.K_UP] and jetpack_y > 0:
        jetpack_y -= 13

    if jetpack_y < 600 - jetpack_height:
        jetpack_y += gravity

    screen.blit(scaled_image, (0, 0))

    for moneda_rect in monedas:
        moneda_rect.x -= 5
        screen.blit(moneda_image, moneda_rect)

    for obstaculo_rect in obstaculos:
        obstaculo_rect.x -= 5
        screen.blit(obstacle_image, obstaculo_rect)

    screen.blit(jetpack_image, (jetpack_x, jetpack_y))

    for moneda_rect in monedas:
        if jetpack_x < moneda_rect.x < jetpack_x + jetpack_width and jetpack_y < moneda_rect.y < jetpack_y + jetpack_height:
            monedas.remove(moneda_rect)
            score += 1

    for obstaculo_rect in obstaculos:
        if jetpack_x < obstaculo_rect.x < jetpack_x + jetpack_width and jetpack_y < obstaculo_rect.y < jetpack_y + jetpack_height:
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
    
    dibujar_texto(screen, str(score),25 ,70,10)
    screen.blit(moneda_image1,(25,9))
    
    pygame.display.flip()

pygame.quit()
