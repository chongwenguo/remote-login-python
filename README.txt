1.Name: chongwen guo  E-mail:cguo61@gatech.edu
2.Class: CS 3251 - Computer Networks I, section A
Assignment: Sockets Programming Assignment 1
Platform: MAC os, Python 2.7

3.
Descriptions of all files:

	server-udp.py: source code of UDP server side 
	letmein-udp.py: source code of UDP client side
	server-tcp.py:  source code of TCP server side
	letmetin-tcp.py: source code of TCP client side 
	sample output.txt: sample outputs for different command


Instructions for compiling and running:

First run a server in a terminal:
1. open a terminal
2. Using cd command go to the folder which contains all the python source code files
3. enter command: 
		for TCP: python server-tcp.py <port number> <-d>
		for UDP: python server-udp.py <port number> <-d>
here adding -d to enable debug mode

example for TCP server: python server-tcp.py 8591
example for UDP server: python server-udp.py 8591

Running a client after set up a server:
1. Open a new terminal
2. Using cd command go to the folder which contains all the files
3. enter command: 
		for TCP: python letmein-tcp.py <serverAddress> <username> <password> <-d>
		for UDP: python letmein-udp.py <serverAddress> <username> <password> <-d>
here adding -d to enable debug mode

example for TCP client: python letmein-tcp.py 127.0.0.1:8591 user1 pass1
example for UDP client: python letmein-udp.py 127.0.0.1:8591 user1 pass1

There are three users on the server side:
Username		Password
user1			pass1
user2			pass2
user3 			pass2


Description of application protocol:
TCP:
1. setting up the TCP server socket, binding to a particular port for connection requests from clients
2. On the client side, creating a client socket, initiating the TCP connection, connecting to the server IP.
3. On the server side, server socket creates a connection socket to accept client connection.
4. Then client uses a client socket to send the authentication Request (string: authentication request) to the server socket.
5. On the server side, server socket reads a request from client socket. If it is a authentication request, the server generates a random 64-bit string and send the string to the client socket.
6. Client socket receives the random string from server, and generates a hash code of MD5(username + password + ransom string), and then send a message of (username : hash code) to the server.
7. The server receives the message containing username and hashcode, and then retrieve the password for the username. And then performing the same hashing function of MD5(username + password + random string) to check if it is the same as the one send from the client. If they are identical, which means it is correct username-password pair, the server sents back a successful log in confirmation to client socket. Otherwise the server sent an fail message (wrong username, correct username but wrong password) to the client. Connection socket closes.
8. Client socket receives the login message from the server, and print the message out to the user. 
9. Client socket closes. server connection socket closes.

UDP:
1. create a UDP server socket, binding to a particular port
2. On the client side, creating a client UDP socket. Then send an Authentication Request message to the server via its server name(ip address) and server port.
3. Server socket receives the Authentication Request from client socket, and generates a random 64-bit string, send back to the client socket.
4. Client socket receives the random string, and generates hash code of  MD5(username + password + random string), then send a message (username:hash code) to the server socket. 
5. Server socket receives the message from client sockets, and retrieves the password for the username send by the client, and uses same MD5 hashing function MD5(username + password + random string) to check if the username and password pair is valid. Finally sending back the confirmation result to the client socket.
6. Client socket receives the confirmation message, then print it out.  
7. Client socket closes

Bugs and limitation:
1. if the TCP client wants to connect to a IP address and port number on which no server running on that address, I set 10s for timeout if within 10s the client does not get response. 
2. if the udp server is not running or the message is losing, the client will resend the request 10 times(2s interval) to the server, and after 20s, if still not getting respond, just timeout.

	
