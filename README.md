# Retro Gaming Web con Podman y EmulatorJS

Proyecto Final de Sistemas Operativos I basado en el **Proyecto 5: Retro-gaming web con EmulatorJS**.
Este proyecto consiste en crear una aplicación web de retro-gaming usando **EmulatorJS**, desplegada con **Podman rootless** y complementada con instrumentación programada para medir la **latencia entrada-a-frame** durante la ejecución de juegos retro.

El objetivo principal es demostrar lo aprendido en el curso mediante conceptos relacionados con **procesos, planificación de CPU, uso de recursos, prioridades y medición de rendimiento**.

---

## Pasos realizados para desarrollar el proyecto

| Paso | Descripción general |
|---|---|
| Paso 1 | Instalación de Podman, creación del contenedor, despliegue con Nginx y configuración del puerto 8080 |
| Paso 2 | Desarrollo de la interfaz web, integración de EmulatorJS, catálogo de juegos y estilos CSS |
| Paso 3 | Instrumentación de latencia entrada-a-frame mediante JavaScript |
| Paso 4 | Experimentos de carga CPU, observación de procesos y modificación de prioridad |
| Paso 5 | Procesamiento de resultados, gráficos, análisis, informe y presentación |

---

## Descripción del proyecto

La aplicación permite ejecutar juegos retro desde el navegador mediante **EmulatorJS**.  
El servidor web se ejecuta dentro de un contenedor **Podman** utilizando **Nginx**.

El proyecto no solo consiste en ejecutar juegos retro en un emulador web, sino también en medir cómo cambia la respuesta del emulador cuando el sistema operativo se encuentra en distintos escenarios:

- Escenario normal.
- Escenario con CPU saturada.
- Escenario con prioridad baja del navegador.
- Intento de prioridad alta o política de tiempo real, cuando el sistema lo permite.

La métrica principal del proyecto es la **latencia entrada-a-frame**.

---

## ¿Qué es la latencia entrada-a-frame?

La latencia entrada-a-frame representa el tiempo que pasa desde que el usuario presiona una tecla hasta que el navegador prepara el siguiente frame visual.

En este proyecto se mide de la siguiente manera:

```text
Tecla presionada
        ↓
Evento keydown detectado por JavaScript
        ↓
Se guarda el tiempo inicial con performance.now()
        ↓
Se espera el siguiente frame con requestAnimationFrame()
        ↓
Se calcula la diferencia en milisegundos
```

Esta medición permite aproximar cuánto tarda el emulador en responder visualmente ante una acción del usuario.

---

## Tecnologías utilizadas

- Linux / Lubuntu / Ubuntu
- Podman rootless
- Nginx
- HTML
- CSS
- JavaScript
- EmulatorJS
- Python 3
- Bash
- Matplotlib
- Herramientas del sistema:
  - `top`
  - `ps`
  - `pgrep`
  - `renice`
  - `chrt`

---

## Estructura del proyecto

```text
retro-gaming-emulatorjs/
│
├── Containerfile
├── README.md
│
├── www/
│   ├── index.html
│   ├── play.html
│   │
│   ├── css/
│   │   └── styles.css
│   │
│   ├── js/
│   │   └── medir_latencia.js
│   │
│   └── roms/
│       ├── atari/
│       │   └── juego_atari.bin
│       │
│       ├── gameboy/
│       │   └── juego_gameboy.gbc
│       │
│       └── nes/
│           └── juego_nes.nes
│
├── scripts/
│   ├── carga_cpu.py
│   ├── experimento_cpu.sh
│   └── graficar_resultados.py
│
├── resultados/
│   ├── normal.csv
│   ├── cpu_stress.csv
│   ├── prioridad_baja.csv
│   ├── resumen_resultados.csv
│   │
│   └── graficos/
│       ├── latencia_promedio.png
│       ├── latencia_mediana.png
│       ├── latencia_maxima.png
│       ├── latencia_p95.png
│       ├── distribucion_latencia.png
│       └── distribucion_latencia_hasta_100ms.png
│
└── docs/
    └── informe_tecnico.pdf
```

---

## Instalación y ejecución

### Actualizar el sistema

```bash
sudo apt update
```

### Instalar Podman

