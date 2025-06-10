#Настройка BGP
class BGPManager:
    #Необходимые переменные
    def __init__(self, connection, neighbor1, neighbor2, neighbor3, loopback):
        self.tn = connection
        self.neighor1 = neighbor1
        self.neighor2 = neighbor2
        self.neighor3 = neighbor3
        self.loopback = loopback

    #Добавление BGP на интерфейсы указанных в json
    def base_configure_bgp(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router bgp 65100\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        self.tn.write(b"bgp router-id " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        for i in [self.neighor1['loopback'], self.neighor2['loopback']]:
            self.tn.write(b"neighbor " + i.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-neighbor)#", timeout=30)
            self.tn.write(b"peer-group-name Internal\n")
            self.tn.write(b"update-source " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
            self.tn.write(b"exit\n")
            self.tn.read_until(b"(config-bgp)#", timeout=30)
        
        self.tn.write(b"peer-group Internal\n")
        self.tn.read_until(b"(config-peer-group)#", timeout=30)
        for i in ['ipv4','ipv6','vpnv4']:
            self.tn.write(b"address-family " + i.encode('ascii') + b" unicast\n")
            self.tn.write(b"exit\n")
        self.tn.write(b"remote-as 65100\n")
        self.tn.write(b"send-community\n")
        self.tn.write(b"send-community-ext\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление BGP на интерфейсы через параметры
    def custom_bgp(self, numas, neighbor, address_family, vrf):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router bgp " + numas.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        
        self.tn.write(b"neighbor " + neighbor.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-neighbor)#", timeout=30)
        self.tn.write(b"peer-group-name Internal\n")
        self.tn.write(b"update-source " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        
        self.tn.write(b"peer-group Internal\n")
        self.tn.read_until(b"(config-peer-group)#", timeout=30)
        self.tn.write(b"address-family " + address_family.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-peer-group)#", timeout=30)
        self.tn.write(b"remote-as " + numas.encode('ascii') + b"\n")
        self.tn.write(b"send-community\n")
        self.tn.write(b"send-community-ext\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        if vrf != 'default':
            self.tn.write(b"vrf " + vrf.encode('ascii') + b"\n")
        self.tn.write(b"bgp router-id " + self.loopback['ip_witout_mask'].encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    #Добавление редистрибьюции
    def redistribution(self, numas, family, type, rule, redist, name, vrf="default"):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router bgp " + numas.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        self.tn.write(b"address-family " + family.encode('ascii') + b" " + type.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"redistribution " + redist.encode('ascii') + b" " + rule.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")

        if vrf != "default":
            self.tn.write(b"vrf " + vrf.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-vrf)#", timeout=30)
        
        self.tn.write(b"address-family " + family.encode('ascii') + b" " + type.encode('ascii') + b"\n")
        self.tn.write(b"redistribution " + redist.encode('ascii') + b" " + name.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)

    def bgp_simple(self,numas,neighbor,src,redist):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router bgp " + numas.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        
        self.tn.write(b"neighbor " + neighbor.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-neighbor)#", timeout=30)
        self.tn.write(b"address-family ipv4 unicast\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"remote-as " + numas.encode('ascii') + b"\n")
        self.tn.write(b"update-source " + src.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        
        self.tn.write(b"address-family ipv4 unicast\n")
        self.tn.write(b"redistribution connected c\n")
        self.tn.write(b"exit\n")
        self.tn.write(b"network " + redist.encode('ascii') + b"\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-bgp)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)