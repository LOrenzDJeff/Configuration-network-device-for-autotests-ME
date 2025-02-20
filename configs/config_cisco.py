import telnetlib

class setting_Cisco():
    def __init__(self, DUT, authorization,hardware_set_id):
        self.hostname = authorization[DUT]["hostname"]
        self.hardware = authorization[DUT]["hardware"]
        self.software = authorization[DUT]["software"]
        self.proto = authorization[DUT]["proto"]
        self.host_ip = authorization[DUT]["host_ip"]
        self.login = authorization[DUT]["login"]
        self.password = authorization[DUT]["password"]
        self.int = authorization[DUT]["int"]
        self.vlanid1 = authorization[DUT]["vlan1"]["id"]
        self.vlanid2 = authorization[DUT]["vlan2"]["id"]
        self.vlanid3 = authorization[DUT]["vlan3"]["id"]
        self.vlanip1 = authorization[DUT]["vlan1"]["ipv4"]
        self.vlanip2 = authorization[DUT]["vlan2"]["ipv4"]
        self.vlanip3 = authorization[DUT]["vlan3"]["ipv4"]
        self.loip = authorization[DUT]["lo"]["ip"]
        self.lonum = authorization[DUT]["lo"]["num"]
        self.server = authorization["DUT7"]["ip"]
        self.stend = hardware_set_id
    
    def connection(self):
        self.tn = telnetlib.Telnet(self.host_ip)
        self.tn.read_until(b"Username: ", timeout=120)
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ", timeout=120)
        self.tn.write(self.password.encode('ascii') + b"\n")

    def close(self):
        self.tn.write(b"exit\n")
        self.tn.close()

    def startup(self):
        self.tn.write(b'config\n')
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"load tftp://%s/%s/startup_config/%s/startup-cfg-cli\n"%(self.server.encode('ascii'), self.stend.encode('ascii'), self.hostname.encode('ascii')))
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b'commit replace\n')
        self.tn.read_until(b'Do you wish to proceed? [no]:', timeout=120)
        self.tn.write(b'yes\n')
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b'exit\n')
        self.tn.read_until(b"#", timeout=120)
    
    def ipv4(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"int " + self.int.encode('ascii') + b"." + self.vlanid1.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"ipv4 address " + self.vlanip1.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"encapsulation dot1q " + self.vlanid1.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"int " + self.int.encode('ascii') + b"." + self.vlanid2.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"ipv4 address " + self.vlanip2.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"encapsulation dot1q " + self.vlanid2.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"int " + self.int.encode('ascii') + b"." + self.vlanid3.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"ipv4 address " + self.vlanip3.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"encapsulation dot1q " + self.vlanid3.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"commit\n")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=120)

    def no_ipv4(self):
        self.tn.write("config")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write("delete interfaces " + self.int + " unit " + self.vlanid1 + " family inet address " + self.vlanip1)
        self.tn.read_until(b"#", timeout=120)
        self.tn.write("delete interfaces " + self.int + " unit " + self.vlanid2 + " family inet address " + self.vlanip2)
        self.tn.read_until(b"#", timeout=120)
        self.tn.write("delete interfaces " + self.int + " unit " + self.vlanid3 + " family inet address " + self.vlanip3)
        self.tn.read_until(b"#", timeout=120)
        self.tn.write("commit")
        self.tn.read_until(b"#", timeout=120)
        self.tn.write("end")
        self.tn.read_until(b"#", timeout=120)