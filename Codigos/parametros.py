# parametros.py

import os

# Parámetros del NEAT
NUM_ENTRADAS = 7   # dx_comida, dy_comida, dirx, diry, peligro_frente, peligro_izquierda, peligro_derecha
NUM_SALIDAS = 3    # girar_izquierda, recto, girar_derecha
POBLACION_TAM = 50
UMBRAL_COMPATIBILIDAD = 3.0
TASA_MUTACION = 0.8
TASA_MUTACION_CONEXION = 0.5
TASA_MUTACION_NODO = 0.03
TASA_MUTACION_ADDCONEXION = 0.05
TASA_CRUZAMIENTO = 0.75
GENERACIONES = 50
LIMITE_SIN_COMER = 100  # pasos máximos sin comer
VELOCIDAD_JUEGO = 10

HISTORIAL_INNOVACION = []

# Carpeta base para guardar resultados
BASE_DIR = "/data"
RESULTADOS_DIR = os.path.join(BASE_DIR, "resultados")

# Crear la carpeta si no existe
if not os.path.exists(RESULTADOS_DIR):
    os.makedirs(RESULTADOS_DIR)
