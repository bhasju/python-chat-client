import socket
import select
import threading
#from chatroom import Chatroom

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

print(f'Listening for connections on {IP}:{PORT}...')

sockets_list = [server_socket]

#errorprone
client_list = []
message_list = []

readable=[]
writable=[]
exceptional=[]

class clients(threading.Thread):
	def __init__(self, client_socket, client_address, client_username,client_inbox=[],client_outbox=[],disconnected=False):
		threading.Thread.__init__(self)
		threading.Thread.daemon=True
		self.client_socket=client_socket
		self.client_address=client_address
		self.client_username=client_username
		self.disconnected=False
	
	def	check_avl(self):
		for client in exceptional:
			if client == self.client_socket:
				self.disconnected=True

	def check_for_message(self):
		
		message=receive_message(self.client_socket)
		if message==False:
			self.disconnected=True
		else:
			chatroom.message_list.append({'sock':self.client_socket,'username':self.client_username,'message': message})
			print(f"{self.client_username} says {message['data'].decode('utf-8')}")
			# print(chatroom.message_list)
			#test			

	def run(self):
		print(f"{self.client_username} client thread started")
		while self.disconnected==False:
			self.check_avl()
			self.check_for_message()

class Chatroom(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		threading.Thread.daemon=True
		self.client_list=[]
		self.message_list=[]


	def run(self):
		while True:
			if not self.message_list:
				continue
			else:
				for message in self.message_list:
					for client in self.client_list:
						if message['sock'] != client:	
							client.sendall(add_header(message['username'])+message['message']['header']+message['message']['data'])
							
				self.message_list.clear()			
								

def add_header(message):
#takes a string and adds header to it
	message = message.encode('utf-8')
	message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
	return message_header+message

def receive_message(sender_socket):

	try:
		message_header = sender_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False

		message_length = int(message_header.decode('utf-8').strip())
		return {'header': message_header, 'data': sender_socket.recv(message_length)}
	except:
		return False





def accept_new_connection(client_list, sockets_list):
	client_socket, client_address = server_socket.accept()
	client_username = receive_message(client_socket)
	if client_username is False:
		return
	new_client=clients(client_socket=client_socket,client_address= client_address,client_username=client_username['data'].decode('utf-8'))	
	client_list.append(client_socket)	
	new_client.start()
	sockets_list.append(client_socket)

	print('Accepted new connection from {}:{}, username: {}'.format(*client_address, client_username['data'].decode('utf-8')))

chatroom=Chatroom()
chatroom.start()
while True:
	readable, writable, exceptional = select.select(sockets_list, [], sockets_list)
	for notified_socket in readable:
		if notified_socket==server_socket:
			accept_new_connection(chatroom.client_list, sockets_list)
		
