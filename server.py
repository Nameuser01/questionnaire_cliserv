#!/usr/bin/env python3
import socket
import threading
from simplecrypt import decrypt

# CONNECTION INFORMATIONS
host = "0.0.0.0"
port = 55555

class ClientThread(threading.Thread):


    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print(f"[+] Nouveau thread pour {self.ip} {self.port}")


    def run(self):
        print(f"Connexion de {self.ip} avec le port {self.port}")
        r = self.clientsocket.recv(2048)
        message = r
        result = decrypt("secretpassword", message)
        print(result)
        result = result.decode("utf-8")
        print(result)
        f = open(f"{self.ip}.dat", "a")
        f.write(f"{result}")
        f.close()
        print("[-] Client déconnecté...")


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((host, port))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()