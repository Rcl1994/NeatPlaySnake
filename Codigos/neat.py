# neat.py

import random
import math
import copy
from parametros import (HISTORIAL_INNOVACION, UMBRAL_COMPATIBILIDAD,
                        TASA_MUTACION, TASA_MUTACION_CONEXION,
                        TASA_MUTACION_NODO, TASA_MUTACION_ADDCONEXION,
                        TASA_CRUZAMIENTO, NUM_ENTRADAS, NUM_SALIDAS)

class GenNodo:
    def __init__(self, nodo_id, tipo):
        self.id = nodo_id
        self.tipo = tipo # "entrada", "oculto", "salida"

class GenConexion:
    def __init__(self, nodo_entrada, nodo_salida, peso, habilitada, innovacion):
        self.nodo_entrada = nodo_entrada
        self.nodo_salida = nodo_salida
        self.peso = peso
        self.habilitada = habilitada
        self.innovacion = innovacion

class Genoma:
    def __init__(self):
        self.nodos = []
        self.conexiones = []
        self.aptitud = 0.0
        self.aptitud_ajustada = 0.0
        self.especie = None

    def copiar(self):
        g = Genoma()
        g.nodos = [GenNodo(n.id, n.tipo) for n in self.nodos]
        g.conexiones = [GenConexion(c.nodo_entrada, c.nodo_salida, c.peso, c.habilitada, c.innovacion) for c in self.conexiones]
        g.aptitud = self.aptitud
        g.aptitud_ajustada = self.aptitud_ajustada
        return g

    def inicializar(self, num_entradas, num_salidas):
        self.nodos = []
        self.conexiones = []
        nodo_id = 0
        # nodos de entrada
        for i in range(num_entradas):
            self.nodos.append(GenNodo(nodo_id, "entrada"))
            nodo_id += 1
        # nodos de salida
        for o in range(num_salidas):
            self.nodos.append(GenNodo(nodo_id, "salida"))
            nodo_id += 1

        # Conexiones totalmente conectadas de entrada a salida
        for i in range(num_entradas):
            for o in range(num_salidas):
                self.agregar_conexion(i, num_entradas+o, random.uniform(-1,1))

    def agregar_conexion(self, n_entrada, n_salida, peso=None):
        if peso is None:
            peso = random.uniform(-1,1)
        for c in self.conexiones:
            if c.nodo_entrada == n_entrada and c.nodo_salida == n_salida:
                return
        innovacion = obtener_numero_innovacion(n_entrada, n_salida)
        self.conexiones.append(GenConexion(n_entrada, n_salida, peso, True, innovacion))

    def agregar_nodo(self):
        conexiones_habilitadas = [c for c in self.conexiones if c.habilitada]
        if len(conexiones_habilitadas) == 0:
            return
        conn = random.choice(conexiones_habilitadas)
        conn.habilitada = False
        nuevo_id_nodo = max([n.id for n in self.nodos]) + 1
        nuevo_nodo = GenNodo(nuevo_id_nodo, "oculto")
        self.nodos.append(nuevo_nodo)

        inno1 = obtener_numero_innovacion(conn.nodo_entrada, nuevo_id_nodo)
        nueva_conn1 = GenConexion(conn.nodo_entrada, nuevo_id_nodo, 1.0, True, inno1)

        inno2 = obtener_numero_innovacion(nuevo_id_nodo, conn.nodo_salida)
        nueva_conn2 = GenConexion(nuevo_id_nodo, conn.nodo_salida, conn.peso, True, inno2)

        self.conexiones.append(nueva_conn1)
        self.conexiones.append(nueva_conn2)

    def mutar(self):
        for c in self.conexiones:
            if random.random() < TASA_MUTACION_CONEXION:
                c.peso += random.uniform(-0.5,0.5)

        if random.random() < TASA_MUTACION_NODO:
            self.agregar_nodo()

        if random.random() < TASA_MUTACION_ADDCONEXION:
            # añadir conexión aleatoria
            nodo_in = random.choice(self.nodos)
            nodo_out = random.choice(self.nodos)
            if nodo_in.id != nodo_out.id and nodo_in.tipo != "salida" and nodo_out.tipo != "entrada":
                self.agregar_conexion(nodo_in.id, nodo_out.id)

