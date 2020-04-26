import socket


class Server:
    def __init__(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start_server(self):
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(('localhost', 5001))
        self._server_socket.listen(2)

        print('Server started')

    def get_clients(self):
        for i in range(2):
            client_sock, addr = self._server_socket.accept()
            self.clients.append((client_sock, addr))

            self.send(client_sock, 'Welcome\n')

            print(f"Client {i}: sock - {client_sock} addr - {addr}")

        return self.clients

    def close_connection(self):
        for client in self.clients:
            client[0].close()

        print("Clients were closed")

    @staticmethod
    def send(client_sock: socket.socket, response: str):
        print(f"send response {response}")

        response = response.encode()
        client_sock.send(response)

    @staticmethod
    def read(client_sock: socket.socket):
        print(f"get data from {client_sock}")

        request = client_sock.recv(1024)
        data = request.decode()

        print(f"received data: {data}")

        return data

