import socket
import selectors

default_selector = selectors.DefaultSelector()

def find_available_port(start_port, end_port):
    for port in range(start_port, end_port):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('localhost', 5000))
            return server_socket, port
        except OSError:
            continue
        return None, None
            
def server():

    server_socket, port = find_available_port(5000, 5100)

    if server_socket == None:
        print("Available port is not found")
        return
    
    server_socket.listen()
    print(f"Server is running on port {port}")

    
    default_selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    print("New connection from: ", client_address)

    verifying_message = "you connecting to file share by Wordik156 and ALKSchrnk"
    client_socket.send(verifying_message.encode('utf-8'))
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
