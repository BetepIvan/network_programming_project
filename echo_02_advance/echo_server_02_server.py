import socket

HOST = '127.0.0.1'
PORT = 50432

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()

        while True:
            print('Ожидаю подключения...')
            sock, addr = serv_sock.accept()
            with sock:
                print("Подключение по", addr)

                while True:
                    try:
                        data = sock.recv(1024)
                        # Проверка на отключение клиента
                        if not data:
                            print(f'Клиент {addr} отключился')
                            break

                    except ConnectionError:
                        print(f'Клиент {addr} внезапно отключился в процессе отправки данных на сервер')
                        break

                    # Декодируем данные
                    try:
                        data_str = data.decode('utf-8').strip()
                    except:
                        data_str = data.decode('latin-1').strip()

                    print(f'Received: {data_str}, from {addr}')

                    # Проверка команд
                    if not data_str:  # Пустой ввод (просто нажали Enter)
                        response = b"Введите сообщение (exit - выход)"
                        print(f'Send: {response.decode()}, to {addr}')
                        try:
                            sock.sendall(response)
                        except ConnectionError:
                            print(f'Клиент {addr} внезапно отключился не могу отправить данные')
                            break
                        continue

                    elif data_str.lower() in ['exit', 'quit']:
                        print(f'Клиент {addr} запросил отключение')
                        try:
                            sock.sendall(b'GOODBYE')
                        except:
                            pass
                        break

                    elif data_str.lower() == 'shutdown server':
                        print(f'Клиент {addr} запросил выключение сервера')
                        try:
                            sock.sendall(b'SERVER_SHUTDOWN')
                        except:
                            pass
                        # Завершаем работу сервера
                        print("Сервер завершает работу...")
                        exit(0)

                    # Обычная обработка - преобразование в верхний регистр
                    data = data_str.upper().encode()
                    print(f'Send: {data_str.upper()}, to {addr}')

                    try:
                        sock.sendall(data)
                    except ConnectionError:
                        print(f'Клиент {addr} внезапно отключился не могу отправить данные')
                        break

                print("Отключение по", addr)
