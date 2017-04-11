# encoding=utf8
'''
Created on Feb 9, 2015

@author: chongwenguo
'''
from socket import *
import threading
import string
import random
import sys
import md5

def main(argv):
    ''' check command line arguments'''
    if len(sys.argv) < 4:
        print 'invalid number of argument'
        sys.exit()
        
    if len(sys.argv) == 5 and sys.argv[4] != '-d':
        print 'invalid number of argument'
        sys.exit()
        
    ''' check debugging mode'''
    debugging = False
    if len(sys.argv) == 5:
        debugging = True
        
    ''' pass the command line arguments'''
    address = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    ''' 
        separate address into ip and port number
        and do some input arguments error checking
    '''
    try: 
        splitIndex = address.index(':')
    except:
        print 'Invalid address format, example: 127.0.0.1:8591 (ip address:port number)'
        sys.exit()
        
    serverName = address[0:splitIndex]
    '''check ip'''
    if not check_ip(serverName):
        print 'invalid ip address'
        sys.exit()
        
    '''check port number'''
    try:
        serverPort = int(address[splitIndex+1:])
    except:
        print 'invalid port number, please using 4 digits integer'
        sys.exit()
        
    '''creates the client’s UDP socket'''
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    if debugging: print 'connecting to server'
    clientSocket.settimeout(2)
    
    '''
        attaches the destination address (serverName, serverPort)
        to the message and sends the authentication request into the process’s socket
    '''
    if debugging:
        print 'Sending authentication request to server ' + serverName + ':' + str(serverPort)
    clientSocket.sendto("authentication request",(serverName, serverPort)) 
    timeCounter = 0
    received = False
    while(not received): 
        '''get the random generated string from server'''
        try:
            if debugging: print 'getting the random 64 bit string from server'
            randomStr, serverAddress = clientSocket.recvfrom(2048) 
            received = True
        except timeout:
            timeCounter += 1
            if timeCounter >= 10:
                print 'do not receive respond in 20 seconds, please try again'
                sys.exit()
            print 'message may get lost, try resending Authentication request. Time:' + str(2*timeCounter) +'s'
            clientSocket.sendto('authentication request', (serverName, serverPort))        
    
  
    
    '''generate the hash code'''
    m = md5.new()
    m.update(username + password + randomStr)
    
    '''sends the username and hash through the client’s socket and into the TCP connection'''
    if debugging:
        print 'Sending username <' + username + '> and hash <' +  m.hexdigest() + '> to server'
    clientSocket.sendto(username + ':' + m.hexdigest(),(serverName, serverPort)) 
   
    ''' get the login information from server and print it out'''
    
    timeCounter = 0
    received = False
    while(not received): 
        try:
            if debugging: print 'getting login information from server'
            message, serverAddress = clientSocket.recvfrom(2048) 
            print message
            received = True
        except timeout:
            timeCounter += 1
            if timeCounter >= 10:
                print 'do not receive respond in 20 seconds, please try again'
                sys.exit()
            print 'message may get lost, try resending. Time:' + str(2*timeCounter) + 's'
            clientSocket.sendto(username + ':' + m.hexdigest(),(serverName, serverPort)) 

    
    #message, serverAddress = clientSocket.recvfrom(2048) 
    #print message
    
    '''closing the connection'''
    if debugging: print 'closing the connection'''
    clientSocket.close()
    
def check_ip(ip):
    try:
        host_bytes = ip.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
        return True
    except:
        return False

if __name__ == '__main__':
     main(sys.argv)
   