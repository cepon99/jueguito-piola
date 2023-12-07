from typing import Any
import pygame
import random
import math
import sys

#inicializando la libreria
pygame.init()
#reloj
reloj=pygame.time.Clock()
FPS=60
#creacion de la ventana
ancho = 1500
alto = 900
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Cat, run!")

# Música de fondo
#pygame.mixer.music.load("musica.mpeg")
#pygame.mixer.music.play(-1)

# Logo del juego
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

#IMAGENES JUGADOR:
#escalas
scala_personaje=2
scala_arma=1
scala_bala=0.5
scala_enemigo=2
#funcion para escalar una nueva imagen 
def escalar(image, scale):
    al_personaje=image.get_width()
    an_personaje=image.get_height()
    imagen_escalada=pygame.transform.scale(image,(al_personaje*scale,an_personaje*scale))
    return imagen_escalada

#cambios de imagen de jugador
jugador_animaciones=[]
for i in range(1,7):
    cambios=pygame.image.load(f"run//cat{i}.png")
    cambios=escalar(cambios,scala_personaje)
    jugador_animaciones.append(cambios)

#IMAGEN ARMA Y BALA:
arma_imagen=pygame.image.load("arma3.png").convert_alpha()
arma_imagen=escalar(arma_imagen,scala_arma)
bala_imagen=pygame.image.load("bala.png")
bala_imagen=escalar(bala_imagen,scala_bala)
tiempo_entre_disparos_balas=200

#ENEMIGOS:
#IMAGENES DE OBSTACULOS:
obstaculo1=pygame.image.load("waos.png").convert_alpha()
misil=pygame.image.load("misil.png").convert_alpha()

#IMAGENES DE OBSTACULOS:
obstaculo1=pygame.image.load("waos.png").convert_alpha()
misil=pygame.image.load("misil.png").convert_alpha()

#FONDOS:
background = pygame.image.load("fondo1.png")
game_over = pygame.image.load("gameover.jpg")
fondo_menu=pygame.image.load("Menu .png")

#IMAGENES ITEMS:
moneda_image = pygame.image.load("moneda.png").convert_alpha()

#IMAGENES SONIDO:
sonido_abajo = pygame.image.load("bajar.png").convert_alpha()
sonido_mute = pygame.image.load("apagado.png").convert_alpha()
sonido_subir = pygame.image.load("subir.png").convert_alpha()


#VARIABLES DE CAMBIO
velocidad_jugador=5
velocidad_bala=20
alto_personaje=90
ancho_personaje=90

# Agrega una nueva variable para la velocidad vertical del personaje
delta_y = 0
delta_x = 0
# Agrega una constante para la gravedad
gravedad = 1

#MOVIMIENTO DEL JUGADOR
arriba=False
abajo=False
izquierda=False
derecha=False

#VILLANO:
animaciones_enemigos=[]
for enemigos in range(1,4):
    enemigos_cambios=pygame.image.load(f"malo//villano{enemigos}.png")
    enemigos_cambios=escalar(enemigos_cambios,scala_enemigo)
    animaciones_enemigos.append(enemigos_cambios)

#TIEMPO
clock = pygame.time.Clock()
score = 0
#LOOP
loop = True
fondo_x = 0
fondo_velocidad = 8

#IMAGENES ITEMS:
monedas = []
#IMAGENES OBSTACULOS:
obstaculos = []
misiles = []  
obstaculos_linea = []

#Generacion de Evento
GENERAR_OBSTACULO_EVENTO = pygame.USEREVENT + 1
GENERAR_MISIL_EVENTO =pygame.USEREVENT + 2
GENERAR_MONEDA_EVENTO = pygame.USEREVENT + 3

#Evento
pygame.time.set_timer(GENERAR_OBSTACULO_EVENTO, 3000)
pygame.time.set_timer(GENERAR_MISIL_EVENTO, 8000)
pygame.time.set_timer(GENERAR_MONEDA_EVENTO, random.randint(3000, 6000)) 


class Jugador:
    def __init__(self, x, y,animaciones,energia):
        self.flip=False
        self.animaciones=animaciones
        self.frame_index=1
        #imagen que se muestra en la actualidad
        self.image=animaciones[self.frame_index]
        self.update_time=pygame.time.get_ticks()
        self.forma= self.image.get_rect()
        self.forma.center=(x,y)
        
    def actualizar(self):
        tiempo_animacion=100
        self.image=self.animaciones[self.frame_index]
        if pygame.time.get_ticks()- self.update_time >= tiempo_animacion:
            self.frame_index=self.frame_index +1 #actualizacion cada milisegundo
            self.update_time=pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index=1

    def movimiento(self, pos_x, pos_y):
        if pos_x < 0: #va a la izquierda
            self.flip=True
        if pos_x > 0: #va a la derecha
            self.flip=False
        self.forma.x = self.forma.x + pos_x
        self.forma.y = self.forma.y + pos_y
    
    def mirar(self,interfaz):
        imagen_flip=pygame.transform.flip(self.image,self.flip,False)
        interfaz.blit(imagen_flip,self.forma)
        #pygame.draw.rect(interfaz, (255, 255, 0), self.forma,1)


