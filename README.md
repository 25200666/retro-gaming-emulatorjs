
# Retro Gaming Web con Podman y EmulatorJS

Proyecto Final de Sistemas Operativos I basado en el *Proyecto 5: Retro-gaming web con EmulatorJS*.
Este proyecto consiste en crear una aplicación web de retro-gaming usando *EmulatorJS, desplegada con **Podman rootless* y complementada con instrumentación programada para medir la *latencia entrada-a-frame* durante la ejecución de juegos retro.

El objetivo principal es demostrar lo aprendido en el curso mediante conceptos relacionados con *procesos, planificación de CPU, uso de recursos, prioridades y medición de rendimiento*.

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

La aplicación permite ejecutar juegos retro desde el navegador mediante *EmulatorJS*.  
El servidor web se ejecuta dentro de un contenedor *Podman* utilizando *Nginx*.

El proyecto no solo consiste en ejecutar juegos retro en un emulador web, sino también en medir cómo cambia la respuesta del emulador cuando el sistema operativo se encuentra en distintos escenarios:

- Escenario normal.
- Escenario con CPU saturada.
- Escenario con prioridad baja del navegador.
- Intento de prioridad alta o política de tiempo real, cuando el sistema lo permite.

La métrica principal del proyecto es la *latencia entrada-a-frame*.

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
