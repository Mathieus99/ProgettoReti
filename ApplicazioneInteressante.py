from msilib.schema import Error
from socket import *
import platform
import os
from psutil._common import bytes2human
import sys
from functions import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind( ('',serverPort) )
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept()
while True:
    comando = connectionSocket.recv(1024).decode()
    # Visualizza info sul sistema operativo e sulla macchina
    if comando == "1":
        messaggio = SystemInfo()
    #Visualizza i file presenti nella directory corrente
    elif comando == "2":
        ls = os.listdir()
        messaggio = ""
        for x in ls:
            messaggio = messaggio + x + "\n"
    #Cambia directory secondo quanto specificato in path
    elif comando[0] == "3":
        path = comando[2:]
        try:
            if path == "":
                os.chdir(".")
                messaggio = "directory cambiata:\n" + os.getcwd()
            else:
                try:
                    os.chdir (path)
                    messaggio = "directory cambiata:\n" + os.getcwd()
                except NotADirectoryError:
                    messaggio = "Not a Directory\n"
        except FileNotFoundError:
            messaggio = "Directory non trovata"
    #Visualizza il percorso della working directory
    elif comando == "4":
        messaggio = os.getcwd()
    #Visualizza info sul processore
    elif comando == "5":
        messaggio = CPUInfo()
    elif comando == "6":
        messaggio = MemoryInfo()
    elif comando == "7":
        messaggio = DiskInfo()
    elif comando[0] == "8":
        readFile = comando[1:]
        try:
            messaggio = open(readFile,"r").read()
        except FileNotFoundError:
            messaggio = "File non trovato\n"
        except Exception:
            messaggio = "Errore nell'apertura del file\n"
    elif comando == "9":
        messaggio = "Sistema: \n" + SystemInfo() + "\nCPU: \n" + CPUInfo() + "\n" + MemoryInfo() + "\nDisks: \n" + DiskInfo() + "\n"
    elif comando == "exit":
        break
    connectionSocket.send(messaggio.encode())
connectionSocket.close()