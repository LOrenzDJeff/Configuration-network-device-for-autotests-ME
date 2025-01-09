from all_lib import *

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
        self.server_ipv4 = authorization["DUT7"]["ip"]
        self.server_login = authorization["DUT7"]["login"]
        self.server_password = authorization["DUT7"]["password"]
        self.connection()
    
    def connection(self):
        acc = Account(self.login, self.password)
        self.con = Telnet()
        self.con.connect(self.host_ip) 
        self.con.login(acc)

    def startup(self):
        con = Telnet()
        acc = Account(self.login, self.password)
        con.connect(self.host_ip)
        con.login(acc)
    # Копируем начальные конфигурации с tftp сервера для Juniper маршрутизатора (Device Under Test - DUT) 
        con.set_prompt('%')
        con.execute('start shell')
        con.set_prompt('tftp>')
        con.execute('tftp %s'%(self.server_ipv4))  #Подключаемся к TFTP серверу     
        con.execute('mode octet')  # Данная команда понадобилась при замене vMX c версией JunOS 14 на vMX c версией 17
        con.set_prompt('Received')
        con.execute('get ./startup_config/%s/labr01.txt'%(self.hostname))    
        con.set_prompt('%')
        con.execute('quit')
        con.set_prompt('>')
        con.execute('exit')
        con.set_prompt('#')
        con.execute('configure')
        con.set_prompt('load complete')
        con.execute('load override labr01.txt') # Это жесткая перезапись всей конфигурации
        con.set_prompt('commit complete')
        con.execute('commit')
        con.set_prompt('>')
        con.execute('exit')

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
        acc = Account(self.login, self.password)
        con = Telnet()
        self.con.connect(self.hostname) 
        self.con.login(acc)
        self.con.execute("config")
        self.con.execute("delete interfaces " + self.int + " unit " + self.vlanid1 + " family inet address " + self.vlanip1)
        self.con.execute("delete interfaces " + self.int + " unit " + self.vlanid2 + " family inet address " + self.vlanip2)
        self.con.execute("delete interfaces " + self.int + " unit " + self.vlanid3 + " family inet address " + self.vlanip3)
        self.con.execute("commit")

    def close(self):
        self.con.close()