import pygame
import os
import random

pygame.init()
ancho = 800
alto = 600
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Cat, run!")

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def disparo(self):
        bala = disparos(self.rect.right, self.rect.centery)
        balas.add(bala)
      
class disparos(pygame.sprite.Sprite):
    def __init__(self, centerx, top):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("disparo.png").convert(), (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.top = top
        self.speed = 25  # Velocidad de la bala

    def update(self, jugador_rect):
        self.rect.x += self.speed
        self.rect.top = jugador_rect.centery  # Actualizar la posición vertical según el jugador
        if self.rect.right > ancho:  # Eliminar la bala cuando sale de la pantalla
            self.kill()


class game:
  # Música de fondo
  pygame.mixer.music.load("musica.mpeg")
  pygame.mixer.music.play(-1)
  # Logo del juego
  logo = pygame.image.load("logo.png")
  pygame.display.set_icon(logo)
  
  def __init__(self,ancho,alto):
    self.ancho=800
    self.alto=600
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

        
balas=pygame.sprite.Group()
jugadores=pygame.sprite.Group()



# Música de fondo
pygame.mixer.music.load("musica.mpeg")
pygame.mixer.music.play(-1)

# Logo del juego
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)


jugador_imagen = pygame.image.load("salta.png").convert_alpha()
jugador = Jugador(50, 300, jugador_imagen)
jugadores.add(jugador)
obstacle_image = pygame.image.load(os.path.join("obs1.png")).convert_alpha()
misil_image = pygame.image.load(os.path.join("misil.png")).convert_alpha()
background_image = pygame.image.load(os.path.join("fondo1.png")).convert_alpha()
game_over_image = pygame.image.load(os.path.join("1258544.jpg"))
moneda_image = pygame.image.load(os.path.join("moneda.png")).convert_alpha()
sonido_abajo = pygame.image.load(os.path.join("bajar.png")).convert_alpha()
sonido_mute = pygame.image.load(os.path.join("apagado.png")).convert_alpha()
sonido_subir = pygame.image.load(os.path.join("subir.png")).convert_alpha()
imagen_linea = pygame.image.load("waos.png").convert_alpha()
monedas = []
obstaculos = []
misiles = []  
obstaculos_linea = []
GENERAR_MONEDAS_EVENTO = pygame.USEREVENT + 1
GENERAR_OBSTACULO_EVENTO = pygame.USEREVENT + 2
GENERAR_MISIL_EVENTO = pygame.USEREVENT + 3  
GENERAR_LINEA_EVENTO = pygame.USEREVENT + 4

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

def generar_obstaculo():
    y = random.choice(y_positions)
    x = 800
    return pygame.Rect(x, y, obstacle_image.get_width(), obstacle_image.get_height())

def generar_misil(y):
    x = 800
    return pygame.Rect(x, y, misil_image.get_width(), misil_image.get_height())

def generar_obstaculo_linea():
    y = random.randint(100, 500)
    x1 = 800
    x2 = x1 + random.randint(50, 200)
    return pygame.Rect(x1, y, x2 - x1, 10)

pygame.time.set_timer(GENERAR_MONEDAS_EVENTO, random.randint(3200, 6000))
pygame.time.set_timer(GENERAR_OBSTACULO_EVENTO, random.randint(5000, 10000))
pygame.time.set_timer(GENERAR_MISIL_EVENTO, random.randint(10000, 20000))
pygame.time.set_timer(GENERAR_LINEA_EVENTO, random.randint(3000, 7000))


y_positions = [random.randint(100, 500) for _ in range(10)]

jetpack_x = 50
jetpack_y = 300
jetpack_width = jugador_imagen.get_width()
jetpack_height = jugador_imagen.get_height()

scaled_image = pygame.transform.scale(background_image, (800, 600))
scaled_image2 = pygame.transform.scale(game_over_image, (800, 600))

clock = pygame.time.Clock()
score = 0
running = True
fondo_x = 0
fondo_velocidad = 8
gravity = 6


