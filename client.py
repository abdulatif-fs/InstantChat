from http import client
import socket
import select
import sys
import pickle
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = input("Login dengan memasukkan nickname: ")
ip = "127.0.0.1"
port = 8080
client.connect((ip, port))

def receive():
    while True:
        try:
            pesan = client.recv(1024).decode('ascii')
            if pesan == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(pickle.loads(pesan))
        except:
            print(f'erorr sodaraa!!!')
            client.close()
            break

def write():
    while True:
        inputan = input("")
        if inputan == '/user':
            client.send(inputan.encode('ascii'))
        else:
            pesan = f'{nickname} : '+ inputan
            dum_pesan = f'{pickle.dumps(pesan)}'
            client.send(dum_pesan.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()