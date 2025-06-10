#Управление OSPF
class OSPFManager:
    #Необходимые переменные
    def __init__(self, connection, neighbor1, neighbor2, neighbor3, loopback):
        self.tn = connection
        self.neighor1 = neighbor1
        self.neighor2 = neighbor2
        self.neighor3 = neighbor3
        self.loopback = loopback

    #Настройка ospf указанный в параметре
    def custom_OSPF(self,area,interface):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router ospfv2 test\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"area " + area.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-area)#", timeout=30)

        self.tn.write(b"interface " + interface.encode('ascii') + b"\n")
        self.tn.write(b"network point-to-point\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-area)#", timeout=30)
        self.tn.write(b"interface " + self.loopback['interface'].encode('ascii') + b"\n")
        self.tn.write(b"passive\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-area)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)

        self.tn.write(b"router-id " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Настройка metric
    def metric(self,area,interface,metric):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router ospfv2 test\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"area " + area.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-area)#", timeout=30)

        self.tn.write(b"interface " + interface.encode('ascii') + b"\n")
        self.tn.write(b"metric " + metric.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-area)#", timeout=30)
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    def redistribution(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router ospfv2 test\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"redistribution connected c\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-ospfv2)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)