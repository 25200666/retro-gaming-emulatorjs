import os
import pandas as pd
import matplotlib.pyplot as plt

# Rutas a las carpetas usando la estructura oficial de Harold
carpeta_resultados = '../resultados'
carpeta_graficos = '../resultados/graficos'

# Crear la carpeta de gráficos si por alguna razón no existe
os.makedirs(carpeta_graficos, exist_ok=True)

# Cargar los archivos CSV reales del experimento
try:
    df_normal = pd.read_csv(os.path.join(carpeta_resultados, 'normal.csv'))
    df_stress = pd.read_csv(os.path.join(carpeta_resultados, 'cpu_stress.csv'))
    df_baja = pd.read_csv(os.path.join(carpeta_resultados, 'prioridad_baja.csv'))
except Exception as e:
    print(f"Error al cargar los CSV. Asegúrate de tener los archivos reales en resultados/: {e}")
    exit()

# Extraer los datos usando la columna real 'latencia_ms'
datos = [df_normal['latencia_ms'], df_stress['latencia_ms'], df_baja['latencia_ms']]
escenarios = ['Normal', 'CPU saturada', 'Prioridad baja']

# --- 1. Gráfico: Latencia Promedio ---
plt.figure(figsize=(10, 5))
promedios = [d.mean() for d in datos]
plt.bar(escenarios, promedios, color=['#4CAF50', '#F44336', '#FF9800'])
plt.title('Latencia Promedio por Escenario')
plt.xlabel('Escenario')
plt.ylabel('Latencia promedio (ms)')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, 'latencia_promedio.png'))
plt.close()

# --- 2. Gráfico: Percentil 95 ---
plt.figure(figsize=(10, 5))
p95 = [d.quantile(0.95) for d in datos]
plt.bar(escenarios, p95, color=['#4CAF50', '#F44336', '#FF9800'])
plt.title('Percentil 95 de Latencia por Escenario')
plt.xlabel('Escenario')
plt.ylabel('P95 de latencia (ms)')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, 'percentil_95.png'))
plt.close()

# --- 3. Gráfico: Distribución Completa (Boxplot) ---
plt.figure(figsize=(10, 5))
plt.boxplot(datos, labels=escenarios)
plt.title('Distribución de Latencia por Escenario (Boxplot)')
plt.xlabel('Escenario')
plt.ylabel('Latencia (ms)')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, 'distribucion_latencia.png'))
plt.close()

# --- 4. Gráfico: Boxplot Zoom (Hasta 100 ms) ---
plt.figure(figsize=(10, 5))
plt.boxplot(datos, labels=escenarios)
plt.title('Distribución de Latencia hasta 100 ms')
plt.xlabel('Escenario')
plt.ylabel('Latencia (ms)')
plt.ylim(-2, 100)  # Limita el eje Y para apreciar mejor la caja
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, 'distribucion_latencia_100ms.png'))
plt.close()

print("¡Gráficos estadísticos generados con éxito en resultados/graficos/!")
