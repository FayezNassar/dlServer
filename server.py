
import socket

def first_connection():
    s = socket.socket()
    host = socket.gethostname()
    print host
    port = 12345
    s.bind((host, port))
    s.listen(5)
    while True:
       c, addr = s.accept()
       print 'Got connection from', addr
       c.send('Thank you for connecting')
       c.close()

if __name__ == '__main__':
    first_connection()
