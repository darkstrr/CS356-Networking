#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
#nums = int(sys.argv[3])
request = ""
ret = ""
fou = False
f = open('dns-master.txt', "r")
lines = [line for line in f.readlines()]
f.close;

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)
    print("Receive data from client " + address[0] + ", " + str(address[1]))
    # separate data into question and number
    #info = data.decode('ascii').split(",")
    message = struct.unpack('!hhihh', data[:12])
    info = struct.unpack_from(f'!{message[3]}s', data[12:])
    info = info[0].decode()
    print(info)
    #check if data is in lines
    for a in lines:
        if (a.find(info) != -1):
            request = a
            fou = True
            break;
    # Echo back to client
    if (fou):
        ret = struct.pack('!hhihh', 2, 1, message[2], message[3], len(request)) + info.encode() + request.encode()
        #ret = request + "," + info[1] + "," + str(0)
        print("Sending data to client " + address[0] + ", " + str(address[1]))
        serverSocket.sendto(ret, address)
    else:
        #ret = " " + "," + info[1] + "," + str(1)
        temp = info + "," + " "
        ret = struct.pack('!hhihh', 2, 0, message[2], len(temp), message[4]) + info.encode()
        print("Sending data to client " + address[0] + ", " + str(address[1]))
        serverSocket.sendto(ret,address)
    ret = ""
    fou = False
    request = ""
