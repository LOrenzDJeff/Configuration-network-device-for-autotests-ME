from configs.method_me.TelnetManager import *
from configs.method_me.InterfaceManager import *
from configs.method_me.ISISManager import *

# Основной класс
class setting_ME:
    def __init__(self, DUT, authorization):
        try:
            # Инициализация параметров из json
            self.boot = authorization[DUT]["boot_timer"]
            self.hostname = authorization[DUT]["hostname"]
            self.dir = authorization[DUT]["dir_hostname"]
            self.hardware = authorization[DUT]["hardware"]
            self.software = authorization[DUT]["software"]
            self.port = authorization[DUT]["port"]
            self.host_ip = authorization[DUT]["host_ip"]
            self.login = authorization[DUT]["login"]
            self.password = authorization[DUT]["password"]
            self.vrf = authorization[DUT]["vrf"]
            self.neighor1 = authorization[DUT]["int"]["to_phys1"]
            self.neighor2 = authorization[DUT]["int"]["to_phys2"]
            self.neighor3 = authorization[DUT]["int"]["to_virt"]
            self.loopback = authorization[DUT]["int"]["lo"]
            self.server = authorization["DUT7"]
            self.stend = authorization['stend']
            self.isis = authorization[DUT]["isis"]
            
            # Инициализация менеджеров в ./method_me
            self.telnet = TelnetManager(
                self.server['ip'], 
                self.port, 
                self.login, 
                self.password
            )
            self.interface = InterfaceManager(
                self.telnet.tn, 
                self.neighor1,
                self.neighor2,
                self.neighor3,
                self.loopback
            )
            self.routing = ISISManager(
                self.telnet, 
                self.isis, 
                self.loopback
            )
            
        except KeyError as e:
            print(f"Отсутствует ключ в JSON: {e}")

    #Загрузка стартовой конфигурации
    def startup(self):
        if self.vrf == "default":
            self.telnet.tn.write(b"copy tftp://%s/%s/startup_config/%s/startup-cfg-cli fs://candidate-config\n"%(self.server['ip'].encode('ascii'),  self.stend.encode('ascii'),  self.hostname.encode('ascii')))
        else:
            self.telnet.tn.write(b"copy tftp://%s/%s/startup_config/%s/startup-cfg-cli fs://candidate-config vrf %s\n"%( self.server['ip'].encode('ascii'), self.stend.encode('ascii'), self.hostname.encode('ascii'), self.vrf.encode('ascii')))
        self.telnet.tn.read_until(b"#", timeout=30)
        self.telnet.tn.write(b"commit replace\n")
        self.telnet.tn.read_until(b"[n]", timeout=30)
        self.telnet.tn.write(b"y\n")
        self.telnet.tn.read_until(b"#", timeout=30)
        self.telnet.tn.write(b"end\n")
        time.sleep(2)
    # Подключение к рутеру
    def connection(self):
        self.telnet.connect()
    # Отключение от рутера
    def close(self):
        self.telnet.close()
    # Конфигурирование lacp черзе json
    def lacp(self):
        self.interface.base_configure_lacp()
    # Конфигурирование ipv4 через json
    def ipv4(self):
        self.interface.base_configure_ipv4()