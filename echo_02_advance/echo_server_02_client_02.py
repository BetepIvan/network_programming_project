import socket

HOST = '127.0.0.1'
PORT = 50432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        data_to_send = input("Message to send: ")
        data_bytes_send = data_to_send.encode()
        sock.sendall(data_bytes_send)
        data_bytes_received = sock.recv(1024)
        data_received = data_bytes_received.decode()
        print("Received", data_received)