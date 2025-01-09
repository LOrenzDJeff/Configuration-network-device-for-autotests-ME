from all_lib import *

class setting_MES():
    def __init__(self, DUT, authorization):
        self.hostname = authorization[DUT]["hostname"]
        self.hardware = authorization[DUT]["hardware"]
        self.software = authorization[DUT]["software"]
        self.proto = authorization[DUT]["proto"]
        self.host_ip = authorization[DUT]["host_ip"]
        self.login = authorization[DUT]["login"]
        self.password = authorization[DUT]["password"]
        self.server = authorization["DUT7"]
        self.connection()

    def connection(self):
        acc = Account(self.login, self.password)
        self.con = Telnet()
        self.con.set_driver(MES5324CliDriver())
        self.con.connect(self.host_ip) 
        self.con.login(acc)

    def init_reboot(self): # Передаём в фикстуру параметры: ip - адрес куда подключаемся; hostname -имя узла куда подключаемся; part - раздел документации для которого будет качаться конфигурация
        def ping_device(ip, event):
            while not event.is_set():
                response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE)
                #print(response) #Информация о пинге
                if response.returncode == 0:
                    event.set()
                time.sleep(1)

        def reboot_device(ip, hostname, login, password, event):
            conn = Telnet()
            acc = Account(login, password)
            conn.set_driver(MES5324CliDriver())
            conn.connect(ip)
            conn.login(acc)

            # Копируем начальные конфигурации с tftp сервера для MES коммутатора (Device Under Test - DUT)
            conn.set_prompt('[N]')
            conn.execute('boot config tftp://%s/startup_config/%s/startup-cfg.txt' %(self.server['ip'],hostname))
            conn.set_prompt('#')
            conn.execute('Y')
            conn.set_prompt('[N]')
            conn.execute('reload')
            conn.send('Y')
            conn.set_prompt('Shutting down ...')
            conn.execute('Y')
            conn.close()

            ping_thread = threading.Thread(target=ping_device, args=(ip, event))
            ping_thread.start()

            start_time = time.time()
            event.wait(400)  # Ждем сигнала или истечения времени ожидания
            elapsed_time = time.time() - start_time

            if event.is_set():
                print(f"Коммутатор успешно перезагрузился за {elapsed_time:.2f} секунд")
                time.sleep(20)
                conn1 = Telnet()
                acc1 = Account(login, password)
                conn1.set_driver(MES5324CliDriver())
                conn1.connect(ip)
                conn1.login(acc1)
                conn1.set_prompt('#')
                conn1.execute('show version')
            else:
                print("Превышено время ожидания перезагрузки коммутатора")
                pytest.fail("Превышено время ожидания перезагрузки коммутатора")
            
            ping_thread.join()

        event = threading.Event()
        reboot_thread = threading.Thread(target=reboot_device, args=(self.host_ip, self.hostname, self.login, self.password, event))
        reboot_thread.start()
        reboot_thread.join()

    def close(self):
        self.con.close()