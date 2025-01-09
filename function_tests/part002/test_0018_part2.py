from conftest import *
import re
import textfsm
import time
@pytest.mark.part2
@pytest.mark.proxy_arp_check
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.008:Проверка системных Proxy ARP')
@allure.title('В данном тесте будем проверять работу arp-proxy')     
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param("DUT1"), 
 			 pytest.param("DUT2")
			]
			)
def test_arp_proxy_off(DUT):
    router = setting_ME(DUT)
    with open('config_OOP.json', 'r', encoding='utf-8') as file:
        check = json.load(file)
    arp_proxy_off(check['DUT3']['host_ip'], check['DUT3']['hostname'], check['DUT3']['login'], check['DUT3']['password'],
                   check['DUT3']['int']['to_phys1']['int_name'], check['DUT3']['int']['to_phys2']['int_name']) 
    conn = Telnet()
    acc = Account(router.login, router.password)
    conn.connect(router.host_ip)
    conn.login(acc)
    allure.attach.file('./network-schemes/part2_18_arp_proxy.png','Схема теста',attachment_type=allure.attachment_type.PNG)    
    if router.hostname==check['DUT1']['hostname']:
     change_int(conn, '192.168.60.1/24', '192.168.55.1/30')
     clear_arp(conn)     
     cmd='ping 192.168.60.254'     
     conn.execute(cmd)
     allure.attach(conn.response,'Результат пинга при выключенном Proxy ARP.', attachment_type=allure.attachment_type.TEXT)
    else:
     change_int(conn, '192.168.60.254/24', '192.168.55.6/30')
     clear_arp(conn)     
     cmd='ping 192.168.60.1'
     conn.execute(cmd)
     allure.attach(conn.response,'Результат пинга при выключенном Proxy ARP.', attachment_type=allure.attachment_type.TEXT)
    resp1 = conn.response
    template1 = open('./templates/parse_arp_ping.txt')
    fsm1 = textfsm.TextFSM(template1)
    result1 = fsm1.ParseTextToDicts(resp1)
    percent=result1[0]['success_rate']
#    allure.attach(percent, '% пакетов успешно доставлено( '+ cmd + ')', attachment_type=allure.attachment_type.TEXT)
    assert_that(percent == '0.0','Ping проходит, хотя arp proxy отключен')
#    conn.close()
@pytest.mark.part2
@pytest.mark.proxy_arp_check
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.8:Проверка системных Proxy ARP')
@allure.title('В данном тесте будем проверять работу arp-proxy')
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')  
@pytest.mark.parametrize("DUT",
			[
			 pytest.param("DUT3")
			]
			)
def test_arp_proxy_on(DUT):
    router = setting_ME(DUT)
    with open('config_OOP.json', 'r', encoding='utf-8') as file:
        check = json.load(file)
    conn = Telnet()
    acc = Account(router.login, router.password)
    conn.connect(router.host_ip)
    conn.login(acc)
    allure.attach.file('./network-schemes/part2_18_arp_proxy.png','Схема теста',attachment_type=allure.attachment_type.PNG)    
    arp_proxy_on(check['DUT3']['host_ip'], check['DUT3']['hostname'], check['DUT3']['login'], check['DUT3']['password'],
                   check['DUT3']['int']['to_phys1']['int_name'], check['DUT3']['int']['to_phys2']['int_name'])  
    if router.hostname==DUT1['hostname']:    
     cmd='ping 192.168.60.254'
     conn.execute(cmd)
     allure.attach(conn.response,'Результат пинга при включенном Proxy ARP.', attachment_type=allure.attachment_type.TEXT)
    else:  
     cmd='ping 192.168.60.1'
     conn.execute(cmd)
     allure.attach(conn.response,'Результат пинга при включенном Proxy ARP.', attachment_type=allure.attachment_type.TEXT)
    resp1 = conn.response
    template1 = open('./templates/parse_arp_ping.txt')
    fsm1 = textfsm.TextFSM(template1)
    result1 = fsm1.ParseTextToDicts(resp1)
    percent=result1[0]['success_rate']
#    allure.attach(percent, '% пакетов успешно доставлено( '+ cmd + ')', attachment_type=allure.attachment_type.TEXT)
    assert_that(percent != '0.0','Ping не проходит, хотя arp proxy включен')
   # conn.close()


