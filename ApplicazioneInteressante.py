from socket import *
import os
from functions import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind( ('',serverPort) )
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept()
while True:
    messaggio = ""
    comando = connectionSocket.recv(1024).decode()
    # Visualizza info sul sistema operativo e sulla macchina
    if comando == "1":
        messaggio = SystemInfo()
    #Visualizza i file presenti nella directory corrente
    elif comando == "2":
        ls = os.listdir()
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
    #Esegue il download di un file della cwd
    elif comando[0] == "5":
        readFile = comando[1:]
        file = open(readFile,"rb")
        try:
            messaggio = file.read()
        except FileNotFoundError:
            messaggio = "File non trovato\n"
        except Exception:
            messaggio = "Errore nell'apertura del file\n"
    #Termina
    elif comando == "exit":
        break
    if comando[0] == "5":
        connectionSocket.sendall(messaggio)
    else:
        connectionSocket.send(messaggio.encode())
connectionSocket.close()