"""
Create command_input client thread
				^V^
Create server thread
	has clients to all other sites



for each other site
	create new socket connection

"""


import threading
import time
import Queue
import sys

q = Queue.Queue()

import asyncore, socket

# class Server(asyncore.dispatcher):
#     def __init__(self, host, port):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.bind(('', port))
#         self.listen(1)

#     def handle_accept(self):
#         # when we get a client connection start a dispatcher for that
#         # client
#         socket, address = self.accept()
#         print 'Connection by', address
#         EchoHandler(socket)

# class EchoHandler(asyncore.dispatcher_with_send):
#     # dispatcher_with_send extends the basic dispatcher to have an output
#     # buffer that it writes whenever there's content
#     def handle_read(self):
#         self.out_buffer = self.recv(1024)
#         if not self.out_buffer:
#             self.close()


# class Client(asyncore.dispatcher_with_send):
#     def __init__(self, host, port, message):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.connect((host, port))
#         self.out_buffer = message

#     def handle_close(self):
#         self.close()

#     def handle_read(self):
#         print 'Received', self.recv(1024)
#         self.close()


class Client(asyncore.dispatcher_with_send):
    def __init__(self, host, port, message):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.out_buffer = message

    def handle_close(self):
        self.close()

    def handle_read(self):
        print 'Received', self.recv(1024)
        self.close()


class EchoHandler(asyncore.dispatcher_with_send):

	def handle_read(self):
		data = self.recv(8192)
		print "Messaged received"
		if data:
			self.send(data)

class Server(asyncore.dispatcher):

	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)
		print "Server listening"

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print 'Incoming connection from %s' % repr(addr)
			handler = EchoHandler(sock)



class myThread (threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.peers = [int(line.rstrip('\n')) for line in open('peers.txt')]

   
	def run(self):
		
		if self.name == 'commandThread':
			while 1:
				time.sleep(1)
				command = raw_input("Please enter a command: ")
				if command == "tweet":
					self.tweetToAll('cool message')
				elif command == "view":
					print self.peers
				elif command == "quit":
					sys.exit()
				elif command == "unblock":
					unblock()
				else:
					print "Unknown command :(. Try again."
		
		
		elif self.name == 'serverThread':
			# Read commands from Queue
			# listens for incoming connections from peers
			try:
				server = Server('localhost', int(sys.argv[1]))
				asyncore.loop()
			except:
				print "Cannot create server."
				print sys.exc_info()[0]

	def tweetToAll(self, msg):
		print "connecting to", self.peers
		# connectedPeers = []
		for peerPort in self.peers:
			if not peerPort != int(sys.argv[1]):
				print "### Sending", msg, "to", peerPort
				c = Client('', peerPort, "Hello friend")
			
			# connectedPeers.append(c)

		# asyncore.loop()


if __name__ == "__main__":
	

	# Create new threads
	commandThread = myThread("commandThread") # takes in raw_inputs and sends tweets to peers
	serverThread = myThread("serverThread") # handles incoming connections from peers
	# commandThread.daemon = True
	# serverThread.daemon = True

	# # Start new Threads
	commandThread.start()
	serverThread.start()