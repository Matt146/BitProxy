import socket
import threading
import time
import sys

DATAFILE = "datarecved.txt"
PORT = 8008
BUFFSIZE = 1073741824
LOCK = threading.Lock()

def log_data(data):
    with LOCK:
        f = open(DATAFILE, "w")
        f.write(data)
        f.close()

class Client:
    def __init__(self, proxyhost, host, port, request):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxyhost = host
        self.host = host
        self.port = port
        self.request = request
        self.sock.connect((self.proxyhost, PORT))
        self.sock.send("Route".encode("utf-8"))
        self.sock.send(str(self.host).encode("utf-8"))
        self.sock.send(str(self.port).encode("utf-8"))
        self.sock.send(str(self.request).encode("utf-8"))
        self.data_recved = self.sock.recv(BUFFSIZE)
        self.sock.send("CloseConn".encode("utf-8"))
        
def main():
    print(sys.argv[0])
    client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
if __name__ == "__main__":
    main()
