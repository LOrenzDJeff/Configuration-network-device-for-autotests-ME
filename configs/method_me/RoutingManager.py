#Управление статическими маршрутами
class RoutingManager:
    #Необходимые переменные
    def __init__(self, connection):
        self.tn = connection

    #Добавление статического маршрута
    def add_static(self, family, type, destination, hop, vrf):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"router static\n")
        self.tn.read_until(b"(config-static)#", timeout=30)

        if vrf != "default":
            self.tn.write(b"vrf " + vrf.encode('ascii') + b"\n")
            self.tn.read_until(b"(config-vrf)#", timeout=30)

        self.tn.write(b"address-family " + family.encode('ascii') + b" " + type.encode('ascii') + b"\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"destination " + destination.encode('ascii') + b" " + hop.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-unicast)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)