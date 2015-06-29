'''
Created on Jun 25, 2015

@author: puneeth

References:
http://www.tutorialspoint.com/python/python_command_line_arguments.htm
http://codereview.stackexchange.com/questions/52701/proxy-using-socket-doubts-on-multithreading-and-connection-closing
https://docs.python.org/3.1/howto/sockets.html
http://ilab.cs.byu.edu/python/threadingmodule.html
http://ruslanspivak.com/lsbaws-part1/
http://learnpythonthehardway.org/book/ex15.html
http://www.december.com/html/tutor/hello.html
http://www.tutorialspoint.com/python/python_multithreading.htm

'''

import socket
import thread
import argparse

server_log = 'log/server_log.txt'

def server_function(connectionSocket, addr):
    try:
        log = open(server_log, 'a')
        
        request = connectionSocket.recv(1024)
#         print type(request)
#         print request
        
        log.write('\n')
        log.write(request)
        log.write('----------')
        log.close()
            
        filename = request.split()[1]
#         print'filename', filename[1:], len(filename)
                        
        try:
            if len(filename) == 1:
                http_response = """\
HTTP/1.1 200 OK

<html>
    <body>
        Welcome to HttpServer Project
    </body>
</html>
"""
                connectionSocket.sendall(http_response)
                connectionSocket.close()
            
            if len(filename) > 1:
                f = open(filename[1:], 'r')
                outputdata = f.readlines()
                
                http_response = """\
HTTP/1.1 200 OK

"""                            
                connectionSocket.sendall(http_response)
                
                for i in range(0, len(outputdata)):
                    connectionSocket.sendall(outputdata[i])
                
                f.close()
                connectionSocket.close()
        
        except IOError:
            http_response = """\
HTTP/1.1 404 Not Found

<html>
    <body>
        404 File Not Found
    </body>
</html>
"""
            connectionSocket.sendall(http_response)
            connectionSocket.close()

    except IOError:
        http_response = """\
HTTP/1.1 404 Not Found

<html>
    <body>
        404 Server Not Found
    </body>
</html>
"""
        connectionSocket.sendall(http_response)
        connectionSocket.close()

def main(port):
    HOST = '127.0.0.1'
#     try:
#         PORT = int(raw_input("Enter port number"))
#     except ValueError:
#         PORT = 8080
        
    PORT = port
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    
    print('Serving on %s ' % PORT)
    while True:
        print('\nReady to serve...')
        
        connectionSocket, addr = serverSocket.accept()
        
        thread.start_new_thread(server_function, (connectionSocket, addr))
         
    serverSocket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Client for HttpServer.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port on the server.'
    )
    args = parser.parse_args()
    main(args.port)