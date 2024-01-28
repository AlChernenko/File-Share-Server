import socket
import selectors
import sys

server_address = 'localhost'
server_port = 5000

sel = selectors.DefaultSelector()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))
client_socket.setblocking(False)
sel.register(client_socket, selectors.EVENT_WRITE, data=None)


def send_message(message):
    message = message.encode()
    client_socket.sendall(message)

    sel.unregister(client_socket)
    client_socket.close()


def main():
    sel.register(client_socket, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)

    while True:
        message = input("Enter message: ")
        send_message(message)

        events = sel.select()
        for key, mask in events:
            if mask & selectors.EVENT_READ:
                response = key.fileobj.recv(1024)
                if response:
                    print(response.decode())
                else:
                    print("Server closed the connection.")
                    sel.unregister(client_socket)
                    client_socket.close()
                    break


if __name__ == "__main__":
    main()
