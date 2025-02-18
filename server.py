
import socket
import threading
import time

#declaring constats

#if ypu are testing this on local macine then use same value for the variable in client script 
server_ip = socket.gethostbyname(socket.gethostname()) 

server_port = 9090
encoder = "ascii"
bytesize = 1024

clients = []
nicknames =[]

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((server_ip,server_port))

server_socket.listen()

print(f"Server is listening on {server_ip}:{server_port}....\n")

def broadcast(message,client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode(encoder))

def handle_clients(client_socket,client_address):
    while True:
        try:
            message= client_socket.recv(bytesize).decode(encoder)
            index = clients.index(client_socket)
            nickname=nicknames[index]
            print(f"{nickname}: {message}")
            broadcast(f"{nickname}: {message}",client_socket)
        
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            nickname =nicknames.pop(index)
            broadcast(f"{nickname} left ..................",None)
            break



def server_message():
    while True:
        if clients:
            message = input()
            broadcast(message,None)
        else:
            time.sleep(2)

server_thread = threading.Thread(target=server_message)
server_thread.daemon = True
server_thread.start()


while True:
    client_socket , client_address = server_socket.accept()
    client_socket.send("NICKNAME".encode(encoder))
    nickname = client_socket.recv(bytesize).decode(encoder)
    print(f"Connected with {nickname}({client_address})")
    nicknames.append(nickname)
    clients.append(client_socket)

    broadcast(f"{nickname} joined .......",None)
    client_socket.send(f"You are now connected to server ({server_ip})\n".encode(encoder))

    thread = threading.Thread(target=handle_clients,args=(client_socket,client_address))
    thread.start()



