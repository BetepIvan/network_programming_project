import socket
import sys

HOST = '127.0.0.1'
PORT = 50431


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10.0)
            print(f'Подключение к {HOST}:{PORT}...')
            sock.connect((HOST, PORT))

            while True:
                data_to_send = input("Message to send: ")

                if not data_to_send:
                    print("Отправляю пустое сообщение...")

                data_bytes_send = data_to_send.encode('utf-8')
                sock.sendall(data_bytes_send)

                if data_to_send.strip().lower() == 'exit':
                    # Для команды exit ждем ответ
                    try:
                        data_bytes_received = sock.recv(1024)
                        if data_bytes_received:
                            data_received = data_bytes_received.decode('utf-8')
                            print("Received:", data_received)
                    except:
                        pass
                    break
                elif data_to_send.strip().lower() == 'stop server':
                    # Для команды stop server ждем подтверждение
                    try:
                        data_bytes_received = sock.recv(1024)
                        if data_bytes_received:
                            data_received = data_bytes_received.decode('utf-8')
                            print("Received:", data_received)

                            if data_received == 'Сервер выключается':
                                print("\nПопытка отправить сообщение после выключения сервера...")
                                try:
                                    sock.sendall("последнее сообщение".encode('utf-8'))
                                    sock.settimeout(2.0)
                                    response = sock.recv(1024)
                                    if not response:
                                        print("Программа на вашем хост-компьютере разорвала установленное подключение")
                                except:
                                    print("Программа на вашем хост-компьютере разорвала установленное подключение")
                    except:
                        pass
                    break
                else:
                    # Обычное сообщение
                    try:
                        data_bytes_received = sock.recv(1024)
                        if not data_bytes_received:
                            print("\nСервер разорвал соединение")
                            break
                        data_received = data_bytes_received.decode('utf-8')
                        print("Received:", data_received)
                    except ConnectionError:
                        print("\nСервер разорвал соединение")
                        break

            print("\nProcess finished with exit code 0")

    except ConnectionRefusedError:
        print(f"Не удалось подключиться к {HOST}:{PORT}")
        print("Process finished with exit code 0")
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Process finished with exit code 0")


if __name__ == '__main__':
    main()