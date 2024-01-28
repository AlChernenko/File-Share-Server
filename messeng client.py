import socket
import selectors

def main():
    server_address = 'localhost'
    server_port = 5000
    sel = selectors.DefaultSelector()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_address, server_port))
        client_socket.setblocking(False)
        sel.register(client_socket, selectors.EVENT_READ | selectors.EVENT_WRITE)

        while True:
            message = input("> > >  ")
            if message.lower() == 'o':
                break

            message = message.encode()
            client_socket.sendall(message)

            events = sel.select(timeout=1)
            for key, mask in events:
                if mask & selectors.EVENT_READ:
                    response = key.fileobj.recv(1024)
                    if response:
                        print("Received:", response.decode())
                    else:
                        print("Server closed the connection.")
                        return

if __name__ == "__main__":
    main()
