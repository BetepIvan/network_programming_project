import socket
import sys

HOST = '127.0.0.1'
PORT = 50432


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10.0)  # Таймаут на операции с сокетом

            print(f'Попытка подключения к {HOST}:{PORT}...')
            sock.connect((HOST, PORT))
            print('Успешное подключение к серверу!')
            print('Введите сообщение для отправки на сервер.')
            print('Команды: "exit" - отключиться, "stop server" - выключить сервер')
            print('Просто нажмите Enter для проверки пустого ввода')

            while True:
                try:
                    data_to_send = input("Type the message to send: ")

                    # Если просто нажали Enter
                    if not data_to_send:
                        print("Вы отправили пустое сообщение, проверяем соединение...")
                        data_to_send = "ping"  # Отправляем тестовое сообщение

                    # Кодируем сообщение
                    data_bytes_send = data_to_send.encode('utf-8')

                    # Отправляем данные
                    sock.sendall(data_bytes_send)

                    # Получаем ответ
                    try:
                        data_bytes_received = sock.recv(1024)
                        # Если сервер закрыл соединение
                        if not data_bytes_received:
                            print("\nПрограмма на вашем хост-компьютере разорвала установленное подключение")
                            break

                        data_received = data_bytes_received.decode('utf-8')
                        print("Received:", data_received)

                        # Если сервер сообщил о выключении
                        if data_received == 'Сервер выключается':
                            print("\nСервер выключен. Пытаюсь отправить еще одно сообщение...")

                            # Пытаемся отправить еще одно сообщение
                            try:
                                sock.sendall("test after shutdown".encode('utf-8'))
                                data = sock.recv(1024)
                                if not data:
                                    print("Программа на вашем хост-компьютере разорвала установленное подключение")
                            except ConnectionError as e:
                                print("Программа на вашем хост-компьютере разорвала установленное подключение")

                            break

                    except socket.timeout:
                        print("Таймаут при получении ответа от сервера")
                        continue
                    except ConnectionError as e:
                        print(f"Программа на вашем хост-компьютере разорвала установленное подключение")
                        break

                except KeyboardInterrupt:
                    print("\n\nПрервано пользователем")
                    break
                except EOFError:
                    print("\n\nКонец ввода")
                    break
                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    break

            print("\nProcess finished with exit code 0")

    except ConnectionRefusedError:
        print(f"Не удалось подключиться к серверу {HOST}:{PORT}")
        print("Убедитесь, что сервер запущен")
        print("\nProcess finished with exit code 0")
    except socket.timeout:
        print("Таймаут при подключении к серверу")
        print("\nProcess finished with exit code 0")
    except Exception as e:
        print(f"Ошибка: {e}")
        print("\nProcess finished with exit code 0")


if __name__ == '__main__':
    main()