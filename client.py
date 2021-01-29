import socket
import ssl
import argparse


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


def createMessage(mySocket, isSSL):
    decodedMessage = ''
    sequenceNotOver = True

    if (isSSL):
        while sequenceNotOver:
            message = mySocket.read(1024)
            partOfMessage = message.decode('utf8', 'strict')
            endingSequence = partOfMessage[-1]
            decodedMessage += partOfMessage
            if endingSequence == "\n":
                sequenceNotOver = False
    else:
        while sequenceNotOver:
            message = mySocket.recv(1024)
            partOfMessage = message.decode('utf8', 'strict')
            endingSequence = partOfMessage[-1]
            decodedMessage += partOfMessage
            if endingSequence == "\n":
                sequenceNotOver = False


    return decodedMessage




def run():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', type=int, default=27995)
    parser.add_argument('-s', action='store_true')
    parser.add_argument('hostname')
    parser.add_argument('neuid')

    args = parser.parse_args()

    if (not args.s):
        setUpSocket(args.hostname, args.neuid, args.port, False)
    else:
        setUpSocket(args.hostname, args.neuid, 27996, True)




run()
