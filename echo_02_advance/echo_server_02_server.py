import socket

HOST = '127.0.0.1'
PORT = 50432

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()

        print(f'Сервер запущен на {HOST}:{PORT}')

        while True:
            print('\nОжидаю подключения...')
            sock, addr = serv_sock.accept()
            with sock:
                print(f"Подключение по {addr}")

                while True:
                    try:
                        data = sock.recv(1024)
                    except ConnectionError:
                        print(f'Клиент {addr} внезапно отключился в процессе отправки данных на сервер')
                        break

                    # Если клиент отправил пустые данные (разрыв соединения)
                    if not data:
                        print(f'Клиент {addr} корректно отключился')
                        break

                    data_decoded = data.decode('utf-8')
                    print(f'Received: "{data_decoded}", from {addr}')

                    # Проверка команд от клиента
                    if data_decoded.strip().lower() == 'exit':
                        print(f'Клиент {addr} запросил отключение по команде')
                        response = 'До свидания!'.encode('utf-8')
                        sock.sendall(response)
                        break
                    elif data_decoded.strip().lower() == 'stop server':
                        print(f'Клиент {addr} запросил выключение сервера')
                        response = 'Сервер выключается'.encode('utf-8')
                        sock.sendall(response)
                        print('Сервер завершает работу...')
                        # Закрываем все соединения и завершаем работу
                        sock.close()
                        serv_sock.close()
                        exit(0)

                    # Обычная обработка - преобразование в верхний регистр
                    response = data_decoded.upper().encode('utf-8')
                    print(f'Send: "{response.decode("utf-8")}", to {addr}')

                    try:
                        sock.sendall(response)
                    except ConnectionError:
                        print(f'Клиент {addr} внезапно отключился, не могу отправить данные')
                        break

                print(f"Отключение по {addr}")