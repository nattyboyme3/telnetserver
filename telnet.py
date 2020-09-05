import socket, threading
from sys import argv

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(argv[1])
port = 11911
s.bind(('', port))
s.listen(1)
s.settimeout(600)

lock = threading.Lock()
ends = [b'\x04', b'\xff\xec', b'\x1d\r\n']


class Daemon(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        (self.socket, self.address) = socket

    def run(self):
        print('Connected: {}'.format(self.address))
        self.socket.send("Welcome!\r\n".encode("utf-8"))
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            if data in ends:
                break
            try:
                utf_data = data.decode("utf-8")
                if '\r\n' in utf_data:
                    return_string = ''
                else:
                    return_string = '\r\n'

                utf_data = utf_data.replace('\r\n','')
                print(utf_data, end='')
                return_string = return_string + f'Received: \'{utf_data}\'\r\n'
                self.socket.send(f'Received: \'{utf_data}\'\r\n'.encode("utf-8"))
            except UnicodeDecodeError:
                pass
        # close connection
        self.socket.shutdown(0)
        self.socket.close()


Daemon(s.accept()).start()


