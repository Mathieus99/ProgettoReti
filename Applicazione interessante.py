from socket import *
import platform
import os
import psutil
import sys
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while True:
    comando = clientSocket.recv(1024).decode()
    # Visualizza info sul sistema operativo e sulla macchina
    if comando == "1":
        NetworkName = platform.node()
        macchina = platform.machine()
        piattaforma = platform.platform()
        messaggio = 'OS: ' + piattaforma + '\nNetwork Name: ' + NetworkName + '\nType: ' + macchina
    elif comando == "2":
        ls = os.listdir()
        messaggio = ""
        for x in ls:
            messaggio = messaggio + x + "\n"
    elif comando[0] == "3":
        path = comando[2:len(comando)]
        print(path)
        os.chdir (path)
        messaggio = "directory cambiata:\n" + os.getcwd()
    elif comando == "4":
        messaggio = os.getcwd()
    elif comando == "5":
            cpu = platform.processor()
            freq = psutil.cpu_freq()
            times = psutil.cpu_times()
            messaggio = "CPU: " + cpu + "\nCPU frequency: " + str(freq[0]) + " MHz (current) , " + str(freq[2]) + " MHz (max)\n"
            messaggio = messaggio + "Logical Cores: " + str(psutil.cpu_count(logical=True)) + "\nPhysical Cores: " + str(psutil.cpu_count(logical=False)) + "\n"
            messaggio = messaggio + "CPU percent: " + str(psutil.cpu_percent()) + "%\n"
            messaggio = messaggio + "Times\nUser Mode: " + str(times[0]) + "\nKernel Mode: " + str(times[1]) + "\nIdle: " + str(times[2]) + "\nServicing HW Interrupts: " + str(times[3]) + "\nServicing procedure calls: " + str(times[4]) + "\n"
            stats = psutil.cpu_stats()
            messaggio = messaggio + "Stats\nContext switches (voluntary + involuntary)(since boot): " + str(stats[0]) + "\nInterrupts (since boot): " + str(stats[1]) + "\nSoftware interrupts (since boot): " + str(stats[2]) + "\nSystem calls (since boot): " + str(stats[3]) + "\n"
    elif comando == "exit":
        break
    clientSocket.send(messaggio.encode())
clientSocket.close()
