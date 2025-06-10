#Настройка интерфейсов
class InterfaceManager:
    #Инициализация необходимых переменных
    def __init__(self, connection, neighbor1, neighbor2, neighbor3, loopback):
        self.tn = connection
        self.neighor1 = neighbor1
        self.neighor2 = neighbor2
        self.neighor3 = neighbor3
        self.loopback = loopback

    #Добавление IPv4 на интерфейсы указанных в json
    def base_configure_ipv4(self):
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

    #Добавление IPv6 на интерфейсы указанных в json
    def base_configure_ipv6(self):
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

    #Добавление IP на интерфейс указанный в параметре
    def custom_configure_interface(self, version, interface, ip, vrf = "default"):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + interface.encode('ascii') + b"\n")
        self.tn.write(version.encode('ascii') + b" address " + ip.encode('ascii') + b"\n")
        self.tn.write(b"load-interval 20\n")
        if vrf != "default":
            self.tn.write(b"vrf " + vrf.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление IP на интерфейс c тегом указанный в параметре
    def custom_configure_subinterface(self, interface, vlan, ip, vrf = "default"):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + interface.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-tengigabitethernet-sub)#", timeout=30)
        self.tn.write(b"encapsulation outer-vid " + vlan.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + ip.encode('ascii') + b"\n")
        if vrf != "default":
            self.tn.write(b"vrf " + vrf.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление IP на интерфейс c двойным тегом указанный в параметре
    def custom_configure_subinterface_doubletag(self, interface, outvlan, invlan, ip, vrf = "default"):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"int " + interface.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-tengigabitethernet-sub)#", timeout=30)
        self.tn.write(b"encapsulation outer-vid " + outvlan.encode('ascii') + b" inner-vid " + invlan.encode('ascii') + b"\n")
        self.tn.write(b"ipv4 address " + ip.encode('ascii') + b"\n")
        if vrf != "default":
            self.tn.write(b"vrf " + vrf.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Удаление интерфейса указанного в параметре
    def delete_interface(self, interface):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"no int " + interface.encode('ascii') + b"\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление IPv4 в loopback указанный в json
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

    #Добавление IPv6 в loopback указанный в json
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

    #Создание loopback указанный в параметре
    def custom_loopback(self, id, ip):
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

    #Настройка lacp взятых из json
    def base_configure_lacp(self):
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

    #Настройка lldp взятых из json
    def base_configure_lldp(self):
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