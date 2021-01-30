import socket
import ssl
import argparse


#Main method to connect to the socket, can be ssl or normal, and perform the protocol required.
def setUpSocket(host, id, port, isSSL):

    #Set up the Hello Message we will send to the server and a decodedMessage placeholder for the messages we
    #receive from the server
    helloMessage = 'cs3700spring2021 HELLO ' + id + '\n'
    decodedMessage = ''

    #If SSL boolean is true we try and do an SSL connection
    if (isSSL):
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((host, port))
            sslConnection = ssl.wrap_socket(mySocket)
        except:
            raise Exception("Error Connecting to SSL Socket, Host Name, Service, or Port Unknown")
        sslConnection.write(str.encode(helloMessage))
        decodedMessage = createMessage(sslConnection, True)

    #If SSL boolean is false we do a normal connection
    else:
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((host, port))
        except:
            raise Exception("Error Connecting to Socket, Host Name, Service, or Port Unknown")
        mySocket.send(str.encode(helloMessage))
        decodedMessage = createMessage(mySocket, False)

    #While loop to iterate through the numerous messages we might recieve from the server
    #Also makes sure we are only receiving BYE or FIND messages from the server. If we get a BYE message we break
    #and print the flag. If we get a FIND message we count the occurances of the symbol in the message, send the
    #COUNT message to the server, and loop again to see what message we receive back.
    while (decodedMessage[:20] != 'cs3700spring2021 BYE'):

        if (decodedMessage[:21] != 'cs3700spring2021 FIND'):
            raise Exception("Received message was not as expected:" + decodedMessage)

        symbolAndCharacters = decodedMessage[22:len(decodedMessage) - 1]
        symbol = symbolAndCharacters.split()[0]
        characters = symbolAndCharacters.split()[1]
        count = 0

        for item in characters:
            if item == symbol:
                count += 1

        countMessage = 'cs3700spring2021 COUNT ' + str(count) + '\n'

        #Check if we are using an SSL connection so we know how to send the message to the server
        if (isSSL):
            sslConnection.write(str.encode(countMessage))
            decodedMessage = createMessage(sslConnection, True)
        else:
            mySocket.send(str.encode(countMessage))
            decodedMessage = createMessage(mySocket, False)


    flag = decodedMessage.split()[2]
    print(flag)
    mySocket.close()


#Method to decode and return the message from the server as a string.
def createMessage(mySocket, isSSL):
    decodedMessage = ''
    sequenceNotOver = True

    #Need to constantly check if the sequence is over. We might not get the full message from one socket.read call
    #Once we see that the message from the serve ends with a new line we stop reading the message and return the full
    #decodedMessage
    try:
        while sequenceNotOver:
            if (isSSL):
                message = mySocket.read(1024)
            else:
                message = mySocket.recv(1024)
            partOfMessage = message.decode()
            endingSequence = partOfMessage[-1]
            decodedMessage += partOfMessage
            if endingSequence == "\n":
                sequenceNotOver = False
    except:
        raise Exception("Error decoding the message recieved from the server.")

    return decodedMessage



#Method to execute the protocol
def runScript():

    #Set up an argument parser for the terminal
    parser = argparse.ArgumentParser()

    #Add arguments
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-s', action='store_true')
    parser.add_argument('hostname')
    parser.add_argument('neuid')

    args = parser.parse_args()

    #If the ssl argument is not provided connect to the TCP socket normally
    if (not args.s):
        #If the port argument is not provided we connect to port 27995 as described in the assignment
        #Else we try and connect to the port provided
        if (not args.port):
            setUpSocket(args.hostname, args.neuid, 27995, False)
        else:
            setUpSocket(args.hostname, args.neuid, args.port, False)
    else:
        #Here we know we are using an SSL connection. If the port argument is not provided we connect to port
        #27996 as described for the SSL connection in the assignment. Else we connect to the port provided
        if (not args.port):
            setUpSocket(args.hostname, args.neuid, 27996, True)
        else:
            setUpSocket(args.hostname, args.neuid, args.port, True)






#Run method to execute this file and perform the protocol
runScript()