```bash
sudo apt install podman -y
```

### Verificar la versión de Podman

```bash
podman --version
```

### Verificar que Podman funcione

```bash
podman ps
```

### Instalar Python y herramientas para gráficos

```bash
sudo apt install python3 python3-pip -y
pip3 install matplotlib
```

---

## Contenedor

### Construcción del contenedor

Desde la carpeta principal del proyecto:

```bash
cd ~/retro-gaming-emulatorjs
podman build -t retro-emulatorjs .
```

### Ejecución del contenedor

```bash
podman run -d --name retro-web -p 8080:80 retro-emulatorjs
```

### Verificar que el contenedor esté corriendo

```bash
podman ps
```

### Abrir en el navegador

```text
http://localhost:8080
```

---

## Reiniciar el contenedor después de cambios

Cada vez que se modifique un archivo HTML, CSS, JavaScript o ROM, se debe reconstruir la imagen y levantar nuevamente el contenedor.

```bash
cd ~/retro-gaming-emulatorjs

podman stop retro-web
podman rm retro-web

podman build -t retro-emulatorjs .

podman run -d --name retro-web -p 8080:80 retro-emulatorjs
```

---

## Páginas principales

### Página principal

Archivo:

```text
www/index.html
```

Contiene el catálogo de consolas y juegos:

- Atari 2600
- Game Boy
- NES

Cada tarjeta envía a `play.html` con los parámetros necesarios para cargar el emulador.

Ejemplo:

```text
play.html?core=nes&rom=/roms/nes/juego_nes.nes&name=Juego%20NES
```

---

### Página del emulador

Archivo:

```text
www/play.html
```

Esta página recibe los parámetros:

- `core`
- `rom`
- `name`

Luego configura EmulatorJS de la siguiente manera:

```javascript
EJS_player = "#game";
EJS_core = core;
EJS_gameUrl = rom;
EJS_gameName = name;
EJS_pathtodata = "https://cdn.emulatorjs.org/stable/data/";
```

---

## Instrumentación de latencia

Archivo:

```text
www/js/medir_latencia.js
```

Este script mide la latencia entrada-a-frame usando:

```javascript
performance.now()
requestAnimationFrame()
keydown
```

La medición se activa cuando el usuario presiona teclas del juego, por ejemplo:

- Flecha arriba
- Flecha abajo
- Flecha izquierda
- Flecha derecha
- Z
- X
- Enter
- Espacio

El panel de latencia muestra en pantalla la medición en milisegundos mientras se juega.  
También permite descargar las mediciones en un archivo CSV.

---

## Formato CSV de la latencia

Cada archivo CSV contiene mediciones con el siguiente formato:

```csv
escenario,prueba,tecla,latencia_ms,fecha
normal,1,ArrowRight,6.000,2026-06-30T10:00:00Z
normal,2,ArrowLeft,5.000,2026-06-30T10:00:01Z
```

Archivos generados:

```text
resultados/normal.csv
resultados/cpu_stress.csv
resultados/prioridad_baja.csv
```

---

## Experimentos realizados

### Escenario 1: CPU normal

En este escenario, el juego se ejecuta sin carga adicional en el sistema.

| Objetivo | Archivo generado |
|---|---|
| Obtener la latencia base del emulador | `resultados/normal.csv` |

---

### Escenario 2: CPU saturada

En este escenario, se ejecuta un script de carga CPU mientras se juega.

Archivo usado:

```text
scripts/carga_cpu.py
```

Ejecución:

```bash
python3 scripts/carga_cpu.py
```

| Objetivo | Archivo generado |
|---|---|
| Analizar si la latencia aumenta cuando el sistema operativo debe planificar procesos con alta demanda de CPU | `resultados/cpu_stress.csv` |

---

### Escenario 3: baja prioridad del navegador

En este escenario, se identifica el proceso del navegador y se reduce su prioridad con `renice`.

Buscar el proceso del navegador en Firefox:

```bash
pgrep -a firefox
```

Buscar el proceso del navegador en Chromium:

```bash
pgrep -a chromium
```

Aplicar prioridad baja:

```bash
renice -n 10 -p PID
```