def pantalla():
    global fondo_x, running
    fondo_avanza = fondo_x % background_image.get_rect().width
    screen.blit(background_image, (fondo_avanza - background_image.get_rect().width, 0))
    if fondo_avanza < ancho:
        screen.blit(background_image, (fondo_avanza, 0))
    fondo_x -= fondo_velocidad

    for moneda_rect in monedas:
        moneda_rect.x -= fondo_velocidad
        screen.blit(moneda_image, moneda_rect)

    for obstaculo_rect in obstaculos:
        obstaculo_rect.x -= fondo_velocidad
        screen.blit(obstacle_image, obstaculo_rect)

        if (
            jetpack_x < obstaculo_rect.x + obstaculo_rect.width - 10
            and jetpack_x + jetpack_width - 10 > obstaculo_rect.x
            and jetpack_y < obstaculo_rect.y + obstaculo_rect.height - 10
            and jetpack_y + jetpack_height - 10 > obstaculo_rect.y
        ):
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    for obstaculo_rect, _ in obstaculos_linea:
        obstaculo_rect.x -= fondo_velocidad
        x, y, width, height = obstaculo_rect
        # Dibuja la línea roja
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, width, height))

        if (
            jetpack_x < x + width - 10
            and jetpack_x + jetpack_width - 10 > x
            and jetpack_y < y + height - 10
            and jetpack_y + jetpack_height - 10 > y
        ):
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    for misil_rect in misiles:
        misil_rect.x -= fondo_velocidad + 5
        screen.blit(misil_image, misil_rect)

    screen.blit(jugador_imagen, (jetpack_x, jetpack_y))

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GENERAR_MONEDAS_EVENTO:
            monedas.extend(generar_fila_de_monedas(y_positions[random.randint(0, 9)]))
        elif event.type == GENERAR_OBSTACULO_EVENTO:
            y = random.choice([pos for pos in y_positions if pos not in [moneda_rect.y for moneda_rect in monedas]])
            y = max(100, min(y, 500))  # Asegura que la posición y esté dentro de los límites
            obstaculos.append(generar_obstaculo())
        elif event.type == GENERAR_MISIL_EVENTO:
            y = random.choice([pos for pos in y_positions if pos not in [moneda_rect.y for moneda_rect in monedas]])
            misiles.append(generar_misil(y))
        elif event.type == GENERAR_LINEA_EVENTO:
            obstaculo_rect = generar_obstaculo_linea()
            obstaculos_linea.append((obstaculo_rect, imagen_linea))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jetpack_x > 0:
        jetpack_x -= 5
    if keys[pygame.K_RIGHT] and jetpack_x < 700 - jetpack_width:
        jetpack_x += 5
    if keys[pygame.K_UP] and jetpack_y > 0:
        jetpack_y -= 13
    
    # Volumen baja
    if keys[pygame.K_o] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
        screen.blit(sonido_abajo, (100, 87))
    elif keys[pygame.K_o] and pygame.mixer.music.get_volume() == 0.0:
        screen.blit(sonido_mute, (100, 87))
    
    # Volumen sube
    if keys[pygame.K_p] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
        screen.blit(sonido_subir, (100, 87))
    # Desactivar volumen 
    elif keys[pygame.K_i]:
        pygame.mixer.music.set_volume(0.0)
        screen.blit(sonido_mute, (100, 87))
    if keys[pygame.K_m]:
        jugador.disparo()

    if jetpack_y < 600 - jetpack_height:
        jetpack_y += gravity

    screen.blit(scaled_image, (0, 0))

    for moneda_rect in monedas:
        moneda_rect.x -= fondo_velocidad
        screen.blit(moneda_image, moneda_rect)

    for obstaculo_rect, imagen_linea in obstaculos_linea:
        obstaculo_rect.x -= fondo_velocidad
        screen.blit(imagen_linea, obstaculo_rect.topleft)

        if (
            jetpack_x < obstaculo_rect.x + obstaculo_rect.width - 10
            and jetpack_x + jetpack_width - 10 > obstaculo_rect.x
            and jetpack_y < obstaculo_rect.y + obstaculo_rect.height - 10
            and jetpack_y + jetpack_height - 10 > obstaculo_rect.y
        ):
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    for misil_rect in misiles:
        misil_rect.x -= fondo_velocidad + 5  # Ajusta la velocidad de los misiles
        screen.blit(misil_image, misil_rect)

    # Verificar colisiones con las monedas
    for moneda_rect in monedas:
        if jetpack_x < moneda_rect.x < jetpack_x + jetpack_width and jetpack_y < moneda_rect.y < jetpack_y + jetpack_height:
            monedas.remove(moneda_rect)
            score += 1

    # Verificar colisiones con los misiles
    for misil_rect in misiles:
        if jetpack_x < misil_rect.x < jetpack_x + jetpack_width and jetpack_y < misil_rect.y < jetpack_y + jetpack_height:
            screen.blit(scaled_image2, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    # Eliminar misiles que salieron de la pantalla
    misiles = [misil for misil in misiles if misil.x > -misil.width]
    pantalla()
    dibujar_texto(screen, str(score),25 ,70,10)
    screen.blit(moneda_image,(25,9))
    balas.update(jugador.rect)
    balas.draw(screen)
    pygame.display.flip()


pygame.quit()