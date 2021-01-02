#! /usr/bin/env python3
# TCP Echo Server

import sys
import socket
import os.path
import time, datetime

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
dataLen = 1000000
t = datetime.datetime.now(datetime.timezone.utc)
date = t.strftime("%a, %d %b %Y %H:%M:%S %Z\\r\\n")

# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port:  ' + str(serverPort) + '\n')

# loop forever listening for incoming connection requests on "welcoming" socket
while True:
    # Accept incoming connection requests; allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    print("Socket created for client " + address[0] + ", " + str(address[1]))

    # Receive and print the client data in bytes from "data" socket
    data = connectionSocket.recv(dataLen).decode()
    print("Data from client: " + data)
    
    datas = data.split('\\r\\n')
    print(len(datas))
    
    fName = datas[0][5:-8]
    print(fName)
    try:
        f = open(fName, "r")
        file = f.read()
        f.close()
        if (len(datas[2]) > 12):
            mod = datas[2] + '\\r\\n'
            print(mod)
            t1 = time.strptime(mod, "%a, %d %b %Y %H:%M:%S %Z\\r\\n")
            secs1 = time.mktime(t1)
        print(file)
        length = len(file)
        #get last modified
        secs2 = os.path.getmtime(fName)
        t2 = time.gmtime(secs2)
        last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\\r\\n")
        print(last_mod_time)
        #check whether conditional get
        if ('GMT' in datas[2]):
            print('im here')
            t = time.strptime(last_mod_time, "%a, %d %b %Y %H:%M:%S %Z\\r\\n")
            if (secs1 < secs2):
                ret = 'HTTP/1.1 200 OK\\r\\nDate: ' + date + 'Last-Modified: ' + last_mod_time + 'Content-Length: ' + str(length) +'\\r\\nContent-Type: text/html; charset=UTF=8\\r\\n\\r\\n ' + file
            else:
                ret = 'HTTP/1.1 304 Not Modified\\r\\nDate: ' + date + '\\r\\n '
        else:
                ret = 'HTTP/1.1 200 OK\\r\\nDate: ' + date + 'Last-Modified: ' + last_mod_time + 'Content-Length: ' + str(length) +'\\r\\nContent-Type: text/html; charset=UTF=8\\r\\n\\r\\n ' + file
        # Echo back to client
        connectionSocket.send(ret.encode())
    except FileNotFoundError:
        ret = 'HTTP/1.1 404 Not Found\\r\\nDate: ' + date +'Content-Length: 0\\r\\n \\r\\n '
        connectionSocket.send(ret.encode())

        
