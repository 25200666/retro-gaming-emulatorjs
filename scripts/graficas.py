import pandas as pd
import matplotlib.pyplot as plt

def main():

	datos = pd.read_csv("../datos/mediciones.csv")

	plt.plot(datos["cpu"])

	plt.title("Uso de CPU")

	plt.xlabel("Muestras")

	plt.ylabel("CPU (%)")

	plt.grid()

	plt.savefig("../evidencias/cpu.png")

	print("Grafica creada correctamente")

main()
