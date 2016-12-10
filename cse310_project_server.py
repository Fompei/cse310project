# SO WHAT DO WE WANT TO DO FOR THIS SERVER?
# WHAT DO WE DO FOR SERVER AND NOT FOR CLIENT?
# WE WANT TO CREATE A SERVER THAT WILL LOGIN CLIENTS THESE CLIENTS 

from socket import *
from time import *
from threading import *
from json import *
from pprint import *
from re import *

# SERVER IS STARTED AND WAITS AT A KNOWN PORT FOR REQUESTS FROM CLIENTS
# SHOULD IT BE (!TCP!) OR UDP CONNECTION?
serverPort = 12003 # HARD CODE SERVER PORT
serverSocket = socket(AF_INET, SOCK_STREAM) # CREATING SOCKET AND BINDING IT TO PORT
serverSocket.bind(('', serverPort))
serverSocket.listen(100)  # ONLY LISTEN TO 100 CLIENTS

ag_flag = 0
sg_flag = 0
rg_flag = 0

while True:

    print('The server is setup and ready to receive from client\n')
    connectionSocket, addr = serverSocket.accept()
##      connectionSocket.send('===========================\r\n')
##      connectionSocket.send('|| Interest Groups Server ||\r\n')
##      connectionSocket.send('===========================\r\n')
##      connectionSocket.send('Awaiting commands...\r\n')
    received_data = connectionSocket.recv(128)  # command
    commands = received_data.split(" ")

    print(commands[0])  # SHOULD BE FIRST command

    if (commands[0] == "ag"):
        default_display = 5
        try:
            if commands[1] != "":
                default_display = int(commands[1])
        except IndexError:
            pass

        ag_info = ""
        with open('server.json') as serverfile:
            server_data = load(serverfile)
            for i in range(default_display):
                ag_info += server_data['discussion_groups'][i]['groupname']
                ag_info += '\n'
        connectionSocket.sendall(ag_info.encode('UTF-8'))

        while (ag_flag == 0):
            ag_data = connectionSocket.recv(128)
            ag_subcommands = ag_data.split(" ")

            if (ag_subcommands[0] == "n"):
                print("Command n entered")
                ag_more_info = ""
                with open('server.json') as serverfile:
                    server_data = load(serverfile)
                    for i in range(default_display, default_display + int(ag_subcommands[1])):
                        ag_more_info += server_data['discussion_groups'][i]['groupname']
                        ag_more_info += '\n'
                connectionSocket.sendall(ag_more_info.encode('UTF-8'))

            elif (ag_subcommands[0] == "q"):
                print("Command q entered")
                break

    elif (commands[0] == "sg"):
        display = 5
        try:
            if not commands[1]:
                display = commands[1]
        except IndexError:
            pass

        connectionSocket.send("1.  18  comp.programming \n" +
                              "2.   2  comp.lang.c \n" +
                              "3.   3  comp.lang.python \n" +
                              "4.  27  sci.crpyt \n" +
                              "5.      rec.arts.ascii \n")
        continue
    elif (commands[0] == "rg"):
        display = 5
        try:
            if not commands[2]:
                display = commands[2]
        except IndexError:
            pass
        try:
            if not commands[1]:
                gname = commands[1]
        except IndexError:
            connectionSocket.send("Require a mandatory argument 'gname'\n")
            continue
            
        connectionSocket.send("1. N  Nov 12 19:32:02   Sort a Python dictionary by value \n" +
                              "2. N  Nov 11 08:11:34   How to print to stderr in Python? \n" +
                              "3. N  Nov 10 22:05:47   \"Print\" and \"Input\" in one file \n" +
                              "4.    Nov  9 13:59:05   How not to display the user inputs? \n" +
                              "5.    Nov  9 12:46:10   Declaring custom exceptions \n")

        continue                
    elif (commands[0] == "logout"):
        connectionSocket.send('Closing your connection\r\n')
        print('Closing connection to client\n')
        connectionSocket.close()    
    else:
        connectionSocket.sendall("400 Bad Request\r\n")  

           
serverSocket.close()            
    
    

