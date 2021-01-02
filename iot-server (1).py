#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct
import random


#Arguments, the IP Address and Port
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

#===================================
bulb_state="OFF"
#===================================
bulb_brightness=0
#===================================
color_length=0
#===================================
color1=0.00
color2=0.00
color3=0.00
full_color=(f"{color1} {color2} {color3}")
#===================================

#UDP socket created
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Assign server IP and port to socket
serverSocket.bind((serverIP, serverPort))

print("Server has been set up and ready to go!")
while True:

	the_destroyer_of_bulbs=random.randint(1,100)
	if the_destroyer_of_bulbs == 1:
		broken="BROKEN"
		bulb_state=broken


	data, address = serverSocket.recvfrom(1024)

	message_type,return_code,message_identifier,action,= struct.unpack(f"!hhih",data[:10])

	
	if action==0:
		if bulb_state == "ON" or bulb_state == "OFF":
			return_code=0
			bulb_state="OFF"
		else:
			return_code=1
		
		message_type=2

		response = struct.pack('!hhi',message_type,return_code,message_identifier)

		serverSocket.sendto(response, address)


	elif action==1:
		if bulb_state == "ON" or bulb_state == "OFF":
			return_code=0;
			brightness,color_length=struct.unpack(f"!fh",data[10:16])
			color=struct.unpack(f'!{color_length}s',data[16:])
			color=color[0].decode()

			bulb_brightness=brightness
			split_color=color.split(" ")
			color1=split_color[0]
			color2=split_color[1]
			color3=split_color[2].split("\ ")[0]
			full_color=(f"{color1} {color2} {color3}")
			bulb_state="ON"

		else:
			return_code=1;


		
		message_type=2

		response = struct.pack('!hhi',message_type,return_code,message_identifier)

		serverSocket.sendto(response, address)

	elif action==2:
		if bulb_state == "ON" or bulb_state == "OFF":
			return_code=0;

			color_length=struct.unpack("!h",data[10:12])
			color_len=color_length[0]
			color=struct.unpack(f'!{color_len}s',data[12:])
			color=color[0].decode()

			split_color=color.split(" ")
			color1=split_color[0]
			color2=split_color[1]
			color3=split_color[2].split("\ ")[0]
			full_color=(f"{color1} {color2} {color3}")
		else:
			return_code=1;



		message_type=2

		response = struct.pack('!hhi',message_type,return_code,message_identifier)

		serverSocket.sendto(response, address)

	elif action==3:
		if bulb_state == "ON" or bulb_state == "OFF":
			return_code=0;

			brightness =struct.unpack(f"!f",data[10:14])
			bulb_brightness=brightness[0]
		else:
			return_code=1;

		
		message_type=2

		response = struct.pack('!hhi',message_type,return_code,message_identifier)

		serverSocket.sendto(response, address)

	elif action==4:
		if bulb_state == "ON" or bulb_state == "OFF":
			return_code=0;
			

		else:
			return_code=1;

		answer=(f"Bulb:{bulb_state},Brightness:{bulb_brightness}%,RGB color %:{full_color}")
		answer_len=len(answer)

		message_type=2

		response = struct.pack(f'!hhih{answer_len}s',message_type, return_code, message_identifier,answer_len,
				answer.encode())

		serverSocket.sendto(response, address)




