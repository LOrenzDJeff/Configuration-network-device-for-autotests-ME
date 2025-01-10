import telnetlib

class setting_ME():
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
            self.vrf = authorization[DUT]["vrf"]
            self.neighor1 = authorization[DUT]["int"]["to_phys1"]
            self.neighor2 = authorization[DUT]["int"]["to_phys2"]
            self.neighor3 = authorization[DUT]["int"]["to_virt"]
            self.loopback = authorization[DUT]["int"]["lo"]
            self.boot_timer = authorization[DUT]["boot_timer"]
            self.server = authorization["DUT7"]
            self.connection()
        except KeyError:
            print("В файле json не достаёт ключа")

    def connection(self):
        self.tn = telnetlib.Telnet(self.host_ip)
        self.tn.read_until(b"login: ")
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ")
        self.tn.write(self.password.encode('ascii') + b"\n")

    def close(self):
        self.tn.write(b"exit\n")

    #Загрузка чистой конфигурации
    def startup(self):
        if self.vrf == "none":
            self.tn.write(b"copy tftp://%s/startup_config/%s/startup-cfg-cli fs://candidate-config\n"%(self.server['ip'].encode('ascii'), self.hostname.encode('ascii')))
        else:
            self.tn.write(b"copy tftp://%s/startup_config/%s/startup-cfg-cli fs://candidate-config vrf %s\n"%(self.server['ip'].encode('ascii'), self.hostname.encode('ascii'), self.vrf.encode('ascii')))
        self.tn.read_until(b"#")
        self.tn.write(b"commit replace\n")
        self.tn.read_until(b"\[n\]")
        self.tn.write(b"y\n")
        self.tn.read_until(b"Commit successfully completed")

    #Добавление ipv4 из config.json
    def ipv4(self):
        self.tn.write(b"config\n")
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + self.neighor1['ip'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor1['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + self.neighor2['ip'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor2['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"int " + self.neighor3['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + self.neighor3['ip'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor3['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"encapsulation outer-vid " + self.neighor3['vlan'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#")
        self.tn.write(b"end\n")
        self.tn.read_until(b"#")
    
    #Изменение ipv4 в одном интерфейсе
    def change_ipv4(self, int, old_ip, new_ip):
        self.tn.write(b"config\n")
        self.tn.write(b"int " + int.encode('ascii') + b"\n")
        self.tn.write(b"no ipv4 address " + old_ip.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + new_ip.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#")
        self.tn.write(b"end\n")
        self.tn.read_until(b"#")

    #Удаление всех ipv4, которые находятся в config_OOP.json
    def no_ipv4(self):
        self.tn.write(b"config\n")
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"no ipv4 address " +  self.neighor1['ip'].encode('ascii') + b"\n")
        self.tn.write(b"int " +  self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"no ipv4 address " + self.neighor2['i[]'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"no int " + self.neighor3['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#")
        self.tn.write(b"end\n")
        self.tn.read_until(b"#")
    
    #Добавление loopback из config_OOP.json
    def loopback_ipv4(self):
        self.tn.write(b"config\n")
        self.tn.write(b"int loopback " + self.loopback['num'].encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + self.loopback['ip'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")

    #Добавление нового loopback
    def add_new_loopback(self, id, ip):
        self.tn.write(b"config\n")
        self.tn.write(b"int loopback " + id.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + ip.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")

    #Изменение ipv4 у указанного loopback
    def change_loopback(self, id, old_ip, new_ip):
        self.tn.write(b"config\n")
        self.tn.write(b"int loopback " + id.encode('ascii') + b"\n")
        self.tn.write(b"no ipv4 address " + old_ip.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + new_ip.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")

    #Удаление указанного loopback
    def deleted_othet_loopback(self, id):
        self.tn.write(b"config\n")
        self.tn.write(b"no int loopback " + id.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")

    #Удаление loopback, который находится в config_OOP.json
    def no_loopback(self):
        self.tn.write(b"config\n")
        self.tn.write(b"no int loopback " + self.loopback["num"].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")

    #Агрегирование интерфейсов из config_OOP.json
    def lacp(self):
        self.tn.write(b"config\n")
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"lacp\n")
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        for i in self.neighor1['interface']:
            self.tn.write(b"int " + i.encode('ascii') + b"\n")
            self.tn.write(b"bundle id " + self.neighor1['id'].encode('ascii') + b"\n")
            self.tn.write(b"bundle mode " + self.neighor1['mode'].encode('ascii') + b"\n")
        for i in self.neighor2['interface']:
            self.tn.write(b"int " + i.encode('ascii') + b"\n")
            self.tn.write(b"bundle id " + self.neighor2['id'].encode('ascii') + b"\n")
            self.tn.write(b"bundle mode " + self.neighor2['mode'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")

    #Удаление агрегации из config_OOP.json
    def no_lacp(self):
        self.tn.write(b"config\n")
        self.tn.write(b"no int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"no int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"lacp\n")
        self.tn.write(b"no int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"no int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        for i in self.neighor1['interface']:
            self.tn.write(b"no int " + i.encode('ascii') + b"\n")
        for i in self.neighor2['interface']:
            self.tn.write(b"no int " + i.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.write(b"end\n")