from all_lib import *

class setting_ME():
    #Инициализация устройства
    def __init__(self, DUT, authorization):
        try:
            self.hostname = authorization[DUT]["hostname"]
            self.hardware = authorization[DUT]["hardware"]
            self.software = authorization[DUT]["software"]
            self.proto = authorization[DUT]["proto"]
            self.host_ip = authorization[DUT]["host_ip"]
            self.login = authorization[DUT]["login"]
            self.password = authorization[DUT]["password"]
            self.vrf = authorization[DUT]["vrf"]
            self.neighor1 = authorization[DUT]["int"]["to_phys1"]
            self.neighor2 = authorization[DUT]["int"]["to_phys2"]
            self.neighor3 = authorization[DUT]["int"]["to_virt"]
            self.loopback = authorization[DUT]["int"]["lo"]
            self.boot_timer = authorization[DUT]["boot_timer"]
            self.server = authorization["DUT7"]
            self.connection()
        except KeyError:
            print("В файле json не достаёт ключа")
    
    def connection(self):
        acc = Account(self.login, self.password)
        self.con = Telnet()
        self.con.connect(self.host_ip) 
        self.con.set_prompt('#')
        self.con.login(acc)

    def close(self):
        self.con.close()

    #Загрузка чистой конфигурации
    def startup(self):
        acc = Account(self.login, self.password)
        con1 = Telnet()
        con1.connect(self.host_ip) 
        con1.set_prompt('#')
        con1.login(acc)
        if self.vrf == "default":
            con1.execute("copy tftp://%s/startup_config/%s/startup-cfg-cli fs://candidate-config"%(self.server['ip'], self.hostname))
        else:
            con1.execute("copy tftp://%s/startup_config/%s/startup-cfg-cli fs://candidate-config vrf %s"%(self.server['ip'], self.hostname, self.vrf))
        con1.set_prompt('\[n\]')
        con1.execute('commit replace')
        con1.set_prompt('Commit successfully completed')
        con1.send('y\r')
        try:
            con1.execute('y')
        except:
            print("\rСработал блок except\r")
            resp=con1.response
            print('\rResp на execute y из except: %s\r'%resp)
            raise # Добавил команду чтобы фикстура генерировала Error в случае срабатывания exception

    #Добавление ipv4 из config.json
    def ipv4(self):
        self.con.set_prompt('#')
        self.con.execute("config")
        self.con.execute("int " + self.neighor1['int_name'])
        self.con.execute("ipv4 address " + self.neighor1['ip'])
        self.con.execute('description ' + self.neighor1['neighbor'])
        self.con.execute("int " + self.neighor2['int_name'])
        self.con.execute("ipv4 address " + self.neighor2['ip'])
        self.con.execute('description ' + self.neighor2['neighbor'])
        self.con.execute("int " + self.neighor3['int_name'])
        self.con.execute("ipv4 address " + self.neighor3['ip'])
        self.con.execute('description ' + self.neighor3['neighbor'])
        self.con.execute("encapsulation outer-vid " + self.neighor3['vlan'])
        self.con.execute("commit")
        self.con.execute("end")

    #Изменение ipv4 в одном интерфейсе
    def change_ipv4(self, int, old_ip, new_ip):
        self.con.execute("config")
        self.con.execute("int " + int)
        self.con.execute("no ipv4 address " + old_ip)
        self.con.execute("ipv4 address " + new_ip)
        self.con.execute("commit")
        self.con.execute("end")

    #Удаление всех ipv4, которые находятся в config_OOP.json
    def no_ipv4(self):
        self.con.execute("config")
        self.con.execute("int " + self.neighor1['int_name'])
        self.con.execute("no ipv4 address " +  self.neighor1['ip'])
        self.con.execute("int " +  self.neighor2['int_name'])
        self.con.execute("no ipv4 address " + self.neighor2['i[]'])
        self.con.execute("exit")
        self.con.execute("no int " + self.neighor3['int_name'])
        self.con.execute("commit")
        self.con.execute("end")

    #Добавление loopback из config_OOP.json
    def loopback_ipv4(self):
        self.con.execute("config")
        self.con.execute("int loopback " + self.loopback['num'])
        self.con.execute("ipv4 address " + self.loopback['ip'])
        self.con.execute("commit")
        self.con.execute("end")

    #Добавление нового loopback
    def add_new_loopback(self, id, ip):
        self.con.execute("config")
        self.con.execute("int loopback " + id)
        self.con.execute("ipv4 address " + ip)
        self.con.execute("commit")
        self.con.execute("end")

    #Изменение ipv4 у указанного loopback
    def change_loopback(self, id, old_ip, new_ip):
        self.con.execute("config")
        self.con.execute("int loopback " + id)
        self.con.execute("no ipv4 address " + old_ip)
        self.con.execute("ipv4 address " + new_ip)
        self.con.execute("commit")
        self.con.execute("end")

    #Удаление указанного loopback
    def deleted_othet_loopback(self, id):
        self.con.execute("config")
        self.con.execute("no int loopback " + id)
        self.con.execute("commit")
        self.con.execute("end")

    #Удаление loopback, который находится в config_OOP.json
    def no_loopback(self):
        self.con.execute("config")
        self.con.execute("no int loopback " + self.loopback["num"])
        self.con.execute("commit")
        self.con.execute("end")

    #Агрегирование интерфейсов из config_OOP.json
    def lacp(self):
        self.con.execute("config")
        self.con.execute("int " + self.neighor1['int_name'])
        self.con.execute("int " + self.neighor2['int_name'])
        self.con.execute("lacp")
        self.con.execute("int " + self.neighor1['int_name'])
        self.con.execute("int " + self.neighor2['int_name'])
        for i in self.neighor1['interface']:
            self.con.execute("int " + i)
            self.con.execute("bundle id " + self.neighor1['id'])
            self.con.execute("bundle mode " + self.neighor1['mode'])
        for i in self.neighor2['interface']:
            self.con.execute("int " + i)
            self.con.execute("bundle id " + self.neighor2['id'])
            self.con.execute("bundle mode " + self.neighor2['mode'])
        self.con.execute("commit")
        self.con.execute("end")

    #Удаление агрегации из config_OOP.json
    def no_lacp(self):
        self.con.execute("config")
        self.con.execute("no int " + self.neighor1['int_name'])
        self.con.execute("no int " + self.neighor2['int_name'])
        self.con.execute("lacp")
        self.con.execute("no int " + self.neighor1['int_name'])
        self.con.execute("no int " + self.neighor2['int_name'])
        for i in self.neighor1['interface']:
            self.con.execute("no int " + i)
        for i in self.neighor2['interface']:
            self.con.execute("no int " + i)
        self.con.execute("commit")
        self.con.execute("end")

    def add_ntp(self):
        self.con.execute("config")
        self.con.execute("ntp vrf " + self.vrf)
        self.con.execute("server " + self.server['ip'])
        self.con.execute("commit")
        self.con.execute("end")

    def delete_ntp(self):
        self.con.execute("config")
        self.con.execute("no ntp vrf " + self.vrf)
        self.con.execute("commit")
        self.con.execute("end")

    def snmp_add(self):
        self.con.execute("config")
        self.con.execute("snmp server vrf " + self.vrf)
        self.con.execute("community label public")
        self.con.execute("community-name encrypted 8CA10161B90C")
        self.con.execute("version v2c")
        self.con.execute("rights ro")
        self.con.execute("exit")
        self.con.execute("community label private")
        self.con.execute("community-name encrypted BEBD045EB50C5AFE75")
        self.con.execute("rights rw")
        self.con.execute("commit")
        self.con.execute("end")

    def delete_snmp(self):
        self.con.execute("config")
        self.con.execute("no snmp server vrf " + self.vrf)
        self.con.execute("commit")
        self.con.execute("end")

    def lldp_agent_add(self):
        self.con.execute("config")
        for i in range(2):
            self.con.execute("lldp interface " + self.neighor1['interface'][i])
            self.con.execute("agent nearest-bridge")
            self.con.execute("exit")
        for i in range(2):
            self.con.execute("lldp interface " + self.neighor2['interface'][i])
            self.con.execute("agent nearest-bridge")
            self.con.execute("exit")
        self.con.execute("commit")
        self.con.execute("end")