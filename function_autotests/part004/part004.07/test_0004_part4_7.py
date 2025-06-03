from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.07:Функциональное тестирование LDPoRSVP')
@allure.story('Проверка установления LDP-соседств P-PE')
@pytest.mark.part4_7
@pytest.mark.ldp_over_rsvp
@pytest.mark.dependency(depends=["load_config47_dut1","load_config47_dut2","load_config47_dut3","load_config47_dut4","load_config47_dut6"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password', [(DUT1['host_ip'], DUT1['hostname'] , DUT1['login'] , DUT1['password']),(DUT2['host_ip'], DUT2['hostname'], DUT2['login'] , DUT2['password']),(DUT3['host_ip'], DUT3['hostname'], DUT3['login'] , DUT3['password'])])
def test_ldporsvp_P_PE_part4_7 (ip, hostname, login, password):   
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('show mpls ldp neighbors')
    resp = conn.response
    allure.attach(resp, 'Вывод команды: show mpls ldp neighbors', attachment_type=allure.attachment_type.TEXT)
      
    template = open('./templates/parse_show_mpls_ldp_neighbors.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseTextToDicts(resp)
    neighbor = result[0]['neighbor']   
    if ip == DUT3['host_ip']:
     neighbor1 = result[1]['neighbor'] 
     assert_that (neighbor == '1.0.0.3:0', 'Некорректное значение neighbor, вместо 1.0.0.3:0 получаем %s'%neighbor)
     assert_that (neighbor1 == '1.0.0.4:0', 'Некорректное значение neighbor, вместо 1.0.0.4:0 получаем %s'%neighbor)
    if ip == DUT2['host_ip']:
      assert_that (neighbor == '1.0.0.4:0', 'Некорректное значение neighbor, вместо 1.0.0.4:0 получаем %s'%neighbor)
    if ip == DUT1['host_ip']:
      assert_that (neighbor == '1.0.0.1:0', 'Некорректное значение neighbor, вместо 1.0.0.1:0 получаем %s'%neighbor)
    
