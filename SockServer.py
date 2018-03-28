#!/usr/bin/python
import socket
import threading

class SockServer(object):
    def __init__(self, host, port):
	self.clients=set()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(500)
        while True:
            client, address = self.sock.accept()
	    self.clients.add(client)
            threading.Thread(target = self.listenToClient,args = (client, address)).start()
	    
    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    for other in self.clients:
			if  other != client:
				other.send(data)
		else:
		    self.clients.remove(client)
		    client.close()

	    except:
                client.close()
		try: 
		    self.clients.remove(client)
		except:
		    pass
                


SockServer('localhost',8000)