| Objetivo | Archivo generado |
|---|---|
| Observar si al reducir la prioridad del navegador cambia la latencia del emulador | `resultados/prioridad_baja.csv` |

---

### Intento de prioridad alta del navegador

También se intentó aplicar prioridad alta al navegador mediante:

```bash
sudo renice -n -5 -p PID
```

Además, se intentó aplicar una política de tiempo real con:

```bash
sudo chrt -f -p 10 PID
```

Sin embargo, estos comandos pueden fallar en algunos entornos por permisos o restricciones del sistema.  
Cuando esto ocurre, se considera una limitación del experimento y se documenta como evidencia.

---

## Scripts del experimento

### `scripts/carga_cpu.py`

Este script genera carga artificial en la CPU.  
Su objetivo es crear un escenario donde el procesador tenga más trabajo y el sistema operativo deba repartir el tiempo de CPU entre varios procesos.

Ejemplo de ejecución:

```bash
python3 scripts/carga_cpu.py
```

---

### `scripts/experimento_cpu.sh`

Este script guía la ejecución de las pruebas y guarda evidencias del sistema operativo.

Funciones principales:

- Verifica que el contenedor Podman esté activo.
- Detecta el navegador abierto.
- Guarda información de los procesos.
- Guarda salidas de `top`.
- Ejecuta el escenario de CPU saturada.
- Aplica prioridad baja al navegador mediante `renice`.
- Guarda evidencias en la carpeta `resultados`.

Dar permisos de ejecución:

```bash
chmod +x scripts/experimento_cpu.sh
```

Ejecutar el experimento:

```bash
./scripts/experimento_cpu.sh
```

---

### `scripts/graficar_resultados.py`

Este script procesa los archivos CSV de latencia y genera gráficos.

Funciones principales:

- Lee los archivos `normal.csv`, `cpu_stress.csv` y `prioridad_baja.csv`.
- Extrae la columna `latencia_ms`.
- Calcula promedio, mediana, mínimo, máximo y percentil 95.
- Genera el archivo `resumen_resultados.csv`.
- Genera gráficos en formato PNG.

Ejecutar:

```bash
python3 scripts/graficar_resultados.py
```

---

## Generación de gráficos

Los gráficos se generan a partir de los archivos CSV ubicados en la carpeta `resultados`.

Archivos de entrada:

```text
resultados/normal.csv
resultados/cpu_stress.csv
resultados/prioridad_baja.csv
```

Comando para generar gráficos:

```bash
python3 scripts/graficar_resultados.py
```

Archivos generados:

```text
resultados/resumen_resultados.csv
resultados/graficos/latencia_promedio.png
resultados/graficos/latencia_mediana.png
resultados/graficos/latencia_maxima.png
resultados/graficos/latencia_p95.png
resultados/graficos/distribucion_latencia.png
resultados/graficos/distribucion_latencia_hasta_100ms.png
```

---

## Resultados obtenidos

| Escenario | Muestras | Promedio ms | Mediana ms | Mínimo ms | Máximo ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|
| Normal | 1000 | 6.015 | 5.0 | 0.0 | 20.0 | 15.00 |
| CPU saturada | 308 | 29.312 | 7.0 | 0.0 | 6372.0 | 23.65 |
| Prioridad baja | 584 | 5.793 | 5.0 | 0.0 | 22.0 | 14.00 |

---

## Análisis de resultados

En el escenario normal, la latencia promedio fue de **6.015 ms**, con una mediana de **5 ms**. Esto indica que el emulador respondió de forma estable cuando el sistema no tenía carga adicional.

En el escenario con CPU saturada, la latencia promedio aumentó a **29.312 ms**. Este aumento se debe principalmente a un valor extremo de **6372 ms**, el cual representa un pico de demora durante la prueba. Sin embargo, la mediana fue de **7 ms** y el percentil 95 fue de **23.65 ms**, lo que indica que la mayoría de mediciones se mantuvieron por debajo de ese valor.

En el escenario con prioridad baja, la latencia promedio fue de **5.793 ms**, muy cercana al escenario normal. Esto puede deberse a que el navegador no fue afectado de forma significativa durante la prueba o a que el sistema todavía pudo asignarle suficiente tiempo de CPU.