# Cambios en la clase de disparos
class Arma:
    def __init__(self,image,image_bala):
        self.image_bala=image_bala
        self.image_original = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.image_original,self.angle)
        self.rect= self.image.get_rect()#encapsular
        self.disparo=False
        self.ultimo_disparo=pygame.time.get_ticks()

    def actualizar_arma(self,personaje):
        tiempo_entre_disparos=tiempo_entre_disparos_balas
        bala=None
        self.rect.center=personaje.forma.center
        if personaje.flip ==False:
            self.rect.x += personaje.forma.width/2
            self.rotacion_personaje(False)
        else: 
            self.rect.x -= personaje.forma.width/2
            self.rotacion_personaje(True)

        #mover mouse
        posicion_mouse=pygame.mouse.get_pos()
        diferencia_x=posicion_mouse[0] - self.rect.centerx
        diferencia_y=-(posicion_mouse[1] - self.rect.centery)
        self.angle= math.degrees(math.atan2(diferencia_y,diferencia_x)) #arco tng
        #falta colocar las concidiciones del angulo

        #detectar los clicks del mouse
        if pygame.mouse.get_pressed()[0] and self.disparo==False  and(pygame.time.get_ticks()-self.ultimo_disparo>=tiempo_entre_disparos):
            bala=Bala(self.image_bala,self.rect.centerx,self.rect.centery,self.angle)
            self.disparo=True
            self.ultimo_disparo=pygame.time.get_ticks()
        #resetear el click
        if pygame.mouse.get_pressed()[0]==False:
            self.disparo=False

        return bala

    def mirar(self,ventana):
        self.image=pygame.transform.rotate(self.image,self.angle)
        ventana.blit(self.image,self.rect)
        #pygame.draw.rect(ventana, (255, 255, 0), self.rect,1)
    
    def rotacion_personaje(self,rotando):
        if rotando==True:
            imagen_flip= pygame.transform.flip(self.image_original,True, False)
            self.image = pygame.transform.rotate(imagen_flip,self.angle)
        else:
            imagen_flip= pygame.transform.flip(self.image_original,False, False)
            self.image = pygame.transform.rotate(imagen_flip,self.angle)

class Bala(pygame.sprite.Sprite): #herencia de pygame
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self) #hereda al constructor
        self.imagen_original=image
        self.angle=angle
        self.image=pygame.transform.rotate(self.imagen_original, self.angle)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.delta_x=math.cos(math.radians(self.angle))*velocidad_bala
        self.delta_y=-math.sin(math.radians(self.angle))*velocidad_bala
    def update(self):
        self.rect.x+=self.delta_x
        self.rect.y+=self.delta_y

        if self.rect.right<0 or self.rect.left>ancho or self.rect.bottom <0 or self.rect.top>alto:
            self.kill()

    def dibujar(self,interfaz):
        interfaz.blit(self.image,(self.rect.centerx,self.rect.centery - int(self.image.get_height())))


class Moneda:
    def __init__(self, imagen, velocidad, y):
        self.image = imagen
        self.rect = self.image.get_rect()
        self.velocidad = velocidad
        self.rect.x = ancho  # Inicializar en el borde derecho de la pantalla
        self.rect.y = y  # La posición vertical de la moneda

    def mover(self):
        self.rect.x -= self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

    def colision_jugador(self, jugador):
        return self.rect.colliderect(jugador.forma)
    
for i in range(1):
    nueva_moneda = Moneda(moneda_image, velocidad=8,y=random.randint(300,600))
    monedas.append(nueva_moneda)

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, imagen, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.velocidad = velocidad
        self.rect.x = ancho  # Inicializar en el borde derecho de la pantalla
        self.rect.y = random.randint(0, alto - self.rect.height)  # Posición vertical aleatoria

    def mover(self):
        self.rect.x -= self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

    def colision_jugador(self, jugador):
        return self.rect.colliderect(jugador.forma)

#INICIALIZAMOS OBJETOS:S
jugador = Jugador(80,400,jugador_animaciones,100)
arma=Arma(arma_imagen,bala_imagen)
grupo_balas=pygame.sprite.Group()

def dibujar_texto (surface, text, size,x,y):
      font= pygame.font.SysFont("serif",size)
      text_surface= font.render(text, True, [255,255,255])
      text_rect= text_surface.get_rect()
      text_rect.midtop=(x,y)
      surface.blit(text_surface,text_rect)

