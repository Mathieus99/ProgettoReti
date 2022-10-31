from msilib.schema import Error
from socket import *
import platform
import os
import psutil
from psutil._common import bytes2human
import sys
from functions import *

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print ("Connessione effettuata\n")
while True:
    comando = clientSocket.recv(1024).decode()
    # Visualizza info sul sistema operativo e sulla macchina
    if comando == "1":
        NetworkName = platform.node()
        macchina = platform.machine()
        piattaforma = platform.platform()
        messaggio = 'OS: ' + piattaforma + '\nNetwork Name: ' + NetworkName + '\nType: ' + macchina
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
            else:
                os.chdir (path)
            messaggio = "directory cambiata:\n" + os.getcwd()
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
    elif comando == "exit":
        print ("Connessione terminata\n")
        break
    clientSocket.send(messaggio.encode())
clientSocket.close()
