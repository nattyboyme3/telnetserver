import socket, threading
from sys import argv

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', int(argv[1])))
s.listen(1)
s.settimeout(60)

lock = threading.Lock()

welcome_message = 'Type something!'


class Daemon(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        (self.socket, self.address) = socket

    def run(self):
        while True:
            # wait for keypress + enter
            data = self.socket.recv(1024)
            if data == b'\x04':
                break
            print(data.decode("utf-8"), end='')
        # close connection
        self.socket.shutdown(0)
        self.socket.close()


Daemon(s.accept()).start()


