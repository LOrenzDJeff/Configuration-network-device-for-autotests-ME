#Управление MPLS
class MPLSManager:
    #Необходимые переменные
    def __init__(self, connection, neighbor1, neighbor2, neighbor3, loopback):
        self.tn = connection
        self.neighor1 = neighbor1
        self.neighor2 = neighbor2
        self.neighor3 = neighbor3
        self.loopback = loopback

    #Настройка mpls взятых из json
    def base_configure_mpls(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"mpls\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"forwarding\n")
        self.tn.read_until(b"(config-forwarding)#", timeout=30)
        for i in [self.neighor1['int_name'], self.neighor2['int_name'],self.neighor3['int_name'],self.loopback['interface']]:
            self.tn.write(b"interface " + i.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"router-id " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"transport-address " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Настройка mpls указанный в параметре
    def custom_mpls(self, interface):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"mpls\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"forwarding\n")
        self.tn.read_until(b"(config-forwarding)#", timeout=30)
        for i in [interface, self.loopback['interface']]:
            self.tn.write(b"interface " + i.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"router-id " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"transport-address " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление vrf
    def vrf(self, name, e, i, rd):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"vrf " + name.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-vrf)#", timeout=30)
        self.tn.write(b"export route-target " + e.encode('ascii') + b"\n")
        self.tn.write(b"import route-target " + i.encode('ascii') + b"\n")
        self.tn.write(b"rd " + rd.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)