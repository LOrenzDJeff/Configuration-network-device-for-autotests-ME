#Управление ISIS
class ISISManager:
    #Необходимые переменные
    def __init__(self, connection, isis_config, hostname, neighbor1, neighbor2, neighbor3, loopback):
        self.tn = connection
        self.isis = isis_config
        self.hostname = hostname
        self.neighor1 = neighbor1
        self.neighor2 = neighbor2
        self.neighor3 = neighbor3
        self.loopback = loopback
        
    #Настройка isis взятых из json
    def base_configure_isis(self):
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

    #Настройка isis указанный в параметре
    def custom_isis(self,interface):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router isis test\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)

        self.tn.write(b"interface " + interface.encode('ascii') + b"\n")
        self.tn.write(b"address-family ipv4 unicast\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"bfd fast-detect\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.write(b"address-family ipv6 unicast\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.write(b"point-to-point\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)

        self.tn.write(b"interface " + self.loopback['interface'].encode('ascii') + b"\n")
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

    # Добавление lfa
    def lfa(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router isis test\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"address-family ipv4 unicast\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"lfa include-all\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"address-family ipv6 unicast\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"lfa include-all\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    # Добавление metric
    def metric(self, interface, metric):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router isis test\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"interface " + interface.encode('ascii') + b"\n")
        self.tn.write(b"level level-2\n")
        self.tn.read_until(b"(config-level)#", timeout=30)
        self.tn.write(b"metric " + str(metric).encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    def redistribution(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router isis test\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"address-family ipv4 unicast\n")
        self.tn.write(b"redistribution connected c\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-isis)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)