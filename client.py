import socket
import select
import errno
import sys
import threading

HEADER_LENGTH = 10
STATUS_LENGTH = 20
keywords=['@list','@file','@quit']

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

def add_status(message, status):
	message_status = f"{status:<{STATUS_LENGTH}}".encode('utf-8')
	return message_status+message

def add_header(message):
	#message = message.encode('utf-8')
	message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
	return message_header+message

def process_message(message):
	message=message.encode('utf-8')
	message=add_status(message,'nothing')
	message=add_header(message)
	return message

def receive_message(sender_socket):
	username_header = client_socket.recv(HEADER_LENGTH)
	if not len(username_header):
		print('Connection closed by the server')
		sys.exit()
	username_length = int(username_header.decode('utf-8').strip())
	username = client_socket.recv(username_length).decode('utf-8')

	message_header = client_socket.recv(HEADER_LENGTH)
	message_length = int(message_header.decode('utf-8').strip())
	message = client_socket.recv(message_length).decode('utf-8')
	return username, message


try:
	client_socket.sendall(process_message(my_username))
except Exception as e:
	print("Server isn't active. Exiting...")
	#sys.exit()

class sendMessage(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#threading.Thread.daemon=True
	def specialmessage(self, message):
		print('you sent a special message')

	def run(self):
		while True:
			message = input()
			if message:
				if message[0]=='@':
					self.specialmessage(message)
				else:	
					message=process_message(message)
					client_socket.sendall(message)	

class acceptMessage(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#threading.Thread.daemon=True

	def run(self):
		#print("receive start")
		while True:
			try:
				while True:
					sender, message = receive_message(client_socket)
					#message = receive_message(client_socket)
					print(sender+'>>'+message)
			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
					print('Reading error: {}'.format(str(e)))
				continue
			except Exception as e:
				print('Reading error: '.format(str(e)))
				sys.exit()							



send = sendMessage()
receive = acceptMessage()
send.start()
receive.start()

# while True:
# 	message = input(f'{my_username} > ')
# 	if message:
# 		message=add_header(message)
# 		client_socket.sendall(message)	
# 	try:
# 		while True:
# 			sender, message = receive_message(client_socket)
# 			#message = receive_message(client_socket)
# 			print(sender+'>>'+message)
# 	except IOError as e:
# 		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
# 			print('Reading error: {}'.format(str(e)))
# 		continue
# 	except Exception as e:
# 		print('Reading error: '.format(str(e)))
# 		sys.exit()					