En general, los resultados muestran que la carga de CPU puede generar picos de latencia, afectando la respuesta del emulador. Esto se relaciona con la planificación del sistema operativo, ya que el procesador debe repartir tiempo entre varios procesos en ejecución.

---

## Evidencias generadas

Durante las pruebas se generaron evidencias como:

```text
resultados/podman_ps.txt
resultados/top_normal.txt
resultados/top_cpu_stress.txt
resultados/proceso_firefox.txt
resultados/proceso_chromium.txt
resultados/renice_prioridad_baja.txt
resultados/prioridad_baja_proceso.txt
resultados/resumen_resultados.csv
```

Estas evidencias permiten demostrar:

- Que el contenedor estaba activo.
- Que el navegador estaba ejecutándose.
- Que la CPU fue sometida a carga.
- Que se modificó la prioridad del navegador.
- Que se tomaron mediciones reales de latencia.

---

## Conceptos de Sistemas Operativos aplicados

### Procesos

El navegador, el contenedor, Nginx y el script de carga CPU se ejecutan como procesos del sistema operativo.

### Planificación de CPU

El sistema operativo decide qué proceso recibe tiempo de procesador.  
Cuando se genera carga de CPU, el planificador debe repartir el procesador entre más procesos activos.

### Prioridades

Mediante `renice` se puede modificar la prioridad relativa de un proceso.  
En este proyecto se probó reducir la prioridad del navegador para observar si afectaba la latencia.

### Contenedores

Podman permite ejecutar la aplicación web dentro de un contenedor sin usar Docker daemon.  
El contenedor ejecuta Nginx y sirve los archivos HTML, CSS, JavaScript y ROMs.

### Medición de rendimiento

La latencia entrada-a-frame se midió mediante un script propio en JavaScript.  
Los datos se exportaron en CSV y luego fueron procesados con Python.

---

## Limitaciones

- La emulación se ejecuta principalmente en el navegador, no dentro del contenedor.
- El contenedor sirve la página web, pero la carga principal del juego ocurre en Firefox o Chromium.
- En algunos entornos no se permite aplicar prioridad alta con `renice` negativo.
- En algunos casos `chrt` puede fallar por permisos o restricciones del sistema.
- Un valor extremo en el escenario de CPU saturada elevó el promedio, por eso también se analizó la mediana y el percentil 95.
- Los resultados pueden variar dependiendo de la máquina virtual, cantidad de CPU asignada y navegador utilizado.

---

## Cómo reproducir el proyecto

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd retro-gaming-emulatorjs
```

### 2. Construir la imagen

```bash
podman build -t retro-emulatorjs .
```

### 3. Ejecutar el contenedor

```bash
podman run -d --name retro-web -p 8080:80 retro-emulatorjs
```

### 4. Abrir la aplicación

```text
http://localhost:8080
```

### 5. Ejecutar el juego y medir latencia

Abrir un juego desde el catálogo, iniciar el emulador y presionar las teclas del juego.  
El panel de latencia mostrará las mediciones en pantalla.

Luego descargar los CSV correspondientes a cada escenario.

### 6. Ejecutar el experimento

```bash
chmod +x scripts/experimento_cpu.sh
./scripts/experimento_cpu.sh
```

### 7. Generar gráficos

```bash
python3 scripts/graficar_resultados.py
```

## Conclusiones del proyecto

El proyecto permitió desplegar una aplicación web real usando Podman y medir su comportamiento mediante instrumentación programada.

La medición de latencia entrada-a-frame permitió observar cómo responde el emulador ante eventos de teclado y cómo puede variar su comportamiento bajo diferentes condiciones del sistema.

El escenario con CPU saturada mostró que la carga del procesador puede generar picos de latencia, lo que evidencia la importancia de la planificación de procesos en el sistema operativo.

También se comprobó que modificar prioridades de procesos puede depender de los permisos y restricciones del entorno. Por ello, los intentos fallidos con `renice` negativo o `chrt` también forman parte del análisis técnico del proyecto.

Este trabajo permitió aplicar de forma práctica conceptos como procesos, prioridades, planificación, contenedores, medición de rendimiento y análisis de resultados.

---

## Nota sobre ROMs

Las ROMs usadas en este proyecto son legales/homebrew.


