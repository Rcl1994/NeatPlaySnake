FROM python:3.9-slim

# Actualizamos e instalamos dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev python3-opengl libsmpeg-dev \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libxext-dev libxrender-dev libxrandr-dev libxi-dev \
    libglib2.0-0 libfreetype6-dev libpng-dev \
    # Paquetes adicionales para soporte X11 (opcional)
    x11-apps \
    # Otras librerías útiles
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Instalar pygame y matplotlib
RUN pip install --no-cache-dir pygame matplotlib

# Crear directorio de la aplicación
WORKDIR /app

# Copiar el código fuente al contenedor
COPY /Codigos /app

# Crear un directorio para XDG_RUNTIME_DIR
ENV XDG_RUNTIME_DIR=/tmp/runtime
RUN mkdir -p /tmp/runtime && chmod 700 /tmp/runtime

# Opcional: si no se requiere audio real, se puede establecer un driver dummy para evitar errores ALSA
ENV SDL_AUDIODRIVER=dummy

# Crear volumen para resultados
VOLUME ["/app/resultados"]


# Comando por defecto
CMD ["python", "main.py"]
