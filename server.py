import socket
import selectors

def accept_connection(server_socket, sel):
    client_socket, client_address = server_socket.accept()
    print("New connection from:", client_address)
    client_socket.setblocking(False)
    sel.register(client_socket, selectors.EVENT_READ, data=handle_client)

def handle_client(client_socket, sel):
    try:
        request = client_socket.recv(1024)
        if request:
            print("Received:", request.decode())
            response = "Message received".encode()
            client_socket.sendall(response)
        else:
            print("Connection closed by client:", client_socket.getpeername())
            sel.unregister(client_socket)
            client_socket.close()
    except Exception as e:
        print("Error:", e)
        sel.unregister(client_socket)
        client_socket.close()

def main():
    server_address = 'localhost'
    server_port = 5000
    sel = selectors.DefaultSelector()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_address, server_port))
        server_socket.listen()
        print(f"Server is running on {server_port}")
        server_socket.setblocking(False)
        sel.register(server_socket, selectors.EVENT_READ, data=accept_connection)

        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, sel)

if __name__ == "__main__":
    main()
