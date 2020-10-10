import socket
import select
import threading

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

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
		self.client_socket=client_socket
		self.client_address=client_address
		self.client_username=client_username
		self.client_inbox=[]
		self.client_outbox=[]
		self.disconnected=False
	
	def	check_avl(self):
		for client in exceptional:
			if client == self.client_socket:
				self.disconnected=True

	def check_outbox(self):
		#print("checking outbox")
		#TODO write an inbox busy variable to make chatroom thread wait.
		# for client in readable:
		# 	if client == self.client_socket:
		# 		message=receive_message(self.client_socket)
		# 		if message==False:
		# 			self.disconnected=True
		# 		else:
		# 			self.client_outbox.append(message['data'])
		# 			print(message["data"].decode('utf-8'))#test
		message=receive_message(self.client_socket)
		if message==False:
			self.disconnected=True
		else:
			self.client_outbox.append(message['data'].decode('utf-8'))
			print(self.client_outbox)
			print(message["data"].decode('utf-8'))#test			

	def check_inbox(self):
		#print("checking inbox")
		#TODO write an inbox busy variable to make chatroom thread wait.
		for message_data in self.client_inbox:
			send_message(self.client_socket, message_data)
		self.client_inbox.clear()


	def run(self):
		print("client thread started")
		while self.disconnected==False:
			self.check_avl()
			self.check_outbox()
			self.check_inbox()



class chatroom(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.client_list=[]

	def clear_outbox(self,sender_client):
		for client in client_list:
			if client !=sender_client:
				client.client_inbox.extend(sender_client.client_outbox)
		client.client_outbox.clear()		

	def run(self):
		print(self.client_list)
		while True:
			#print(self.client_list)
			for client in client_list:
				clear_outbox(client)
				

print(f'Listening for connections on {IP}:{PORT}...')

class message:
	"""docstring for message"""
	def __init__(self, sender, content):
		self.sender = sender
		self.content = content




def receive_message(sender_socket):

	try:
		message_header = sender_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False

		message_length = int(message_header.decode('utf-8').strip())
		return {'header': message_header, 'data': sender_socket.recv(message_length)}
		print("message received")
	except:
		return False



def send_message(message_data,reciever_socket):
	message = f"{len(message_data):<{HEADER_LENGTH}}" + message_data
	reciever_socket.send(message,"utf-8")


def accept_new_connection(client_list, sockets_list):
	client_socket, client_address = server_socket.accept()
	client_username = receive_message(client_socket)
	if client_username is False:
		return
	new_client=clients(client_socket=client_socket,client_address= client_address,client_username=client_username['data'].decode('utf-8'))	
	client_list.append(new_client)	
	new_client.start()
	sockets_list.append(client_socket)

	print('Accepted new connection from {}:{}, username: {}'.format(*client_address, client_username['data'].decode('utf-8')))

chatroom=chatroom()
chatroom.start()
while True:
	readable, writable, exceptional = select.select(sockets_list, [], sockets_list)
	for notified_socket in readable:
		if notified_socket==server_socket:
			accept_new_connection(chatroom.client_list, sockets_list)
		# else:
		# 	load_message(message_list)

			