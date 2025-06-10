#Управление LDP
class LDPManager:
    #Необходимые переменные
    def __init__(self, connection, neighbor1, neighbor2, neighbor3, loopback):
        self.tn = connection
        self.neighor1 = neighbor1
        self.neighor2 = neighbor2
        self.neighor3 = neighbor3
        self.loopback = loopback

    #Настройка ldp взятых из json
    def base_configure_ldp(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"mpls\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"ldp\n")
        self.tn.read_until(b"(config-ldp)#", timeout=30)
        for i in [self.neighor1['int_name'], self.neighor2['int_name'],self.neighor3['int_name']]:
            self.tn.write(b"discovery interface " + i.encode('ascii') + b"\n")
            self.tn.write(b"exit\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)
    
    #Настройка ldp указанный в параметре
    def custom_ldp(self, interface):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"mpls\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"ldp\n")
        self.tn.read_until(b"(config-ldp)#", timeout=30)
        self.tn.write(b"discovery interface " + interface.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление соседей в ldp
    def neighbor(self, neighbor):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"mpls\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"ldp\n")
        self.tn.read_until(b"(config-ldp)#", timeout=30)
        self.tn.write(b"neighbor " + neighbor.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    