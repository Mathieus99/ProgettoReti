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
        nodo = platform.node()
        macchina = platform.machine()
        processore = platform.processor()
        piattaforma = platform.platform()
        sistema = platform.system() + platform.release()
        versione = platform.version()
        messaggio = nodo + '\n' + macchina + '\n' + processore + '\n' + piattaforma + '\n' + sistema + ' versione: ' + versione
    elif comando == "2":
        ls = os.listdir()
        messaggio = ""
        for x in ls:
            messaggio = messaggio + x + "\n"
    elif comando[0] == "3":
        path = comando[1:]
        os.chdir (path)
        messaggio = "directory cambiata"
    elif comando == "4":
        messaggio = os.getcwd()
    elif comando == "5":
            times = psutil.cpu_times()
            messaggio = "time spent by normal processes executing in user mode: " + str(times[0]) + "\ntime spent by processes executing in kernel mode: " + str(times[1]) + "\ntime spent doing nothing: " + str(times[2]) + "\ntime spent for servicing hardware interrupts: " + str(times[3]) + "\ntime spent servicing deferred procedure calls: " + str(times[4]) + "\n\n"
            messaggio = messaggio + "Number of logical cores in the system: " + str(psutil.cpu_count(logical=True)) + "\nNumber of phisical cores in the system: " + str(psutil.cpu_count(logical=False)) + "\n\n"
            messaggio = messaggio + "CPU percent " + str(psutil.cpu_percent()) + "\n\n"
            stats = psutil.cpu_stats()
            messaggio = messaggio + "number of context switches (voluntary + involuntary) since boot " + str(stats[0]) + "\nnumber of interrupts since boot " + str(stats[1]) + "\nnumber of software interrupts since boot " + str(stats[2]) + "\nnumber of system calls since boot " + str(stats[3]) + "\n\n"
            freq = psutil.cpu_freq()
            messaggio = messaggio + "CPU frequency\n\tcurrent " + str(freq[0]) + "\n\tmin " + str(freq[1]) + "\n\tmax " + str(freq[2])
    elif comando == "exit":
        break
    clientSocket.send(messaggio.encode())
clientSocket.close()
