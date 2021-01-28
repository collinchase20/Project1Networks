import socket
import argparse


def setUpSocket(host, id, port):
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
    mySocket.send('cs3700spring2021 HELLO ' + id + '\n')
    message = mySocket.recv(1024)

    while (message[:20] != 'cs3700spring2021 BYE'):
        if (message[:21] != 'cs3700spring2021 FIND'):
            raise Exception("Received message was not as expected.")
        strings = message[21:len(message) - 1]
        symbol = strings.split()[0]
        searchString = strings.split()[1]
        count = 0

        for item in searchString:
            if item == symbol:
                count += 1

        mySocket.send('cs3700spring2021 COUNT ' + str(count) + '\n')
        message = mySocket.recv(1024)


    flag = message.split()[2]
    print(message)
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
