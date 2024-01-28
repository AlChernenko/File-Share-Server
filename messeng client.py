import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
sock.connect(('localhost', 5000))  # подключемся к серверному сокету

while True:
    mes = str(input("> > >  "))
    if mes == '0':
        break
    sock.send(bytes(mes, encoding = 'UTF-8'))  # отправляем сообщение
    
sock.close()  # закрываем соединение
