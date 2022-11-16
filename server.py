from concurrent.futures import thread
import socket
import socketserver
from _thread import *
import pick
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
    pes = pick.pack(pesan)
    for client in clients:
        client.send(pes)

def handle(client, nickname):
    while True:
        try:
            pes = client.recv(1024)
            pesan = pick.unpack(pes)
            if pesan == '/user':
                daf = f'{nickname} : /user \ndaftar user aktif = '
                daf1 = pick.pack(daf)
                print('nickname yang terhubung = ', nicknames)
                for clien in clients:
                    clien.send(daf1)
                    clien.send(pick.pack(nicknames))
                    # for nick in nicknames:
                    #     daftar = '-' + nick 
                    #     # daftar_pack = pick.pack(daftar)
                    #     clien.send(pick.pack(daftar))
                    #     print(nick)
            elif pesan[0] == '/':
                nama = pesan.split(' ')[0]
                penerima = nama.split('/')[1]
                if penerima in nicknames:
                    a = 0
                    for pen in nicknames:
                        if pen == penerima:
                            break
                        else:
                            a = a+1
                    recv = clients[a]

                    kirim = f'{nickname}_private : ' + pesan
                    recv.send(pick.pack(kirim))
                else:
                    kirim = 'nama penerima salah!'
                    client.send(pick.pack(kirim))
            else:
                broadcast(pesan)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} keluar dari room! ')
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f'{str(address)} Terhubung!')

        client.send(pick.pack('NICK'))
        nicknam = client.recv(1024)
        nickname = pick.unpack(nicknam)
        nicknames.append(nickname)
        clients.append(client)

        print(f'nickname client: {nickname}')
        # print('nickname yang terhubung = ', nicknames)
        terhubung = pick.pack('anda terhubung kedalam server!')
        client.send(terhubung)
        broadcast(f'{nickname} join the chat!')
        

        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

receive()