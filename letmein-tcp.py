# encoding=utf8
'''
Created on Feb 9, 2015

@author: chongwenguo
'''

from socket import *
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
        print 'invalid port number, please use 4 digits integer'
        sys.exit()

    '''creates client’s TCP socket'''
    clientSocket = socket(AF_INET, SOCK_STREAM)
    if debugging: print 'connecting to server'
    clientSocket.settimeout(5)
    '''initiates the TCP connection between the client and server'''
    clientSocket.connect((serverName,serverPort))
    
    '''send authentication request to server'''
    if debugging:
        print 'Sending authentication request to server ' + serverName + ':' + str(serverPort)
    clientSocket.send("authentication request")
   
    '''get the random generated string from server'''
    randomStr = clientSocket.recv(1024) 
    m = md5.new()
    m.update(username + password + randomStr)
    
    '''sends the username and hash through the client’s socket and into the TCP connection'''
    if debugging:
        print 'Sending username <' + username + '> and hash <' +  m.hexdigest() + '> to server'
    clientSocket.send(username + ':' + m.hexdigest())
   
    ''' get the login information from server and print it out'''
    message = clientSocket.recv(1024) 
    print message
    
    '''closing the connection'''
    if debugging: print 'closing the connection'
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
   
 