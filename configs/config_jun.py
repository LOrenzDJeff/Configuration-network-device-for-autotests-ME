import telnetlib

class setting_vMX():
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
        self.tn.read_until(b"login: ", timeout=30)
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ", timeout=30)
        self.tn.write(self.password.encode('ascii') + b"\n")
        self.tn.read_until(b'>', timeout=30)

    def startup(self):
        self.tn.write(b'start shell\n')
        self.tn.read_until(b'%', timeout=30)     
        self.tn.write(b'tftp %s\n'%self.server.encode('ascii'))  #Подключаемся к TFTP серверу
        self.tn.read_until(b'tftp>', timeout=30)     
        self.tn.write(b'mode octet\n')  # Данная команда понадобилась при замене vMX c версией JunOS 14 на vMX c версией 17
        self.tn.read_until(b'tftp>', timeout=30)
        self.tn.write(b'get ./%s/startup_config/%s/startup-cfg-cli.txt\n'%(self.stend.encode('ascii'), self.hostname.encode('ascii')))  
        self.tn.read_until(b'tftp>', timeout=30)  
        self.tn.write(b'quit\n')
        self.tn.read_until(b'%', timeout=30)
        self.tn.write(b'exit\n')
        self.tn.read_until(b'>', timeout=30)
        self.tn.write(b'configure\n')
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b'load override startup-cfg-cli.txt\n') # Это жесткая перезапись всей конфигурации
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b'commit\n')
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b'exit\n')
        self.tn.read_until(b'>', timeout=30)

    def ipv4(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b'# ', timeout=30)
        self.tn.write(b"set interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid1.encode('ascii') + b" vlan-id " + self.vlanid1.encode('ascii') + b"\n")
        self.tn.read_until(b'# ', timeout=30)
        self.tn.write(b"set interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid1.encode('ascii') + b" family inet address " + self.vlanip1.encode('ascii') + b"\n")
        self.tn.read_until(b'# ', timeout=30)
        self.tn.write(b"set interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid2.encode('ascii') + b" vlan-id " + self.vlanid2.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"set interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid2.encode('ascii') + b" family inet address " + self.vlanip2.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"set interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid3.encode('ascii') + b" vlan-id " + self.vlanid3.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"set interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid3.encode('ascii') + b" family inet address " + self.vlanip3.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b'exit\n')
        self.tn.read_until(b'>', timeout=30)

    def no_ipv4(self):
        self.tn.write(b"config\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"delete interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid1.encode('ascii') + b" family inet address " + self.vlanip1.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"delete interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid2.encode('ascii') + b" family inet address " + self.vlanip2.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"delete interfaces " + self.int.encode('ascii') + b" unit " + self.vlanid3.encode('ascii') + b" family inet address " + self.vlanip3.encode('ascii') + b"\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b"commit\n")
        self.tn.read_until(b'#', timeout=30)
        self.tn.write(b'exit\n')
        self.tn.read_until(b'#', timeout=30)

    def close(self):
        self.tn.write(b'exit\n')
        self.tn.close()