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
import dill
import pickle
import datetime
from user import User

names_ = [line.rstrip('\n').split(' ')[0] for line in open('EC2-peers.txt')]
ec2ips_ = [line.rstrip('\n').split(' ')[1] for line in open('EC2-peers.txt')]
peers_ = [int((line.rstrip('\n')).split(' ')[2]) for line in open('EC2-peers.txt')]


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
	# 	self.send(self.message)
	# 	self.close()
	# 	pass

	def handle_error(self):
		print "Can't connect to peer at %s:%s" % (self.host, self.port)



class EchoHandler(asyncore.dispatcher_with_send):
	def handle_read(self):
		data = self.recv(8192)
		if data:
			serializedMessage = dill.loads(data)

			hey = site.receive(serializedMessage[0],serializedMessage[1],serializedMessage[2])
			#print "Received message:", data.rstrip('\n')
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
			sender = 0
			for index, ip in enumerate(ec2ips_):
				if ip == repr(addr)[0]:
					sender = index
			print 'Recieved message from %s' % names_[sender]
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
		# self.peers = [int(line.rstrip('\n')) for line in open('peers.txt')]
		# self.names = [line.rstrip('\n') for line in open('names.txt')]
		
		self.peers = [int((line.rstrip('\n')).split(' ')[2]) for line in open('EC2-peers.txt')]
		self.names = [line.rstrip('\n').split(' ')[0] for line in open('EC2-peers.txt')]
		self.ec2ips = [line.rstrip('\n').split(' ')[1] for line in open('EC2-peers.txt')]


	def run(self):
		# Enter while loop accepting the following commands
		if self.name == 'commandThread':
			while 1:
				time.sleep(0.2)
				command = raw_input("\nPlease enter a command:\n")
				if command[:6] == "tweet ":
					messageBody = command[6:]
					utcDatetime = datetime.datetime.utcnow()
					utcTime = utcDatetime.strftime("%Y-%m-%d %H:%M:%S")

					messageData = site.tweet(command[6:], utcTime)
					sendingPorts = site.nonBlockedPorts()
					self.tweetToAll(messageData, sendingPorts)
				elif command == "view":
					site.view()
				elif command == "quit":
					self.shutdown_flag = True
					raise KeyboardInterrupt
					self.shutdown_flag = True
				elif command == "unblock ":
					name = command[6:]
					siteName = sys.argv[2]
					for i in range(0,len(self.names)):
						if (name == names[i]):
							name = self.peers[i]
							break
					utc_datetime = datetime.datetime.utcnow()
					utcTime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
					site.unblock(utcTime,(int(name[0])-1))

				elif command[:6] == "block ":
					name = command[6:]
					siteName = sys.argv[2]
					for i in range(0,len(self.names)):
						if (name == self.names[i]):
							name = self.peers[i]
							break
					utc_datetime = datetime.datetime.utcnow()
					utcTime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
					print "Blocking User: "+command[6:]
					site.block(utcTime,(int(name[0])-1))
				elif command == "View Log":
					site.viewPartialLog()
				elif command == "View Clock":
					site.viewMatrixClock()


				else:
					print "Unknown command %s :(. Try again." % (command)

		# Start the server the listening for incoming connections
		elif self.name == 'serverThread':
			server = Server('0.0.0.0', int(sys.argv[1]))
			if self.shutdown_flag != True:
				asyncore.loop()

	# Connect to all peers send them <msg>
	def tweetToAll(self, msg, sendingPorts):
		for index, peerPort in enumerate(self.peers): # avoid connecting to self
			if peerPort != int(sys.argv[1]) and len(sendingPorts) == len(self.peers):
				# print "### Sending", msg, "to", peerPort
				fullMessage = site.send(msg, peerPort)
 				dilledMessage = dill.dumps(fullMessage)
				c = Client(self.ec2ips[index], peerPort, dilledMessage) # send <msg> to localhost at port 5555
				asyncore.loop(timeout = 5, count = 1)
			else:
				nonBlockedPorts = site.nonBlockedPorts()
				check = (peerPort in nonBlockedPorts)
				# print check
				if peerPort != int(sys.argv[1]) and len(nonBlockedPorts) > 0 and check:
					fullMessage = site.send(msg, peerPort)
	 				dilledMessage = dill.dumps(fullMessage)
					c = Client(self.ec2ips[index], peerPort, dilledMessage) # send <msg> to localhost at port <peerPort>
					asyncore.loop(timeout =5, count = 1)



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

	"""
	program usage:				-change to->
		arg 0: twitter.py (duh)							--> twitter.py
		arg 1: local port										--> local port
		arg 2: name													--> 'Alice'

		local port needs to match port of current EC2 instance
	"""


	# Register the signal handlers
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)

	# Create new threads
	commandThread = myThread("commandThread") # takes in raw_inputs and sends tweets to peers
	commandThread.setDaemon(True)
	serverThread = myThread("serverThread") # handles incoming connections from peers
	serverThread.setDaemon(True)



	# Try loading from pickle file
	allIds = None
	site = None
	try:
		# Create user from pickle
		pickledUser = pickle.load( open( "pickledUser.p", "rb" ) )
		allIds = commandThread.peers
		site = User(sys.argv[2][0], allIds, True, pickledUser)
	except IOError:
		print "Site pickle doesn't exist. Creating user from scratch."
		allIds = commandThread.peers
		site = User(sys.argv[2][0], allIds, False, None)




	# # Start new Threads
	commandThread.start()
	serverThread.start()

	# keep main thread alive
	while True:
		# print threading.activeCount()
		time.sleep(3)
