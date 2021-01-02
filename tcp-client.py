#! /usr/bin/env python3
# TCP Echo Client

import sys
import socket
import datetime, time
import webbrowser
# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
url = sys.argv[3]
count = 1000000
req = 'GET /' + url + 'HTTP/1.1\\r\\n';
hos = 'Host: ' + str(host) + ':' + str(port) + '\\r\\n';
end = '\\r\\n ';
name = 'cache' + url
t = datetime.datetime.now(datetime.timezone.utc)
date = t.strftime("%a, %d %b %Y %H:%M:%S %Z\\r\\n")

# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create TCP connection to server
print("Connecting to " + host + ", " + str(port))
clientSocket.connect((host, port))

# try to find cached file
try:
    with open(name) as f:
        first = f.readline()
    mod = first[19:-4]
    print(mod)
    # Send encoded data through TCP connection
    data = req + hos + mod + end
    print("Sending data to server:   " + data)
    clientSocket.send(data.encode())

    # Receive the server response
    dataEcho = clientSocket.recv(count)
    # Display the decoded server response as an output
    print("Receive data from server: " + dataEcho.decode())
    dataEcho = dataEcho.decode()
    datas = dataEcho.split("\\r\\n")
    if ('304' in datas[0]):
        print('not modified')
        webbrowser.open_new_tab(name)
    elif ('200' in datas[0]):
        os.remove(name)
        print('webpage returned')
        caches = open(name, "w")
        caches.write('<!--'+ datas[2] + '-->\n')
        caches.write(datas[-1])
        caches.close()
        webbrowser.open_new_tab(name)
        print('cache successfully created')
    elif ('404' in datas[0]):
        print('webpage does not exist')
    else:
        print('error in code')

#if cached file does not exist
except FileNotFoundError:
    print('file not found')
    data = req + hos + end
    print("Sending data to server:   " + data)
    clientSocket.send(data.encode())

    # Receive the server response
    dataEcho = clientSocket.recv(count)  
    # Display the decoded server response as an output
    temp = dataEcho.decode()
    print("Receive data from server: " + temp)
    tempSplit = temp.split('\\r\\n')
    print(tempSplit[0])
    if ('304' in tempSplit[0]):
        print('not modified')
        webbrowser.open_new_tab(name)
    elif ('200' in tempSplit[0]):
        print('webpage returned')
        caches = open(name, "w")
        caches.write('<!--'+ tempSplit[2] + '-->\n')
        caches.write(tempSplit[-1])
        caches.close()
        webbrowser.open_new_tab(name)
        print('cache successfully created')
    elif ('404' in tempSplit[0]):
        print('webpage does not exist')
    else:
        print('error in code')
# Close the client socket
clientSocket.close()
    


