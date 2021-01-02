#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
power = False
color = 'white'
found = False
f = open('supported-colors.txt', "r")
lines = [line.lower() for line in f.readlines()]
f.close;
ret = ""
done = ''

def turnOn(col):
    print('turn on')
    global power
    if (power):
        return(changeColor(col))
    else:
        power = True
        return(changeColor(col))

def changeColor(col):
    print('change color')
    global found
    global done
    found = False
    for a in lines:
        if (a.find(col) != -1):
            found = True
    if (found):
        global color
        color = col
        print (color)
        
        done = 'OK'
        return (True)
    else:
        done = 'color not supported'
        print(done)
        return (False)
    
def turnOff():
    global power
    global done
    print('turn off')
    power = False
    done = 'OK'
    return (True)
    
def status():
    global power
    global done
    global color
    powst = 'off'
    if (power):
        powst = 'on'
    done = 'Status: ' + powst + ', Color: ' + color

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    data, address = serverSocket.recvfrom(1024)
    print("Receive data from client " + address[0] + ", " + str(address[1]))
    message = struct.unpack('!hhihh', data[:12])
    info = struct.unpack_from(f'!{message[3]}s', data[12:])
    col = info[0].decode()
    print(color)
    
    #check each action code
    if (message[0] == 1):
        sucess = turnOn(col)
    elif (message[0] == 2):
        sucess = changeColor(col)
    elif (message[0] == 4):
        sucess = turnOff()
    elif(message[0] == 3):
        sucess = status()
        
    else:
        sucess = False
        print ('incorrect action number')
        done = 'incorrect action number'
    
    #change power to number
    if (power):
        pownum = 1
    else:
        pownum = 0
    # Echo back to client
    if (sucess):
        ret = struct.pack('!hhihh', 0, 0, message[2], message[3], pownum) + col.encode() + done.encode()
        print("Sending data to client " + address[0] + ", " + str(address[1]))
        serverSocket.sendto(ret, address)
    else:
        ret = struct.pack('!hhihh', 0, 1, message[2], message[3], pownum) + col.encode() + done.encode()
        print("Sending data to client " + address[0] + ", " + str(address[1]))
        serverSocket.sendto(ret,address)
    ret = ""
    found = False
    done= ''