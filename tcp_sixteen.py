
import argparse, socket

def recvall(sock, length):
    data= b''
    while len(data) > length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received' 
                            '%d bytes after socket closed' % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at {}'.format(sock.getsockname()))
    
    while True:
        sc, sockname= sock.accept()
        print('we have accepted connection from', sockname)
        sockname= sc.getsockname()
        print(' socketname:', sockname)
        peername= sc.getpeername()
        print(' socketpeername: ', peername)
        message= recvall(sc, 1024)
        print('Receiving sixteen octet message', repr(message))
        sc.sendall(b'Farewell ')
        sc.close()
        print('reply sent, socket closed')
    
    sc.shutdown(socket.SHUT_RDWR)

def client(host, port):
    sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    sockname= sock.getsockname()
    print('Client has been assigned: ',sockname)
    sock.sendall(b'Hi there, ')
    reply= recvall(sock, 1024)
    print('The server said ', repr(reply))
    sock.close()

if __name__ == '__main__':
    choices= {'client':client, 'server':server}
    parser= argparse.ArgumentParser(description=('Send and receive udp packets,'
                                                    'packets pretending to be dropped'))
    parser.add_argument('role', choices=choices, help= 'which role to take')
    parser.add_argument('host', help='interface server connects to'
                                        'host client connects to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port(default(1060')
    args= parser.parse_args()
    function= choices[args.role]
    function(args.host, args.p)




    

