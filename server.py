import socket
import threading
import time

PORT = 8008
MAX_CONNS = 800
IPFILE = "ip.txt"
LOCK = threading.Lock()
BUFFSIZE = 1073741824

def log_ip(addr):
    with LOCK:
        f = open(IPFILE, "a")
        f.write(str(addr))
        f.close()

class Router:
    def __init__(self, conn, host, port, request):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.sock.connect((self.host, self.port))
        self.sock.send(request.encode("utf-8"))
    def conn_handler(self):
        data = self.sock.recv(BUFFSIZE)
        self.sock.close()

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ""
        self.port = PORT
        self.sock.bind((self.host, self.port))
        self.listener()
    def listener(self):
        for x in range(MAX_CONNS):
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
            log_ip(self.addr)
            threading.Thread(target=self.recver, args=(self.conn,)).start()
    def recver(self, conn):
        while True:
            data = conn.recv(BUFFSIZE).decode("utf-8")
            if data == "Route":
                # deal with routing
                host = conn.recv(BUFFSIZE).decode("utf-8")
                port = int(conn.recv(BUFFSIZE).decode("utf-8"))
                request = conn.recv(BUFFSIZE).decode("utf-8")
                Router(conn, host, port, request)
            if data == "CloseConn":
                conn.close()
            
def main():
    server = Server()
    
if __name__ == "__main__":
    main()
            
