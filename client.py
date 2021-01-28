import socket
import argparse


def setUpSocket(host, id, port):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))

    helloMessage = 'cs3700spring2021 HELLO ' + id + '\n'
    mySocket.send(str.encode(helloMessage))

    message = mySocket.recv(1024)
    decodedMessage = message.decode('utf8', 'strict')


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
        mySocket.send(str.encode(countMessage))

        message = mySocket.recv(1024)
        decodedMessage = message.decode('utf8', 'strict')

    print(message)
    flag = message.split()[2]
    mySocket.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=27995)

    parser.add_argument('-s', action='store_true')

    parser.add_argument('hostname')
    parser.add_argument('neuid')

    args = parser.parse_args()

    setUpSocket(args.hostname, args.neuid, args.port)




main()
