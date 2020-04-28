import socket


def read():
    data = sock.recv(20480)
    return data


def send():
    response = input().encode()
    sock.send(response)


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('localhost', 5001))

    while True:
        cur_data = read()

        if not cur_data:
            break

        cur_data = cur_data.decode().split('|')

        print(cur_data[1])

        if cur_data[0] == 'awaiting response':
            send()
