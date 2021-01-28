import socket
import argparse


def setUpSocket(host, id, port):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))

    helloMessage = 'cs3700spring2021 HELLO ' + id + '\n'
    mySocket.send(str.encode(helloMessage))
    decodedMessage = createMessage(mySocket)

    iterations = 0

    raise Exception (decodedMessage)

    while (decodedMessage[:20] != 'cs3700spring2021 BYE'):

        if (decodedMessage[:21] != 'cs3700spring2021 FIND'):
            raise Exception("This is the number of iterations" + str(iterations) + "Received message was not as expected:" + decodedMessage)

        iterations += 1

        symbolAndCharacters = decodedMessage[22:len(decodedMessage) - 1]
        symbol = symbolAndCharacters.split()[0]
        characters = symbolAndCharacters.split()[1]

        count = 0

        for item in characters:
            if item == symbol:
                count += 1

        countMessage = 'cs3700spring2021 COUNT ' + str(count) + '\n'
        mySocket.send(str.encode(countMessage))
        decodedMessage = createMessage(mySocket)


    print(decodedMessage)
    flag = decodedMessage.split()[2]
    print(flag)
    mySocket.close()


def createMessage(mySocket):
    decodedMessage = ''
    sequenceNotOver = True

    while sequenceNotOver:
        message = mySocket.recv(1024)
        partOfMessage = message.decode('utf8', 'strict')
        endingSequence = partOfMessage[-1]
        print(endingSequence)
        decodedMessage += partOfMessage
        print(decodedMessage)
        if endingSequence == "\n":
            sequenceNotOver = False

    return decodedMessage




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=27995)

    parser.add_argument('-s', action='store_true')

    parser.add_argument('hostname')
    parser.add_argument('neuid')

    args = parser.parse_args()

    setUpSocket(args.hostname, args.neuid, args.port)




main()
