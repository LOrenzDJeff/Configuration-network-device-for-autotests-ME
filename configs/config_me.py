from configs.method_me.TelnetManager import *
from configs.method_me.InterfaceManager import *
from configs.method_me.ISISManager import *
from configs.method_me.MPLSManager import *
from configs.method_me.LDPManager import *
from configs.method_me.BalanceManager import *
from configs.method_me.BGPManager import *
from configs.method_me.OSPFManager import *

# Основной класс
class setting_ME:
    def __init__(self, DUT, authorization):
        try:
            # Инициализация параметров из json
            self.boot = authorization[DUT]["boot_timer"]
            self.hostname = authorization[DUT]["hostname"]
            self.dir = authorization[DUT]["dir_hostname"]
            self.hardware = authorization[DUT]["hardware"]
            self.software = authorization[DUT]["software"]
            self.port = authorization[DUT]["port"]
            self.host_ip = authorization[DUT]["host_ip"]
            self.login = authorization[DUT]["login"]
            self.password = authorization[DUT]["password"]
            self.vrf = authorization[DUT]["vrf"]
            self.neighor1 = authorization[DUT]["int"]["to_phys1"]
            self.neighor2 = authorization[DUT]["int"]["to_phys2"]
            self.neighor3 = authorization[DUT]["int"]["to_virt"]
            self.loopback = authorization[DUT]["int"]["lo"]
            self.server = authorization["DUT7"]
            self.stend = authorization['stend']
            self.isis_conf = authorization[DUT]["isis"]
            
            # Инициализация подключения
            self.telnet = TelnetManager(
                self.server['ip'], 
                self.port, 
                self.login, 
                self.password
            )
            
        except KeyError as e:
            print(f"Отсутствует ключ в JSON: {e}")

    #Загрузка стартовой конфигурации
    def startup(self):
        if self.vrf == "default":
            self.telnet.tn.write(b"copy tftp://%s/%s/startup_config/%s/startup-cfg-cli fs://candidate-config\n"%(self.server['ip'].encode('ascii'),  self.stend.encode('ascii'),  self.hostname.encode('ascii')))
        else:
            self.telnet.tn.write(b"copy tftp://%s/%s/startup_config/%s/startup-cfg-cli fs://candidate-config vrf %s\n"%( self.server['ip'].encode('ascii'), self.stend.encode('ascii'), self.hostname.encode('ascii'), self.vrf.encode('ascii')))
        self.telnet.tn.read_until(b"#", timeout=30)
        self.telnet.tn.write(b"commit replace\n")
        self.telnet.tn.read_until(b"[n]", timeout=30)
        self.telnet.tn.write(b"y\n")
        self.telnet.tn.read_until(b"#", timeout=30)
        self.telnet.tn.write(b"end\n")
        time.sleep(2)
    # Подключение к рутеру
    def connection(self):
        # Инициализация менеджеров в ./method_me
        self.telnet.connect()
        self.interface = InterfaceManager(
                self.telnet.tn, 
                self.neighor1,
                self.neighor2,
                self.neighor3,
                self.loopback
            )
        self.isis = ISISManager(
                self.telnet.tn,
                self.isis_conf,
                self.hostname, 
                self.neighor1,
                self.neighor2,
                self.neighor3,
                self.loopback
            )
        self.mpls = MPLSManager(
                self.telnet.tn, 
                self.neighor1,
                self.neighor2,
                self.neighor3,
                self.loopback
            )
        self.ldp = LDPManager(
                self.telnet.tn, 
                self.neighor1,
                self.neighor2,
                self.neighor3,
                self.loopback
            )
        self.balance = BalanceManager(
            self.telnet.tn
        )
        self.bgp = BGPManager(
            self.telnet.tn,
            self.neighor1,
            self.neighor2,
            self.neighor3,
            self.loopback
        )
        self.ospf = OSPFManager(
                self.telnet.tn,
                self.neighor1,
                self.neighor2,
                self.neighor3,
                self.loopback
        )
    # Отключение от рутера
    def close(self):
        self.telnet.close()
    # Конфигурирование lacp черзе json
    def lacp(self):
        self.interface.base_configure_lacp()
    # Конфигурирование ipv4 через json
    def ipv4(self):
        self.interface.base_configure_ipv4()
    # Конфигурирование ipv6 через json
    def ipv6(self):
        self.interface.base_configure_ipv6()
    # Конфигурирование интерфейса через параметр
    def ip_custom(self, vers, int, ip, vrf = 'default'):
        self.interface.custom_configure_interface(vers, int, ip, vrf)
    # Конфигурирование интерфейса с двумя тегами
    def double_subint(self, int, out, inv, ip, vrf = "default"):
        self.interface.custom_configure_subinterface_doubletag(int,out,inv,ip,vrf)
    # Конфигурирование ipv6 loopback через json
    def loopback_ipv6(self):
        self.interface.loopback_ipv6()
    # Конфигурирование ipv4 loopback через json
    def loopback_ipv4(self):
        self.interface.loopback_ipv4()
    # Конфигурирование lldp через json
    def lldp_agent_add(self):
        self.interface.base_configure_lldp()
    # Конфигурирование isis через json
    def isis_add(self):
        self.isis.base_configure_isis()
    # Конфигурирование isis через параметры
    def isis_custom(self,int):
        self.isis.custom_isis(int)
    # Добавление lfa в isis
    def isis_add_lfa(self):
        self.isis.lfa()
    # Добавление метрики в isis
    def isis_metric(self, interface, metric):
        self.isis.metric(interface, metric)
    def isis_redistribution(self):
        self.isis.redistribution()
    def vrf_add(self,name,e,i,rd):
        self.mpls.vrf(name,e,i,rd)
    # Конфигурирование mpls через json
    def mpls_add(self):
        self.mpls.base_configure_mpls()
    def mpls_custom(self,int):
        self.mpls.custom_mpls(int)
    # Конфигурирование ldp через json
    def ldp_add(self):
        self.ldp.base_configure_ldp()
    def ldp_custom(self,int):
        self.ldp.custom_ldp(int)
    # Добавление соседей в ldp
    def add_neighbor_ldp(self, interface):
        self.ldp.neighbor(interface)
    # Добавление hash-field
    def hash_field(self,type,direction):
        self.balance.hash_field(type, direction)
    def bgp_add(self):
        self.bgp.base_configure_bgp()
    def bgp_custom(self,num,neigb,add,vrf="default"):
        self.bgp.custom_bgp(num,neigb,add,vrf)
    def bgp_redistribution(self,num,fam,type,rule,redist,name,vrf = "default"):
        self.bgp.redistribution(num,fam,type,rule,redist,name,vrf)
    def bgp_simple_custom(self,num,neigh,src,red):
        self.bgp.bgp_simple(num,neigh,src,red)
    def ospf_custom(self,area,int):
        self.ospf.custom_OSPF(area,int)
    def ospf_metric(self,area,int,met):
        self.ospf.metric(area,int,met)
    def ospf_redistribution(self):
        self.ospf.redistribution()