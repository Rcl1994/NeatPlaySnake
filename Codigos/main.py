# main.py

from parametros import (POBLACION_TAM, NUM_ENTRADAS, NUM_SALIDAS, GENERACIONES)
from neat import Poblacion
from juego_serpiente import evaluar_genoma
from graficar import guardar_genoma, graficar_historial_aptitud, dibujar_red

if __name__ == "__main__":
    poblacion = Poblacion(POBLACION_TAM, NUM_ENTRADAS, NUM_SALIDAS)

    historial_mejor_aptitud = []
    diez_por_ciento = GENERACIONES//10 if GENERACIONES>=10 else 1

    for gen in range(GENERACIONES):
        # Evaluar todos los individuos sin mostrar
        for g in poblacion.genomas:
            g.aptitud = evaluar_genoma(g, mostrar=False)

        # Mejor genoma
        mejor = max(poblacion.genomas, key=lambda x: x.aptitud)
        historial_mejor_aptitud.append(mejor.aptitud)
        print(f"Generación {gen}, Mejor fitness: {mejor.aptitud}")

        # Cada 10% de las generaciones, mostrar el primero de la población
        if (gen+1) % diez_por_ciento == 0:
            primero = poblacion.genomas[0]
            evaluar_genoma(primero, mostrar=True)
            guardar_genoma(mejor, f"resultados/mejor_genoma_gen{gen+1}.txt")

        # Especiar
        poblacion.especiar()

        # Reproducir
        poblacion.reproducir()

    # Mejor final
    mejor = max(poblacion.genomas, key=lambda x: x.aptitud)
    print("Mejor genoma final con fitness:", mejor.aptitud)

    # Graficar la evolución del desempeño con matplotlib
    graficar_historial_aptitud(historial_mejor_aptitud, "resultados/evolucion_fitness.png")

    # Crear imagen de la red del mejor genoma con matplotlib
    dibujar_red(mejor, "resultados/red_mejor_genoma.png")
