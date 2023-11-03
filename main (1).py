import pygame
import os
import random
ANCHO=1280
LARGO=720
pygame.init()
screen = pygame.display.set_mode((ANCHO, LARGO))

pygame.display.set_caption("Jetpack Joyride")

jetpack_image = pygame.image.load(os.path.join('boy.png'))
obstacle_image = pygame.image.load(os.path.join('jetpack_2-removebg-preview (1).png'))
background_image = pygame.image.load(os.path.join('B21rglpIUAEAa4Z.jpg'))
game_over_image = pygame.image.load(os.path.join('1258544.jpg'))
PLAYER_X=50
PLAYER_Y=480
y_change=0
x_change=0
gravedad=1
obstacle_x = 800
obstacle_y = random.randint(100, 400)
obstacle_width = 100
obstacle_height = 100


scaled_image = pygame.transform.scale(background_image, (ANCHO, LARGO))
scaled_image2 = pygame.transform.scale(game_over_image, (ANCHO, LARGO))

screen.blit(scaled_image, (0, 0))

clock = pygame.time.Clock()
score = 0
running = True



while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_UP and y_change==0:
            y_change += 10
        elif event.key==pygame.K_DOWN:
            y_change -= 2
        elif event.key==pygame.K_LEFT:
            y_change -=1
        if event.key==pygame.K_RIGHT:
            y_change +=1
    if event.type==pygame.KEYUP:
        if event.key==pygame.K_RIGHT:
            y_change=0
        if event.key==pygame.K_LEFT:
            y_change=0
    

    screen.blit(scaled_image, (0, 0))

    obstacle_x -= 5
    if obstacle_x + obstacle_width < 0:
        obstacle_x = 800
        obstacle_y = random.randint(100, 500)

    if 0<=PLAYER_X<=430:
        PLAYER_X+=x_change
    if PLAYER_X<0:
        PLAYER_X=0
    if PLAYER_X>430:
        PLAYER_X=430

    if y_change > 0 or PLAYER_Y < 480:
        PLAYER_Y-=y_change
        y_change-=gravedad
    if PLAYER_Y>480:
        PLAYER_Y=480
    if PLAYER_Y==480  and y_change<0:
        y_change=0

    screen.blit(obstacle_image, (obstacle_x, obstacle_y))
    screen.blit(jetpack_image, (PLAYER_X, PLAYER_Y))

    if (y_change + jetpack_image.get_width() > obstacle_x and
        y_change < obstacle_x + obstacle_width and
        x_change + jetpack_image.get_height() > obstacle_y and
        x_change < obstacle_y + obstacle_height):
        screen.blit(scaled_image2, (0, 0))
        pygame.display.flip()

        pygame.time.delay(3000)
        running = False

    pygame.display.flip()


pygame.quit()
