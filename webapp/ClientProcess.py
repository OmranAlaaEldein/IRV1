# Import socket module
import socket

import sys
sys.path.insert(0, "../")

# project's root
from os import path
baseUrl = path.join(path.dirname(__file__), '../')

class Client :

    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 5050

        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.connect((self.HOST, self.PORT))

        while True:
            query = input("What is your query : ")
            # message sent to server
            self.Socket.send(query.encode('utf8'))

            # docs received from server
            data = self.Socket.recv(1024)

            # print the received message
            # here it would be a reverse of sent message
            print('Received from the server :', str(data.decode('utf8')))

            self.readFile( baseUrl + 'OutPut.txt' )
            # ask the client whether he wants to continue
            ans = input('\nDo you want to continue(y/n) :')
            if ans == 'y':
                continue
            else:
                break
        # close the connection
        self.Socket.close()


    def readFile(self , file_name ):
        with open(file_name , encoding='utf8') as file :
            for line in file :
                print(line)




clientRequester = Client()