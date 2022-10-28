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
    print (com[3:len(com)])
    comando = "x"
    if com == "os":
        comando = "1"
    elif com == "ls":
        comando = "2"
    #Cambia directory inserendo la directory destinazione dopo cd (cd directory)
    elif com[0:2] == "cd":
        comando = "3" + com[2:len(com)]
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