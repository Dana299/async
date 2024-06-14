import selectors
import socket


selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    # когда серверный сокет будет доступен для чтения,
    # на нем можно будет вызвать функцию для принятия подключения
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print("Connection from", client_address)

    # когда клиентский сокет будет доступен для чтения,
    # на нем можно будет вызвать функцию для отправки сообщения
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # блокируется пока на каком-то сокете не произойдет зарегистрированное событие
        events = selector.select()   # (key, events)

        # key - экземпляр SelectorKey, соответствующий файловому объекту
        for key, _ in events:
            # получаем функцию которую прописали
            callback = key.data
            # вызываем эту функцию на сокете
            callback(key.fileobj)


if __name__ == "__main__":
    server()
    event_loop()
