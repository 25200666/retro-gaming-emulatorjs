
import psutil
import csv
from datetime import datetime

def main():

	archivo = open("../datos/mediciones.csv", "w", newline="")

	escritor = csv.writer(archivo)

	escritor.writerow(["hora", "cpu", "memoria"])

	for i in range(20):

		hora = datetime.now()

		cpu = psutil.cpu_percent(1)

		memoria = psutil.virtual_memory().percent

		escritor.writerow([hora, cpu, memoria])

		archivo.flush()

		print("Hora:", hora)
		print("CPU:", cpu, "%")
		print("Memoria:", memoria, "%")
		print("-------------------")

main()
