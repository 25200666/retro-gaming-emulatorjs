import os
import psutil

def main():

	pid = os.getpid()

	print("PID del programa:", pid)

	for i in range(10):

		cpu = psutil.cpu_percent(1)

		memoria = psutil.virtual_memory().percent

		print("Muestra:", i + 1)
		print("CPU:", cpu, "%")
		print("Memoria:", memoria, "%")
		print("----------------")

main()
