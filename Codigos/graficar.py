# graficar.py

import matplotlib.pyplot as plt

def guardar_genoma(genoma, nombre_archivo):
    entradas = [n for n in genoma.nodos if n.tipo=="entrada"]
    ocultos = [n for n in genoma.nodos if n.tipo=="oculto"]
    salidas = [n for n in genoma.nodos if n.tipo=="salida"]

    with open(nombre_archivo, "w") as f:
        f.write("Nodos de entrada:\n")
        for n in entradas:
            f.write(f"  id:{n.id}, tipo:{n.tipo}\n")
        f.write("Nodos ocultos:\n")
        for n in ocultos:
            f.write(f"  id:{n.id}, tipo:{n.tipo}\n")
        f.write("Nodos de salida:\n")
        for n in salidas:
            f.write(f"  id:{n.id}, tipo:{n.tipo}\n")

        f.write("Conexiones:\n")
        for c in genoma.conexiones:
            f.write(f"  {c.nodo_entrada}->{c.nodo_salida}, peso:{c.peso:.4f}, habilitada:{c.habilitada}, innov:{c.innovacion}\n")

def graficar_historial_aptitud(historial_aptitud, nombre_archivo):
    plt.figure(figsize=(8,6))
    plt.plot(historial_aptitud, marker='o')
    plt.title("Evolución del mejor fitness")
    plt.xlabel("Generaciones")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.savefig(nombre_archivo)
    plt.close()

def dibujar_red(genoma, nombre_archivo):
    entradas = [n for n in genoma.nodos if n.tipo=="entrada"]
    ocultos = [n for n in genoma.nodos if n.tipo=="oculto"]
    salidas = [n for n in genoma.nodos if n.tipo=="salida"]

    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_xlim(0,3)
    ax.set_ylim(0, max(len(entradas), len(ocultos), len(salidas))+1)
    ax.axis('off')

    def ubicar_nodos(lista_nodos, x):
        paso = (max(len(entradas),len(ocultos),len(salidas))+1)/(len(lista_nodos)+1)
        pos = {}
        for i,n in enumerate(lista_nodos):
            pos[n.id] = (x, (i+1)*paso)
        return pos

    pos_in = ubicar_nodos(entradas, 0)
    pos_h = ubicar_nodos(ocultos, 1)
    pos_out = ubicar_nodos(salidas, 2)
    posiciones = {}
    posiciones.update(pos_in)
    posiciones.update(pos_h)
    posiciones.update(pos_out)

    # Dibujar conexiones
    for c in genoma.conexiones:
        if c.habilitada:
            x1,y1 = posiciones[c.nodo_entrada]
            x2,y2 = posiciones[c.nodo_salida]
            color = 'blue' if c.peso>=0 else 'red'
            ax.plot([x1,x2],[y1,y2], color=color, alpha=0.5)

    # Dibujar nodos
    for n in entradas:
        x,y = posiciones[n.id]
        ax.plot(x,y,'o',color='lightblue',markersize=12)
        ax.text(x,y,f"E{n.id}",ha='center',va='center',fontsize=8)
    for n in ocultos:
        x,y = posiciones[n.id]
        ax.plot(x,y,'o',color='lightgreen',markersize=12)
        ax.text(x,y,f"H{n.id}",ha='center',va='center',fontsize=8)
    for n in salidas:
        x,y = posiciones[n.id]
        ax.plot(x,y,'o',color='orange',markersize=12)
        ax.text(x,y,f"S{n.id}",ha='center',va='center',fontsize=8)

    plt.savefig(nombre_archivo)
    plt.close()
