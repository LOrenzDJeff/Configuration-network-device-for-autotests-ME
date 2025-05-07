import telnetlib
import time

class setting_ME():
    #Инициализация устройства
    def __init__(self, DUT, authorization):
        try:
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
        except KeyError:
            print("В файле json не достаёт ключа")

    def connection(self):
        self.tn = telnetlib.Telnet(self.server['ip'], self.port)
        self.tn.write(b"\n")
        self.tn.read_until(b"login: ", timeout=30)
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ", timeout=30)
        self.tn.write(self.password.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=30)

    def close(self):
        self.tn.write(b"quit\n")
        self.tn.close()

    def startup(self):
        if self.vrf == "default":
            self.tn.write(b"copy tftp://%s/%s/startup_config/%s/startup-cfg-cli fs://candidate-config\n"%(self.server['ip'].encode('ascii'),  self.stend.encode('ascii'),  self.hostname.encode('ascii')))
        else:
            self.tn.write(b"copy tftp://%s/%s/startup_config/%s/startup-cfg-cli fs://candidate-config vrf %s\n"%( self.server['ip'].encode('ascii'), self.stend.encode('ascii'), self.hostname.encode('ascii'), self.vrf.encode('ascii')))
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"commit replace\n")
        self.tn.read_until(b"[n]", timeout=30)
        self.tn.write(b"y\n")
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"end\n")
        time.sleep(2)

    #Добавление ipv4 из config.json
    def ipv4(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"ipv4 address " + self.neighor1['ip'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor1['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"ipv4 address " + self.neighor2['ip'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor2['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor3['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-tengigabitethernet-sub)#", timeout=30)
        self.tn.write(b"ipv4 address " + self.neighor3['ip'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor3['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"encapsulation outer-vid " + self.neighor3['vlan'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
    
    def ipv6(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"ipv6 address " + self.neighor1['ipv6'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor1['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"ipv6 address " + self.neighor2['ipv6'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor2['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor3['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-tengigabitethernet-sub)#", timeout=30)
        self.tn.write(b"ipv6 address " + self.neighor3['ipv6'].encode('ascii') + b"\n")
        self.tn.write(b"description " + self.neighor3['neighbor'].encode('ascii') + b"\n")
        self.tn.write(b"encapsulation outer-vid " + self.neighor3['vlan'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
    
    #Изменение ip в одном интерфейсе
    def change_ipv4(self, int, old_ip, new_ip):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + int.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"no ipv4 address " + old_ip.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + new_ip.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Удаление всех ipv4, которые находятся в config_OOP.json
    def no_ipv4(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"no ipv4 address " +  self.neighor1['ip'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " +  self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"no ipv4 address " + self.neighor2['i[]'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int " + self.neighor3['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    def no_ipv6(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"no ipv6 address " +  self.neighor1['ipv6'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " +  self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"no ipv6 address " + self.neighor2['ipv6'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int " + self.neighor3['int_name'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
    
    #Добавление loopback из config_OOP.json
    def loopback_ipv4(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int loopback " + self.loopback['num'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-loopback)#", timeout=30)
        self.tn.write(b"ipv4 address " + self.loopback['ip'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-loopback)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    def loopback_ipv6(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int loopback " + self.loopback['num'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-loopback)#", timeout=30)
        self.tn.write(b"ipv6 address " + self.loopback['ipv6'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-loopback)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление нового loopback
    def add_new_loopback(self, id, ip):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int loopback " + id.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-loopback)#", timeout=30)
        self.tn.write(b"ipv4 address " + ip.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Изменение ipv4 у указанного loopback
    def change_loopback(self, id, old_ip, new_ip):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int loopback " + id.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-loopback)#", timeout=30)
        self.tn.write(b"no ipv4 address " + old_ip.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + new_ip.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Удаление указанного loopback
    def deleted_othet_loopback(self, id):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int loopback " + id.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Удаление loopback, который находится в config_OOP.json
    def no_loopback(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int loopback " + self.loopback["num"].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Агрегирование интерфейсов из config_OOP.json
    def lacp(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"lacp\n")
        self.tn.read_until(b"(config-lacp)#", timeout=30)
        self.tn.write(b"int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        self.tn.write(b"int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
        for i in self.neighor1['interface']:
            self.tn.write(b"int " + i.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-tengigabitethernet)", timeout=30)
            self.tn.write(b"bundle id " + self.neighor1['id'].encode('ascii') + b"\n")
            self.tn.read_until(b"(config-tengigabitethernet)", timeout=30)
            self.tn.write(b"bundle mode " + self.neighor1['mode'].encode('ascii') + b"\n")
        for i in self.neighor2['interface']:
            self.tn.write(b"int " + i.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-tengigabitethernet)", timeout=30)
            self.tn.write(b"bundle id " + self.neighor2['id'].encode('ascii') + b"\n")
            self.tn.read_until(b"(config-tengigabitethernet)", timeout=30)
            self.tn.write(b"bundle mode " + self.neighor2['mode'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config-tengigabitethernet)", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-lacp)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Удаление агрегации из config_OOP.json
    def no_lacp(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int " + self.neighor1['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int " + self.neighor2['int_name'].encode('ascii') + b"\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no lacp\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    def lldp_agent_add(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"lldp\n")
        self.tn.read_until(b"(config-lldp)#", timeout=30)
        for i in range(2):
            self.tn.write(b"interface " + self.neighor1['interface'][i].encode('ascii') + b"\n")
            self.tn.read_until(b"(config-tengigabitethernet)#", timeout=30)
            self.tn.write(b"agent nearest-bridge\n")
            self.tn.read_until(b"(config-agent)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-tengigabitethernet)#", timeout=30)
        for i in range(2):
            self.tn.write(b"interface " + self.neighor2['interface'][i].encode('ascii') + b"\n")
            self.tn.read_until(b"(config-tengigabitethernet)#", timeout=30)
            self.tn.write(b"agent nearest-bridge\n")
            self.tn.read_until(b"(config-agent)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-tengigabitethernet)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-lldp)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-lldp)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
        time.sleep(5)

    def isis_add(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router isis test\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)

        for i in [self.neighor1['int_name'], self.neighor2['int_name']]:
            self.tn.write(b"interface " + i.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
            self.tn.write(b"address-family ipv4 unicast\n")
            self.tn.read_until(b"(config-unicast)#", timeout=30)
            self.tn.write(b"bfd fast-detect\n")
            self.tn.read_until(b"(config-unicast)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
            self.tn.write(b"address-family ipv6 unicast\n")
            self.tn.read_until(b"(config-unicast)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
            self.tn.write(b"point-to-point\n")
            self.tn.read_until(b"(config-bundle-ether)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-isis)#", timeout=30)

        for i in [self.neighor3['int_name'], self.loopback['interface']]:
            self.tn.write(b"interface " + i.encode('ascii') + b"\n")
            if i == self.neighor3['int_name']:
                self.tn.read_until(b"(config-tengigabitethernet-sub)#", timeout=30)
                self.tn.write(b"point-to-point\n")
                self.tn.read_until(b"(config-tengigabitethernet-sub)#", timeout=30)
            else:
                self.tn.read_until(b"(config-loopback)#", timeout=30)
                self.tn.write(b"passive\n")
                self.tn.read_until(b"(config-loopback)#", timeout=30)
            self.tn.write(b"address-family ipv4 unicast\n")
            self.tn.read_until(b"(config-unicast)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.write(b"address-family ipv6 unicast\n")
            self.tn.read_until(b"(config-unicast)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-isis)#", timeout=30)

        self.tn.write(b"host-name %s\n"%self.hostname.encode('ascii'))
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"is-level level-2\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        for i in ['level level-2', 'level level-1']:
            self.tn.write(i.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-level)#", timeout=30)
            self.tn.write(b"metric-style wide\n")
            self.tn.read_until(b"(config-level)#", timeout=30)
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-isis)#", timeout=30)
        
        self.tn.write(b"net %s\n"%self.isis.encode('ascii'))
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
    
    def isis_delete(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no router isis test\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