def obtener_numero_innovacion(nodo_entrada, nodo_salida):
    global HISTORIAL_INNOVACION
    for (inn, inp, outp) in HISTORIAL_INNOVACION:
        if inp == nodo_entrada and outp == nodo_salida:
            return inn
    nueva_innov = len(HISTORIAL_INNOVACION)+1
    HISTORIAL_INNOVACION.append((nueva_innov, nodo_entrada, nodo_salida))
    return nueva_innov

def distancia_compatibilidad(g1, g2):
    i1 = {c.innovacion:c for c in g1.conexiones}
    i2 = {c.innovacion:c for c in g2.conexiones}
    todos_innov = set(i1.keys()).union(set(i2.keys()))
    disjuntos = 0
    dif_pesos = 0
    coincidencias = 0
    for inn in todos_innov:
        c1 = i1.get(inn, None)
        c2 = i2.get(inn, None)
        if c1 and c2:
            coincidencias += 1
            dif_pesos += abs(c1.peso - c2.peso)
        else:
            disjuntos += 1
    if coincidencias == 0:
        coincidencias = 1
    return disjuntos + (dif_pesos / coincidencias)

def cruzar(g1, g2):
    hijo = Genoma()
    hijo.nodos = [GenNodo(n.id, n.tipo) for n in g1.nodos]

    i1 = {c.innovacion:c for c in g1.conexiones}
    i2 = {c.innovacion:c for c in g2.conexiones}

    todos_innov = set(i1.keys()).union(set(i2.keys()))
    for inn in todos_innov:
        c1 = i1.get(inn, None)
        c2 = i2.get(inn, None)
        if c1 and c2:
            elegido = random.choice([c1,c2])
            hijo.conexiones.append(GenConexion(elegido.nodo_entrada, elegido.nodo_salida, elegido.peso, elegido.habilitada, elegido.innovacion))
        elif c1 and (c1 in i1.values()):
            hijo.conexiones.append(GenConexion(c1.nodo_entrada, c1.nodo_salida, c1.peso, c1.habilitada, c1.innovacion))

    return hijo

class Poblacion:
    def __init__(self, tam, num_entradas, num_salidas):
        self.genomas = []
        for _ in range(tam):
            g = Genoma()
            g.inicializar(num_entradas, num_salidas)
            self.genomas.append(g)

    def especiar(self):
        if len(self.genomas) == 0:
            return
        representante = self.genomas[0]
        for g in self.genomas:
            dist = distancia_compatibilidad(g, representante)
            if dist < UMBRAL_COMPATIBILIDAD:
                g.especie = 1
            else:
                g.especie = 2

    def reproducir(self):
        self.genomas.sort(key=lambda x: x.aptitud, reverse=True)
        corte = len(self.genomas)//2
        padres = self.genomas[:corte]
        nuevos_genomas = []
        while len(nuevos_genomas) < len(self.genomas):
            p1 = random.choice(padres)
            p2 = random.choice(padres)
            if random.random() < TASA_CRUZAMIENTO:
                hijo = cruzar(p1, p2)
            else:
                hijo = p1.copiar()
            if random.random() < TASA_MUTACION:
                hijo.mutar()
            nuevos_genomas.append(hijo)
        self.genomas = nuevos_genomas

def construir_red(genoma):
    def sigmoide(x):
        return 1/(1+math.exp(-x))

    nodos_entrada = [n.id for n in genoma.nodos if n.tipo=="entrada"]
    nodos_salida = [n.id for n in genoma.nodos if n.tipo=="salida"]
    nodos_ocultos = [n.id for n in genoma.nodos if n.tipo=="oculto"]

    def propagar(entradas):
        valores = {}
        for i, nid in enumerate(nodos_entrada):
            valores[nid] = entradas[i]

        for nid in nodos_ocultos + nodos_salida:
            s = 0.0
            for c in genoma.conexiones:
                if c.habilitada and c.nodo_salida == nid:
                    if c.nodo_entrada in valores:
                        s += valores[c.nodo_entrada]*c.peso
            valores[nid] = sigmoide(s)

        return [valores[o] for o in nodos_salida]

    return propagar
