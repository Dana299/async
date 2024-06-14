import socket
from select import select


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)

# список сокетов для мониторинга
sockets_to_monitor = []


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print("Connection from", client_address)

    sockets_to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)
    else:
        sockets_to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # мониторим список сокетов, доступных для чтения
        ready_to_read, _, _ = select(sockets_to_monitor, [], [])   # read, write, errors

        for sock in ready_to_read:
            if sock == server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == "__main__":
    sockets_to_monitor.append(server_socket)
    event_loop()
