import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen()

sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')


def recieve_message(sender_socket):

	try:
		message_header = sender_socket.recv(HEADER_LENGTH)
		if not len(message_header):
			return False

		message_length = int(message_header.decode('utf-8').strip())
		return {'header': message_header, 'data': sender_socket.recv(message_length)}
	except:
		return False



def send_message(message,reciever_socket):
	message = f"{len(message):<{HEADER_LENGTH}}" + message
	reciever_socket.send(message,"utf-8")
