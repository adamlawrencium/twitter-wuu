"""
Create command_input client thread
				^V^
Create server thread
	has clients to all other sites



for each other site
	create new socket connection

"""


import threading
import signal
import time
import sys
import asyncore, socket

class Client(asyncore.dispatcher_with_send):
	def __init__(self, host, port, message):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.port = port
		self.connect((host, port))
		self.out_buffer = message
		self.message = message

	def handle_close(self):
		self.close()

	def handle_read(self):
		print 'Received', self.recv(1024)
		self.close()

	# def handle_write(self):
	# 	# self.send(self.message)
	# 	# self.close()
	# 	pass

	def handle_error(self):
		print "Can't connect to peer at %s:%s" % (self.host, self.port)


class EchoHandler(asyncore.dispatcher_with_send):
	def handle_read(self):
		data = self.recv(8192)
		if data:
			print "Received message:", data.rstrip('\n')
			self.send("Thank you for the message.\n")

class Server(asyncore.dispatcher_with_send):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)
		print "Server listening at", host, port

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print 'Incoming connection from %s' % repr(addr)
			handler = EchoHandler(sock)

	# def handle_read(self):
	# 	data = self.recv(8192)
	# 	print "Messaged received"
	# 	if data:
	# 		self.send(data)
	# 		# self.close()


# Main thread wrapper class
class myThread (threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		# The shutdown_flag is a threading.Event object that indicates whether the thread should be terminated.
		self.shutdown_flag = False
		self.name = name
		self.peers = [int(line.rstrip('\n')) for line in open('peers.txt')]

	def run(self):
		# Enter while loop accepting the following commands
		if self.name == 'commandThread':
			while 1:
				time.sleep(0.5)
				command = raw_input("Please enter a command:\n")
				if command[:6] == "tweet ":
					self.tweetToAll(command[6:])
				elif command == "view":
					print self.peers
				elif command == "quit":
					self.shutdown_flag = True
					raise KeyboardInterrupt
					self.shutdown_flag = True
				elif command == "unblock":
					unblock()
				else:
					print "Unknown command :(. Try again."

		# Start the server the listening for incoming connections
		elif self.name == 'serverThread':
			server = Server('localhost', int(sys.argv[1]))
			if self.shutdown_flag != True:
				asyncore.loop()

	# Connect to all peers send them <msg>
	def tweetToAll(self, msg):
		for peerPort in self.peers: # avoid connecting to self
			if peerPort != int(sys.argv[1]):
				# print "### Sending", msg, "to", peerPort
				c = Client('', peerPort, msg) # send <msg> to localhost at port <peerPort>
				asyncore.loop(count = 1)


class ServiceExit(Exception):
	"""
	Custom exception which is used to trigger the clean exit
	of all running threads and the main program.
	"""
	pass
 
 
def service_shutdown(signum, frame):
	print('Caught signal %d' % signum)
	raise ServiceExit


if __name__ == "__main__":	

	# Register the signal handlers
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)

	# Create new threads
	commandThread = myThread("commandThread") # takes in raw_inputs and sends tweets to peers
	commandThread.setDaemon(True)
	serverThread = myThread("serverThread") # handles incoming connections from peers
	serverThread.setDaemon(True)

	# # Start new Threads
	commandThread.start()
	serverThread.start()

	# keep main thread alive
	while True:
		# print threading.activeCount()
		time.sleep(3)