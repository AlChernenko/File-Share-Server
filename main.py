import socket
import selectors

default_selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    default_selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print("New connection from: ", client_address)
    default_selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_mes)

def send_mes(client_socket):
    try:
        request = client_socket.recv(1024)
        if request:
            print(request)
        else:
            print("Connection closed by client: ", client_socket.getpeername())
            default_selector.unregister(client_socket)
            client_socket.close()
    except ConnectionResetError:
        print("Client forcibly closed the connection")
        default_selector.unregister(client_socket)
        client_socket.close()
    except OSError as e:
        print("Connection error:", e)
        default_selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        events = default_selector.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)

if __name__ == '__main__':
    print('Server run')
    server()
    event_loop()
