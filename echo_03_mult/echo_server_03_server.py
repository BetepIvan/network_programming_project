import socket
import threading

HOST = '127.0.0.1'
PORT = 50431


def handle_connection(sock, addr, clients):
    """Обработка подключения клиента в отдельном потоке"""
    with sock:
        print(f"Подключение по {addr}")
        clients.append((sock, addr, threading.current_thread()))  # Добавляем клиента в список

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

                # Уведомляем всех клиентов о выключении сервера
                for client_sock, client_addr, client_thread in clients:
                    if client_sock != sock:  # Не уведомляем клиента, который инициировал выключение
                        try:
                            client_sock.sendall('Сервер выключается'.encode('utf-8'))
                        except:
                            pass

                # Закрываем все соединения
                for client_sock, client_addr, client_thread in clients:
                    try:
                        client_sock.close()
                    except:
                        pass

                # Завершаем работу сервера
                print("\nПроцесс завершен с кодом выхода 0")
                exit(0)

            # Обычная обработка - преобразование в верхний регистр
            response = data_decoded.upper().encode('utf-8')
            print(f'Send: "{response.decode("utf-8")}", to {addr}')

            try:
                sock.sendall(response)
            except ConnectionError:
                print(f'Клиент {addr} внезапно отключился, не могу отправить данные')
                break

        # Удаляем клиента из списка при отключении
        for i, (client_sock, client_addr, client_thread) in enumerate(clients):
            if client_addr == addr:
                clients.pop(i)
                break

        print(f"Отключение по {addr}")


if __name__ == '__main__':
    clients = []  # Список активных клиентов

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()

        print(f'Многопоточный сервер запущен на {HOST}:{PORT}')
        print(f'Поддерживает одновременную работу нескольких клиентов')

        while True:
            print('\nОжидаю соединения...')
            my_sock, my_addr = serv_sock.accept()

            # Создаем и запускаем поток для обработки клиента
            thread = threading.Thread(target=handle_connection, args=(my_sock, my_addr, clients))
            thread.daemon = True  # Поток завершится при завершении основного потока
            print(f'Запущен поток для клиента {my_addr}: {thread.name}')
            thread.start()