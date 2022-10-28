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
    com = input ("\nInserire un comando\nScrivere \"help\" per la lista dei comandi\n")
    comando = "x"
    if com == "os":
        comando = "1"
    elif com == "ls":
        comando = "2"
    elif com == "cd":
        path = input ("Inserire il path della destinazione:\n")
        if len(path) > 0:
            comando = "3" + path
        else:
            print ("Path non specificato")
            continue
    elif com == "pwd":
        comando = "4"
    elif com == "cpu":
        comando = "5"
    elif com == "exit":
        comando = "exit"
    elif com == "help":
        cmd_list()
        continue
    else:
        print ("\nComando non riconosciuto\nDigitare il comando \"help\" per la lista dei comandi")
        continue
    connectionSocket.send(comando.encode())
    if comando == "exit":
        break
    messaggio = connectionSocket.recv(1024).decode()
    print ("\n" + messaggio + "\n")
connectionSocket.close()