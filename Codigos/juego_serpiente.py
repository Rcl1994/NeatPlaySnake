# juego_serpiente.py

import random
import pygame
import sys
from parametros import LIMITE_SIN_COMER, VELOCIDAD_JUEGO
from neat import construir_red

class JuegoSerpiente:
    def __init__(self, ancho=10, alto=10):
        self.ancho = ancho
        self.alto = alto
        self.reiniciar()

    def reiniciar(self):
        self.serpiente = [(self.ancho//2, self.alto//2)]
        self.direccion = (1,0)
        self.aparecer_comida()
        self.pasos_sin_comer = 0
        self.viva = True
        self.puntaje = 0

    def aparecer_comida(self):
        while True:
            fx = random.randint(0, self.ancho-1)
            fy = random.randint(0, self.alto-1)
            if (fx,fy) not in self.serpiente:
                self.comida = (fx,fy)
                break

    def paso(self, accion):
        self.direccion = self.nueva_direccion(accion)
        cabeza = self.serpiente[0]
        nueva_cabeza = (cabeza[0]+self.direccion[0], cabeza[1]+self.direccion[1])

        if nueva_cabeza[0]<0 or nueva_cabeza[0]>=self.ancho or nueva_cabeza[1]<0 or nueva_cabeza[1]>=self.alto:
            self.viva = False
            return
        if nueva_cabeza in self.serpiente:
            self.viva = False
            return

        self.serpiente.insert(0,nueva_cabeza)
        if nueva_cabeza == self.comida:
            self.puntaje += 1
            self.aparecer_comida()
            self.pasos_sin_comer = 0
        else:
            self.serpiente.pop()
            self.pasos_sin_comer += 1
            if self.pasos_sin_comer > LIMITE_SIN_COMER:
                self.viva = False

    def nueva_direccion(self, accion):
        dx, dy = self.direccion
        # 0: izquierda, 1: recto, 2: derecha
        if accion == 0:
            return (-dy, dx)
        elif accion == 1:
            return (dx,dy)
        elif accion == 2:
            return (dy, -dx)

    def obtener_estado(self):
        cabeza = self.serpiente[0]
        fx, fy = self.comida
        dx_comida = (fx - cabeza[0])/(self.ancho)
        dy_comida = (fy - cabeza[1])/(self.alto)
        dirx, diry = self.direccion

        peligro_frente = self.colision_frente(dirx, diry)
        izquierda_dir = (-diry, dirx)
        derecha_dir = (diry, -dirx)
        peligro_izquierda = self.colision_frente(izquierda_dir[0], izquierda_dir[1])
        peligro_derecha = self.colision_frente(derecha_dir[0], derecha_dir[1])

        return [dx_comida, dy_comida, dirx, diry, float(peligro_frente), float(peligro_izquierda), float(peligro_derecha)]

    def colision_frente(self, dx, dy):
        cabeza = self.serpiente[0]
        nueva_cabeza = (cabeza[0]+dx, cabeza[1]+dy)
        if nueva_cabeza[0]<0 or nueva_cabeza[0]>=self.ancho or nueva_cabeza[1]<0 or nueva_cabeza[1]>=self.alto:
            return True
        if nueva_cabeza in self.serpiente:
            return True
        return False

def evaluar_genoma(genoma, mostrar=False):
    ancho, alto, tam_celda = 10,10,20
    if mostrar:
        pygame.init()
        pantalla = pygame.display.set_mode((ancho*tam_celda, alto*tam_celda))
        pygame.display.set_caption("Serpiente NEAT - Visualización")
        reloj = pygame.time.Clock()
    else:
        pygame.init()
        pantalla = pygame.Surface((1,1))
        reloj = pygame.time.Clock()

    juego = JuegoSerpiente(ancho, alto)
    red = construir_red(genoma)

    while juego.viva:
        if mostrar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        estado = juego.obtener_estado()
        salida = red(estado)
        accion = salida.index(max(salida))
        juego.paso(accion)

        if mostrar:
            pantalla.fill((0,0,0))
            pygame.draw.rect(pantalla, (255,0,0), (juego.comida[0]*tam_celda, juego.comida[1]*tam_celda, tam_celda, tam_celda))
            for x,y in juego.serpiente:
                pygame.draw.rect(pantalla, (0,255,0), (x*tam_celda,y*tam_celda,tam_celda,tam_celda))
            pygame.display.flip()
            reloj.tick(VELOCIDAD_JUEGO)

    aptitud = juego.puntaje
    if mostrar:
        pygame.quit()
    return aptitud
