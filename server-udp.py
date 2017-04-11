# encoding=utf8
'''
Created on Feb 9, 2015

@author: chongwenguo
'''

from socket import *
import md5
import sys
import random
import string
from time import sleep

def main(argv):
    '''check valid command line argument'''
    if len(sys.argv) != 2:
        if len(sys.argv) == 3 and sys.argv[2] != '-d':
            print 'invalid number of argument'
            sys.exit()
        
    ''' check debugging mode'''
    debugging = False
    if len(sys.argv) == 3:
        debugging = True
        
    '''passing command line argument'''
    serverPort = int(sys.argv[1])
    
    '''create a server UDP socket'''
    serverSocket = socket(AF_INET, SOCK_DGRAM) 
    
    ''' binds the port number to the server’s socket'''
    serverSocket.bind(('', serverPort))
    print 'The server is ready to receive'
    
    ''' create 3 username and password pairs'''
    userinfo = {'user1':'pass1', 'user2':'pass2', 'user3':'pass3'}
    
    while 1:
        ''' get the request and client address from client'''
        request, clientAddress = serverSocket.recvfrom(2048) 
        
        randomStr = ''
        if request == 'authentication request':
            ''' generate 64 character random string'''
            randomStr = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))
           
            ''' 
                attaches the client’s address (IP address and port number)
                sends the resulting packet into the server’s socket
            '''
            if debugging:
                print 'Sending random string <' + randomStr + " > to client"
            serverSocket.sendto(randomStr, clientAddress)
        else:
            ''' wait until got request from a client'''
            continue
        ''' receive username and hash from client'''
        str, clientAddress = serverSocket.recvfrom(2048) 
        
        '''split the username and hashcode'''

        splitIndex = str.index(':')
        username = str[0:splitIndex]
        hashcode = str[splitIndex+1:]
        
        '''get the password'''
        password = 'notfound'
        message = ''
        
        '''chceck user name'''
        if username in userinfo.keys():
            password = userinfo[username]
        else:
            '''invalid username, send error message to the client'''
            message = 'User authorization failed: invalid username'
            if debugging: print message
            serverSocket.sendto(message, clientAddress)
            continue
        
        if debugging:
            print 'finding password for user <' + username + " >, password: " +password  
        m = md5.new()
        m.update(username + password + randomStr)
        
        '''check username and pasword'''
        if m.hexdigest() == hashcode:
            message = 'welcome to our service'
            print message
            serverSocket.sendto(message, clientAddress)
        else:
            message = 'User authorization failed: wrong password'
            print message
            serverSocket.sendto(message, clientAddress)
            
   
if __name__ == '__main__':
    main(sys.argv)
   