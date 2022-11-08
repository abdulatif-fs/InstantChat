from concurrent.futures import thread
import socket
import socketserver
from _thread import *
import pickle
import select
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


ip = "127.0.0.1"
port = 8080

server.bind((ip, port))
server.listen(5)
print( '%s is Activated ...' % ip)
print('Listening on port %s ...' % port)
clients = []
nicknames =[]

def broadcast(pesan):
    # dum_pesan = pickle.dumps(pesan)
    for client in clients:
        client.send(pesan)

def handle(client):
    while True:
        try:
            pesan = client.recv(1024).decode('ascii')
            
            if pesan == '/user':
                for clien in clients:
                    clien.send('daftar user aktif = '.encode('ascii'))
                    for nick in nicknames:
                        daftar = nick + ' \n'
                        clien.send(daftar.encode('ascii'))
            else:
                load_pesan = f'{pickle.loads(pesan)}'
                broadcast(load_pesan.encode('ascii'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} keluar dari room! '.encode('ascii'))
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f'{str(address)} Terhubung!')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'nickname client: {nickname}')
        client.send(f'terhubung kedalam server!'.encode('ascii'))
        broadcast(f'{nickname} join the chat!'.encode('ascii'))
        

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()