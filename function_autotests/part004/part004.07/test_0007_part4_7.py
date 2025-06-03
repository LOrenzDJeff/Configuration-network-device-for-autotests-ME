from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.07:Функциональное тестирование LDPoRSVP')
@allure.story('Проверка наличия связности между CE-устройствами')
@pytest.mark.part4_7
@pytest.mark.ldp_over_rsvp
@pytest.mark.dependency(depends=["load_config47_dut1","load_config47_dut2","load_config47_dut3","load_config47_dut4","load_config47_dut6"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password', [(DUT4['host_ip'], DUT4['hostname'] , DUT4['login'] , DUT4['password'])])
def test_ldporsvp_ping_CE1_CE2_part4_7 (ip, hostname, login, password):   
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('ping vrf vrf42 192.168.168.47 source ip 192.168.168.42')
    resp = conn.response
    allure.attach(resp, 'ping vrf vrf42 192.168.168.47 source ip 192.168.168.42', attachment_type=allure.attachment_type.TEXT)
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
    result=fsm.ParseTextToDicts(resp)
    result_loss = result[0]['loss']
    assert_that(int(result_loss)==0,"Обнаружены потери пакетов между CE1 и CE2 в размере %s %%"%result_loss)
