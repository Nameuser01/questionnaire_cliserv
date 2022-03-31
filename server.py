#!/usr/bin/env python3
# -*- coding: utf8 -*-

host = "localhost"
port= 22255
class ClientThread(threading.Thread):
	def init(self, ip,port clientsocket):
		threading.Thread.init(self)
    	self.ip = ip 
    	self.port = port
    	self.clientsocket = clientsocket
    	print(f"[+] Nouveau thread pour {self.ip}{self.port}")
	
    def run (self):
    	print(f"Connexion de {self.ip} avec le port {self.port}")
    	r = self.clientsocket.recv(2048)
    	print(f"{r.decode()}")
	    print("[-] Client déconnecté")

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_RUSSEADDR, 1)
tcpsock.bind((host, port))

while True:
	tcpsock.listen(10)
	print("En écoute...")
	(clientsocket, (ip, port)) = tcpsock.accept()
	newthread = ClientThread(ip, port, clientsocket) 
	newthread.start()