import socket
import ssl
import argparse


#Main method to connect to the socket, can be ssl or normal, and perform the protocol required.
def setUpSocket(host, id, port, isSSL):
    helloMessage = 'cs3700spring2021 HELLO ' + id + '\n'
    decodedMessage = ''

    if (isSSL):
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((host, port))
            sslConnection = ssl.wrap_socket(mySocket)
            sslConnection.write(str.encode(helloMessage))
            decodedMessage = createMessage(sslConnection, True)
        except:
            raise Exception("Error Connecting to SSL Socket, Host Name or Service Unknown")
    else:
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((host, port))
            mySocket.send(str.encode(helloMessage))
            decodedMessage = createMessage(mySocket, False)
        except:
            raise Exception("Error Connecting to Socket, Host Name or Service Unknown")


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
    #Once we see that the message from the serve ends with a new line we stop reading the message
    while sequenceNotOver:
        if (isSSL):
            message = mySocket.read(1024)
        else:
            message = mySocket.recv(1024)
        partOfMessage = message.decode('utf8', 'strict')
        endingSequence = partOfMessage[-1]
        decodedMessage += partOfMessage
        if endingSequence == "\n":
            sequenceNotOver = False

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
        if (not args.port):
            setUpSocket(args.hostname, args.neuid, 27995, False)
        else:
            setUpSocket(args.hostname, args.neuid, args.port, False)
    else:
        #Here we know we are using an SSL connection. We are now checking if the port argument was provided
        #if it is not provided we run the SSL connection on port 27996 as described in the extra credit
        if (not args.port):
            setUpSocket(args.hostname, args.neuid, 27996, True)
        else:
            setUpSocket(args.hostname, args.neuid, args.port, True)






#Run method to execute this file and perform the protocol
runScript()
