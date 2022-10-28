from audioop import add
from socket import *
from functions import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind( ('',serverPort) )
serverSocket.listen(1)
print ('Server pronto')
connectionSocket, addr = serverSocket.accept()
print ('Connessione stabilita',addr)
while True:
    com = input ("\nInserire un comando (\"help\" per la lista dei comandi): ")
    comando = "x"
    if com == "os":
        comando = "1"
    elif com == "ls":
        comando = "2"
    elif com == "cd":
        comando = "3" + input("Inserisci path: ")
    elif com == "pwd":
        comando = "4"
    elif com == "cpu":
        comando = "5"
    elif com == "help":
        print (cmd_list())
        continue
    elif com == "exit":
        comando = "exit"
    else:
        print("Comando non riconosciuto\n")
        continue
    connectionSocket.send(comando.encode())
    if comando == "exit":
        print ("Connessione terminata")
        break
    messaggio = connectionSocket.recv(1024).decode()
    print ("\n" + messaggio + "\n")
connectionSocket.close()