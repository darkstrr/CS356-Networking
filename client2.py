#! /usr/bin/env python3
# Echo Client
import sys
import socket
import time

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
count = 10
data = 'X' * count # Initialize data to be sent
mini = 10
maxi = 0
times = 0
avg = 0
err = 0
# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
for x in range(10):
    data = str(x)
    try:
        # Send data to server
         print("Sending data to   " + host + ", " + str(port) + ": " + data)
         tic = time.perf_counter()
         clientsocket.sendto(data.encode(),(host, port))


        # Receive the server response
         dataEcho, address = clientsocket.recvfrom(count)
         toc = time.perf_counter()
         print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
         times = toc - tic
         if (times < mini):
            mini = times
         if (times > maxi):
            maxi = times
         avg = avg + times
         print(f"Data took {times:0.4f} seconds")
    except socket.timeout as e:
        err = err + 1
        print (e)
avg = avg / 10       
print(f"Min: {mini:0.4f} seconds  Max: {maxi:0.4f} seconds  Avg: {avg:0.4f} seconds ")
print("Packet loss: " + str(err) + "0%" )          
#Close the client socket
clientsocket.close()
