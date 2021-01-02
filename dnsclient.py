#! /usr/bin/env python3
# Echo Client
import sys
import socket
import random
import struct

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
temp = sys.argv[3]
nums = random.randint(1,101)
hostname = str(temp) + " A IN"
#data = hostname + "," + str(nums)
data = struct.pack('!hhihh', 1, 0, nums, len(hostname), 0) + hostname.encode()
# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
for x in range (3):
    try:
        # Send data to server
         print("Sending Request to   " + host + ", " + str(port))
         print("Message ID: " + str(nums))
         print("Question Length: " + str(len(hostname)) + " bytes")
         print("Answer Length: 0 bytes")
         print("Question: " + hostname)
         clientsocket.sendto(data,(host, port))


        # Receive the server response
         dataEcho, address = clientsocket.recvfrom(100)
         #info = dataEcho.decode().split(",")
         
         message = struct.unpack('!hhihh', dataEcho[:12])
         info = dataEcho[12:]
         info1 = info[:message[3]].decode()
         temp1 = info[message[3]:].decode()
         
         print("Receive data from " + address[0] + ", " + str(address[1]))
         print("Message ID: " + str(message[2]))
         print("return code: " + str(message[1]))
         print("Question Length: " + str(len(info1)) + " bytes")
         print("Answer Length: " + str(len(temp1)) + " bytes")
         print("Question: " + info1)
         print("Answer: " + temp1)
         break;
         
    except socket.timeout as e:
        print (e)
     
        
#Close the client socket
clientsocket.close()
