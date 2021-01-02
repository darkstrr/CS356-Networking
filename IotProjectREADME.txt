For the Iot implementation, I have made the following changes to clear up some conflicting issues in the instructions:

Changed the sent and recieve data to match the message format:
	i.e. Action Type is 8 bits, Return Code is 8bits, Message Identifier is 16 bits...

Return 0 for Action Type Number when sending data from server to client
	specified in the message format of action type