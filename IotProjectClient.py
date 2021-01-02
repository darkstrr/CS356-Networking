#! /usr/bin/env python3
# Echo Client
import sys
import socket
import random
import struct

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
act = int(sys.argv[3])
iden = random.randint(1,101)
retc = 0
power = 0
lencol = 0
color = ""
n = len(sys.argv)
if(n == 5):
    color = sys.argv[4].lower()
    lencol = len(color)

#construct message
if (act == 1 or act == 2):
    data = struct.pack('!hhihh', act, retc, iden, lencol, power) + color.encode()
elif (act == 3 or act == 4):
    data = struct.pack('!hhihh', act, retc, iden, lencol, power)
else:
    print("invalid action number")
    exit()


# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
for x in range (3):
    try:
        # Send data to server
         print("Sending Request to   " + host + ", " + str(port))
         print("Action number: " + str(act))
         print("Message ID: " + str(iden))
         print("Color Length: " + str(lencol))
         print("Color String: " + color)
         clientsocket.sendto(data,(host, port))


        # Receive the server response
         dataEcho, address = clientsocket.recvfrom(100)
         print("recieved")
         
         message = struct.unpack('!hhihh', dataEcho[:12])
         info = dataEcho[12:]
         color = info[:message[3]].decode()
         done = info[message[3]:].decode()
         
         print("Receive data from " + address[0] + ", " + str(address[1]))
         print("Message ID: " + str(message[2]))
         print("Return code: " + str(message[1]))
         print("Action number: " + str(message[0]))
         print("Color Length: " + str(message[3]))
         if(message[4] == 1):
            print("Power: True")
         else:
            print("Power: False")
         print('Color: ' + color)
         print("Response: " + done)
         break;
    except socket.timeout as e:
        print (e)
    except:
        print('Cannot find lightbulb, or lightbulb is broken')
     
        
#Close the client socket
clientsocket.close()