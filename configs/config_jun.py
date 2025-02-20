import telnetlib

class setting_vMX():
    def __init__(self, DUT, authorization):
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
    
    def connection(self):
        self.tn = telnetlib.Telnet(self.host_ip)
        self.tn.read_until(b"login: ", timeout=30)
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ", timeout=30)
        self.tn.write(self.password.encode('ascii') + b"\n")

    def startup(self):
        self.tn.read_until('%', timeout=30)
        self.tn.write(b'start shell\n')
        self.tn.read_until('tftp>', timeout=30)
        self.tn.write(b'tftp %s\n'%self.server_ipv4.encode('ascii'))  #Подключаемся к TFTP серверу     
        self.tn.write(b'mode octet\n')  # Данная команда понадобилась при замене vMX c версией JunOS 14 на vMX c версией 17
        self.tn.read_until('Received', timeout=30)
        self.tn.write(b'get ./startup_config/%s/labr01.txt\n'%self.hostname.encode('ascii'))    
        self.tn.read_until('%', timeout=30)
        self.tn.write('quit\n')
        self.tn.read_until('>', timeout=30)
        self.tn.write('exit\n')
        self.tn.read_until('#', timeout=30)
        self.tn.write('configure\n')
        self.tn.read_until('load complete', timeout=30)
        self.tn.write('load override labr01.txt\n') # Это жесткая перезапись всей конфигурации
        self.tn.read_until('commit complete', timeout=30)
        self.tn.write('commit\n')
        self.tn.read_until('>', timeout=30)
        self.tn.write('exit\n')

    def ipv4(self):
        self.con.execute("config")
        self.con.execute("set interfaces " + self.int + " unit " + self.vlanid1 + " vlan-id " + self.vlanid1)
        self.con.execute("set interfaces " + self.int + " unit " + self.vlanid1 + " family inet address " + self.vlanip1)
        self.con.execute("set interfaces " + self.int + " unit " + self.vlanid2 + " vlan-id " + self.vlanid2)
        self.con.execute("set interfaces " + self.int + " unit " + self.vlanid2 + " family inet address " + self.vlanip2)
        self.con.execute("set interfaces " + self.int + " unit " + self.vlanid3 + " vlan-id " + self.vlanid3)
        self.con.execute("set interfaces " + self.int + " unit " + self.vlanid3 + " family inet address " + self.vlanip3)
        self.con.execute("commit")

    def no_ipv4(self):
        self.con.execute("config")
        self.con.execute("delete interfaces " + self.int + " unit " + self.vlanid1 + " family inet address " + self.vlanip1)
        self.con.execute("delete interfaces " + self.int + " unit " + self.vlanid2 + " family inet address " + self.vlanip2)
        self.con.execute("delete interfaces " + self.int + " unit " + self.vlanid3 + " family inet address " + self.vlanip3)
        self.con.execute("commit")

    def close(self):
        self.con.close()