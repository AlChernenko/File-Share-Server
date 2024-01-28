import socket
import selectors
import sys

server_address = ('localhost', 12345)


def start_connection(address, port, sel):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))

    client_socket.setblocking(False)
    sel.register(client_socket, selectors.EVENT_WRITE, data=None)

    return client_socket


def send_message(client_socket, message, sel):
    message = message.encode()
    client_socket.sendall(message)

    sel.unregister(client_socket)
    client_socket.close()


def main():
    sel = selectors.DefaultSelector()
    client_socket = start_connection(*server_address, sel)

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(sys.stdin, selectors.EVENT_READ, data=client_socket)
    sel.register(client_socket, events, data=None)

    while True:
        events = sel.select()
        for key, mask in events:
            if key.data is None:
                send_message(client_socket, input("Enter message: "), sel)
            elif mask & selectors.EVENT_READ:
                if key.fileobj is sys.stdin:
                    continue
                response = key.fileobj.recv(1024)
                if response:
                    print(response)
                else:
                    print("Server closed the connection.")
                    sel.unregister(client_socket)
                    client_socket.close()
                    break


if __name__ == "__main__":
    main()
