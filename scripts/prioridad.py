import os
import psutil

def main():
	pid = os.getpid()

	proceso = psutil.Process(pid)

	prioridad = proceso.nice()

	print("PID:", pid)
	print("Prioridad (nice):", prioridad)

main()
