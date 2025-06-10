#Управление RSVP
class RSVPManager:
    #Необходимые переменные
    def __init__(self, connection, isis_config, loopback):
        self.tn = connection
        self.isis_config = isis_config
        self.loopback = loopback

    #Добавление RSVP через json
    def add_rsvp(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"mpls\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"rsvp\n")
        self.tn.read_until(b"(config-rsvp)#", timeout=30)
        for i in [self.neighor1['int_name'], self.neighor2['int_name'],self.neighor3['int_name']]:
            self.tn.write(b"interface " + i.encode('ascii') + b"\n")
            self.tn.write(b"exit\n")
        self.tn.write(b"exit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config-mpls)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)