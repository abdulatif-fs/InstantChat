from http import client
import socket
import select
import sys
import pick
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = input("Login dengan memasukkan nickname: ")
ip = "127.0.0.1"
port = 8080
client.connect((ip, port))

def receive():
    while True:
        try:
            pes = client.recv(1024)
            pesan = pick.unpack(pes)
            if pesan == 'NICK':
                client.send(pick.pack(nickname))
            else:
                print(pesan)
                
        except:
            print(f'erorr sodaraa!!!')
            client.close()
            break

def write():
    while True:
        inputan = input("")
        if inputan[0] == '/':
            client.send(pick.pack(inputan))
        else:
            pesan = f'{nickname} : '+ inputan
            dum_pesan = pick.pack(pesan)
            client.send(dum_pesan)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()