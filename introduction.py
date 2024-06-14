import socket

# SOCK_STREAM - TCP сокет, SOCK_DGRAM - UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

while True:

    # блокирующая функция ждет подключения
    print("Before accepting connections")
    client_socket, client_address = server_socket.accept()
    print("Connection from", client_address)

    while True:
        print("Before receiving data from client")
        # тоже блокирующая функция
        request = client_socket.recv(4096)
        if not request:
            break
        else:
            response = "Hello world\n".encode()
            client_socket.send(response)

    print("Outside inner while loop")
    client_socket.close()
