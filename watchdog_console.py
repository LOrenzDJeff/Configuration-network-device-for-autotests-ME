from concurrent.futures import ThreadPoolExecutor
from collections import Counter

from conftest import *

server_host = '192.168.16.115'
devices = [
    {'ip': DUT1.host_ip, 'login': DUT1.login, 'password': DUT1.password, 'console_port': DUT1.port,
     'log_file': 'reports/atAR1_console_output.log', 'report': 'reports/monitor_report_atAR1.txt'},
    {'ip': DUT3.host_ip, 'login': DUT3.login, 'password': DUT3.password, 'console_port': DUT3.port,
     'log_file': 'reports/atDR1_console_output.log', 'report': 'reports/monitor_report_atDR1.txt'},
    {'ip': DUT2.host_ip, 'login': DUT2.login, 'password': DUT2.password, 'console_port': DUT2.port,
     'log_file': 'reports/atAR2_console_output.log', 'report': 'reports/monitor_report_atAR2.txt'},
]
keywords = ["Assertion failed", "crash-info", "pp-manager not response", "SIGFAULT", "coredump", "memory leak"]

def get_name_software(ip, login, password):
    tn = telnetlib.Telnet(ip, 23)
    tn.write(b"\n")
    tn.read_until(b"login: ")
    tn.write(login.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

    tn.read_until(b'#')
    tn.write(b"show system\n")
    time.sleep(1)

    output = tn.read_very_eager().decode('ascii')
    tn.write(b"quit\n")

    device_name = re.search(r"\s+System name:\s+(\S+)", output).group(1)
    firmware_version = re.search(r"\s+System software:\s+Eltex Network OS for ME5k version (\S+)", output).group(1)
    uptime = re.search(r"\s+System uptime:\s+(.+)", output).group(1)
    return device_name, firmware_version, uptime


def generate_report(device, hostname, software, connect_time, disconnect_time, output_analysis, uptime):
    with open(device['report'], 'a') as rep:
        rep.write(f'Устройство: {hostname}\n')
        rep.write(f'Версия ПО: {software}\n')
        rep.write(f'Uptime: {uptime}\n')
        rep.write(f'Дата и время начала мониторинга: {connect_time}\n')
        rep.write(f'Дата и время окончания мониторинга: {disconnect_time}\n')
        rep.write(f'Результат анализа консольного вывода:\n{output_analysis}\n')


# Логируем и анализируемым вывод консоли
def connect_and_log(device):
    counters = Counter({key: 0 for key in keywords})
    with open(device['log_file'], 'w'):
        pass
    with open(device['report'], 'w'):
        pass
    max_attempts = 3
    attempt = 0  # Счетчик попыток
    connected = False
    tn = None
    start_monitor_date_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Время начала мониторинга
    print(f"{device['ip']}. Дата и время начала мониторинга: {start_monitor_date_time}")
    while tests_running.is_set():  # Цикл логирования работает, пока выполняются тесты
        try:
            if not connected:
                # Попытка подключиться к устройству
                attempt += 1
                if attempt > max_attempts:
                    print(f"Не удалось подключиться к {server_host}:{device['console_port']} после {max_attempts} попыток")
                    break

                tn = telnetlib.Telnet(server_host, device['console_port'])
                connected = True
                attempt = 0  # Сбрасываем счетчик попыток после успешного подключения
                print(f"Подключение к {server_host}:{device['console_port']} успешно")

            # Логирование и анализ консольного вывода
            with open(device['log_file'], 'a') as log:
                output = tn.read_until(b"\n", timeout=5).decode("utf-8")
                log.write(output)
                log.flush()  # Немедленно записываем данные в файл
                for keyword in keywords:
                    if keyword in output:
                        counters[keyword] += 1

        except IOError as e:
            if e.errno == errno.EPIPE:
                print(f"Broken pipe. Порт {server_host}:{device['console_port']} временно заблокирован")
                connected = False
                time.sleep(10)
        except (EOFError, ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Соединение с {server_host}:{device['console_port']} потеряно: {e}")
            connected = False
            time.sleep(5)
        except Exception as e:
            print(f"Ошибка при подключении к {server_host}:{device['console_port']}: {e}")
            connected = False
            break  # Прерываем цикл, если возникла непредвиденная ошибка

    # Фиксируем время окончания мониторинга и создаем отчет после завершения всех попыток
    end_monitor_date_time = time.strftime('%Y-%m-%d %H:%M:%S')
    # Получаем информацию о ПО устройства
    try:
        device_name, firmware_version, uptime = get_name_software(device['ip'], device['login'], device['password'])
    except Exception as e:
        print(f"Ошибка при попытке подключиться и получить информацию с устройства {device['ip']}: {e}")
        device_name = firmware_version = uptime = 'Unknown '

    print(f"Устройство: {device_name}\nВерсия ПО: {firmware_version}")
    generate_report(device, device_name, firmware_version, start_monitor_date_time, end_monitor_date_time,
        dict(counters), uptime)
    if connected:
        tn.close()
        print(f"Отключение от {server_host}:{device['console_port']}\n"
              f"Дата и время окончания мониторинга: {end_monitor_date_time}")
    else:
        print(f"Не удалось подключиться к {server_host}:{device['console_port']} после всех попыток")


def run_tests():
    print("Запуск тестов...")
    with open('reports/function_test_cron.log', 'w') as log_file:
        subprocess.run(["python3", "-m", "pytest", "./function_autotests/", "-s", "-v", "--disable-warnings", "--alluredir=./new_result/"],
                       stdout=log_file,
                       stderr=log_file)


# Флаг для состояния тестов
tests_running = threading.Event()
tests_running.set()

"""Пул потоков для подключения и логирования, где сначала подключаемся к консоли каждого устройства, 
    а после в новом потоке запускаем тесты"""
with ThreadPoolExecutor(max_workers=len(devices) + 1) as executor:
    futures = [executor.submit(connect_and_log, device) for device in devices]
    test_future = executor.submit(run_tests)

    test_future.result()  # Ожидание окончания тестов
    tests_running.clear()  # Останавливаем логирование после тестов
    print("Тесты завершены")

# Ожидаем завершения всех потоков логирования
for future in futures:
    future.result()

print("Все подключения закрыты")
