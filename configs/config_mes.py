import telnetlib
import threading
import time
import subprocess

class setting_MES():
    #Инициализация устройства
    def __init__(self, DUT, authorization):
        try:
            self.hostname = authorization[DUT]["hostname"]
            self.hardware = authorization[DUT]["hardware"]
            self.software = authorization[DUT]["software"]
            self.proto = authorization[DUT]["proto"]
            self.host_ip = authorization[DUT]["host_ip"]
            self.login = authorization[DUT]["login"]
            self.password = authorization[DUT]["password"]
        except KeyError:
            print("В файле json не достаёт ключа")

    def connection(self):
        self.tn = telnetlib.Telnet(self.host_ip)
        self.tn.read_until(b"login: ", timeout=30)
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ", timeout=30)
        self.tn.write(self.password.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=30)

    def close(self):
        self.tn.write(b"quit\n")
        self.tn.close()

    def init_reboot(self): # Передаём в фикстуру параметры: ip - адрес куда подключаемся; hostname -имя узла куда подключаемся; part - раздел документации для которого будет качаться конфигурация
        def ping_device(ip, event):
            while not event.is_set():
                response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE)
                #print(response) #Информация о пинге
                if response.returncode == 0:
                    event.set()
                time.sleep(1)

        def reboot_device(ip, hostname, login, password, event):
            # Копируем начальные конфигурации с tftp сервера для MES коммутатора (Device Under Test - DUT)
            tn = telnetlib.Telnet(ip)
            tn.write(login.encode('ascii') + b"\n")
            tn.read_until(b"Password: ", timeout=30)
            tn.write(password.encode('ascii') + b"\n")
            tn.read_until(b"#", timeout=30)
            tn.write(b'reload\n')
            tn.read_until(b'[N]')
            tn.write(b'Y\n')
            tn.read_until(b'This command will reset the whole system and disconnect your current session.')
            tn.write(b'Y\n')
            tn.close()
            time.sleep(10)

            ping_thread = threading.Thread(target=ping_device, args=(ip, event))
            ping_thread.start()

            start_time = time.time() + 10
            event.wait(400)  # Ждем сигнала или истечения времени ожидания
            elapsed_time = time.time() - start_time

            if event.is_set():
                print(f"Коммутатор успешно перезагрузился за {elapsed_time:.2f} секунд")
                time.sleep(20)
            else:
                print("Превышено время ожидания перезагрузки коммутатора")
            
            ping_thread.join()

        event = threading.Event()
        reboot_thread = threading.Thread(target=reboot_device, args=(self.host_ip, self.hostname, self.login, self.password, event))
        reboot_thread.start()
        reboot_thread.join()
