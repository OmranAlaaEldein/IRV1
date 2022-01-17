import sys
sys.path.insert(0, "../")

# project's root
from os import path
baseUrl = path.join(path.dirname(__file__), '../')

# import socket programming library
import socket

# import thread module
from _thread import *

# import creating index module
from invertedIndexProcess import invertedIndex
from QgramIndexProcess import QgramIndex

# import (Query) Matcher
from MatcherProcess import Matcher

#import threading


class Server :
    def __init__(self):
        #self.print_lock = threading.Lock()
        self.HOST = "127.0.0.1"
        self.PORT = 5050

        # establish socket
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.HOST, self.PORT))

        # create Inverted Index
        self.invertedIX = invertedIndex()
        self.Q_gramIX = QgramIndex(3)

        #read data set
        self.readDataSet()

        #establish matcher
        self.matcher = Matcher(self.invertedIX , self.Q_gramIX)

        # put the socket into listening mode
        self.Socket.listen(5)
        print("socket is listening")


        # a forever loop until client wants to exit
        while True:
            # establish connection with client
            Connecting, addr = self.Socket.accept()

            # lock acquired by client
            #self.print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            start_new_thread(self.threaded, (Connecting,))
        s.close()

    # thread function
    def threaded(self , Connecting):
        while True:

            try:
                # data received from client
                query = Connecting.recv(1024)
                if not query:
                    print('Connector ', Connecting.getpeername(), 'left')

                    # lock released on exit
                    # self.print_lock.release()
                    break
                query = str(query.decode('utf8'))
                print('Query(Client) :', query )

                # parsing query
                self.matcher.parse(False,query)

                Connecting.send(b'Query fetching done!')

            except Exception as e:
                print("error in level argument", e.args[0])
                break

        # connection closed
        Connecting.close()


    def readDataSet(self):
        self.invertedIX.readFromFile(baseUrl + 'dataset/andQueryMatch.txt')
        self.invertedIX.presentIndexOrderByOccur()
        self.Q_gramIX.buildIndex(self.invertedIX)
        print('indexes building done!')





SnapshotServer = Server()