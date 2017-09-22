# -*- coding:utf-8 -*-
import socket

host = "172.21.32.101" #server ip
port = 8080 #port  same client

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #bind ip and port
serversock.listen(10) #connect listen（Max queue）

print('Waiting for connections...')
clientsock, client_address = serversock.accept()

while True:
    rcvmsg = clientsock.recv(1024)
    if rcvmsg != b'':
    	print('Received -> %s' % (rcvmsg))
    #print('Wait...')

clientsock.close()
