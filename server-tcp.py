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
        
    ''' pass the command line arguments'''
    serverPort = int(sys.argv[1])
    '''creates a TCP server socket'''
    serverSocket = socket(AF_INET,SOCK_STREAM)
    '''associate the server port number with this socket'''
    serverSocket.bind(('',serverPort))
    '''maximum number of 5 queued connections'''
    serverSocket.listen(5)
    print 'The server is ready to receive' 
    
    
    ''' create 3 username and pastword pairs'''
    userinfo = {'user1':'pass1', 'user2':'pass2', 'user3':'pass3'}
    
    while 1:
        '''creates a new socket in the server, dedicated to a particular client'''
        connectionSocket, addr = serverSocket.accept()
        '''TCP connection is now established'''
        
        
        ''' receive request from client'''
        request = connectionSocket.recv(1024) 
        
        randomStr = ''
        if request == 'authentication request':
            ''' generate 64 character random string'''
            randomStr = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))
            if debugging:
                print 'Sending random string <' + randomStr + " > to client"
            connectionSocket.send(randomStr)
        
        ''' receive username and hash from client'''
        str = connectionSocket.recv(1024)
        
        '''split the username and hashcode'''
        splitIndex = str.index(':')
        username = str[0:splitIndex]
        hashcode = str[splitIndex+1:]
        
        '''get the password'''
        password = 'notfound'
        message = ''
        
        ''' check valid username'''
        if username in userinfo.keys():
            password = userinfo[username]
        else:
            '''invalid username, send error message to the client'''
          
            message = 'User authorization failed: invalid username'
            if debugging: print message
            connectionSocket.send(message)
            connectionSocket.close()
            continue
        if debugging:
            print 'finding password for user <' + username + " >, password: " +password  
        m = md5.new()
        m.update(username + password + randomStr)
        '''check username and pasword'''
        if m.hexdigest() == hashcode:
            message = 'welcome to our service'
            print message
            connectionSocket.send(message)
        else:
            message = 'User authorization failed: wrong password'
            print message
            connectionSocket.send(message)
            
            
        connectionSocket.close()

if __name__ == '__main__':
    main(sys.argv)
   