# Variables del menú
fuente_opciones = pygame.font.SysFont("serif", 40)
opciones = ["JUGAR", "SALIR"]
opcion_seleccionada = 0

# Funciones del menú
def dibujar_menu():
    screen.blit(fondo_menu,[0,0])
    for i, opcion in enumerate(opciones):
        texto = fuente_opciones.render(opcion, True, (0,0,0))
        x_opcion = ancho // 2 - texto.get_width() // 2
        y_opcion = alto // 2 + i * (fuente_opciones.get_height() + 10)
        if i == opcion_seleccionada:
            pygame.draw.rect(screen, (0,0,0), (x_opcion - 10, y_opcion - 5, texto.get_width() + 20, texto.get_height() + 10))
            texto = fuente_opciones.render(opcion, True, (255,255,255))
        screen.blit(texto, (x_opcion, y_opcion))

def cambiar_opcion(direccion):
    global opcion_seleccionada
    opcion_seleccionada += direccion
    if opcion_seleccionada < 0:
        opcion_seleccionada = len(opciones) - 1
    elif opcion_seleccionada >= len(opciones):
        opcion_seleccionada = 0

#PANTALLA
def pantalla():
    #fondo
    global fondo_x
    fondo_avanza = fondo_x % background.get_rect().width
    screen.blit(background, (fondo_avanza - background.get_rect().width, 0))
    if fondo_avanza < ancho:
        screen.blit(background, (fondo_avanza, 0))
    fondo_x -= fondo_velocidad
    
#BUCLE PRINCIPAL: Es decir un loop
menu_abierto = True
while menu_abierto:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif event.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif event.key == pygame.K_RETURN:
                if opcion_seleccionada == 0:
                    menu_abierto = False  # Inicia el juego
                elif opcion_seleccionada == 1:
                    sys.exit()  # Sale del juego

    dibujar_menu()
    pygame.display.flip()
 
#INICIALIZAMOS OBJETOS:S
jugador = Jugador(80,400,jugador_animaciones,100)
arma=Arma(arma_imagen,bala_imagen)
grupo_balas=pygame.sprite.Group()

while loop:
    reloj.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == GENERAR_OBSTACULO_EVENTO:
            nuevo_obstaculo = Obstaculo(pygame.image.load("waos.png").convert_alpha(), velocidad=8)
            obstaculos.append(nuevo_obstaculo)
        elif event.type == GENERAR_MISIL_EVENTO:
            nuevo_misil = Obstaculo(pygame.image.load("misil.png").convert_alpha(), velocidad=20)
            misiles.append(nuevo_misil)
        elif event.type == GENERAR_MONEDA_EVENTO:
            nueva_moneda = Moneda(moneda_image, velocidad=8, y=300)
            monedas.append(nueva_moneda)

    pantalla()

    for obstaculo in obstaculos:
        obstaculo.mover()
        obstaculo.dibujar(screen)
        if obstaculo.colision_jugador(jugador):
            screen.blit(game_over, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            loop = False

    for misil in misiles:
        misil.mover()
        misil.dibujar(screen)
        if misil.colision_jugador(jugador):
            screen.blit(game_over, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            loop = False
        if misil.rect.x < 0:  # Si el misil sale de la pantalla
            misiles.remove(misil)

    for moneda in monedas:
        moneda.mover()
        moneda.dibujar(screen)
                
        if moneda.colision_jugador(jugador):
            score += 1
            monedas.remove(moneda)

    # MOVIMIENTO DEL JUGADOR
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        izquierda = True
    if keys[pygame.K_d]:
        derecha = True
    if keys[pygame.K_s]:
        abajo = True
    if keys[pygame.K_w]:
        arriba = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            izquierda = False
        if event.key == pygame.K_d:
            derecha = False
        if event.key == pygame.K_s:
            abajo = False
        if event.key == pygame.K_w:
            arriba = False

    #calculo del movimiento
    delta_x = 0
    delta_y = 0
    if derecha:
        delta_x = velocidad_jugador
    if izquierda:
        delta_x = -velocidad_jugador
    if arriba:
        delta_y = -velocidad_jugador
    if abajo:
        delta_y = velocidad_jugador

    #teclas de la musica
        #Volumen baja
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
        

    arma.mirar(screen)
    jugador.movimiento(delta_x, delta_y)
    jugador.actualizar()
    jugador.mirar(screen)

    bala = arma.actualizar_arma(jugador)
    if bala:
        grupo_balas.add(bala)

    for bala in grupo_balas:
        bala.update()

    for bala in grupo_balas:
        bala.dibujar(screen)

    dibujar_texto(screen, str(score),25 ,70,10)
    screen.blit(moneda_image,(25,9))
    pygame.display.update()

pygame.quit()