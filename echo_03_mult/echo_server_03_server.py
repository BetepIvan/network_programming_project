import socket
import threading

HOST = '127.0.0.1'
PORT = 50431

# Флаг для выключения сервера
server_running = True
server_lock = threading.Lock()

def handle_connection(sock, addr):
    global server_running

    with sock:
        print("Подключение по", addr)

        while True:
            # Проверяем, работает ли еще сервер
            with server_lock:
                if not server_running:
                    print(f'Сервер выключается, отключаем клиента {addr}')
                    try:
                        sock.sendall(b'SERVER_SHUTDOWN')
                    except:
                        pass
                    break

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
            if not data_str:  # Пустой ввод
                response = b"Введите сообщение (exit - выход, shutdown server - выключить сервер)"
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
                with server_lock:
                    server_running = False
                try:
                    sock.sendall(b'SERVER_SHUTDOWN_INITIATED')
                except:
                    pass
                break

            # Обычная обработка
            data = data_str.upper().encode()
            print(f'Send: {data_str.upper()}, to {addr}')

            try:
                sock.sendall(data)
            except ConnectionError:
                print(f'Клиент {addr} внезапно отключился не могу отправить данные')
                break

        print("Отключение по", addr)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()

        threads = []

        try:
            while server_running:
                print('Ожидаю соединения...')
                my_sock, my_addr = serv_sock.accept()
                thread = threading.Thread(target=handle_connection, args=(my_sock, my_addr))
                threads.append(thread)
                thread.start()
                print(f"Запущен поток для клиента {my_addr}")

        except KeyboardInterrupt:
            print("\nСервер останавливается...")
            with server_lock:
                server_running = False

        finally:
            # Ожидаем завершения всех потоков
            print("Ожидаю завершения клиентских соединений...")
            for thread in threads:
                thread.join(timeout=2.0)

            print("Сервер завершил работу")
            print("Process finished with exit code 0")