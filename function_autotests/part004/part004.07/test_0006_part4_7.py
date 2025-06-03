from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.07:Функциональное тестирование LDPoRSVP')
@allure.story('Проверка наличия необходимых маршрутов до CE')
@pytest.mark.part4_7
@pytest.mark.ldp_over_rsvp
@pytest.mark.dependency(depends=["load_config47_dut1","load_config47_dut2","load_config47_dut3","load_config47_dut4","load_config47_dut6"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password', [(DUT1['host_ip'], DUT1['hostname'] , DUT1['login'] , DUT1['password']),(DUT2['host_ip'], DUT2['hostname'] , DUT2['login'] , DUT2['password'])])
def test_ldporsvp_route_to_CE_part4_7 (ip, hostname, login, password):   
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('show route vrf VRF40 bgp')
    resp = conn.response
    allure.attach(resp, 'Вывод команды: show route vrf VRF40 bgp', attachment_type=allure.attachment_type.TEXT)
    template = open('./templates/parse_show_bgp_route.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseTextToDicts(resp)
    prefix = result[0]['net']
    prefix1 = result[1]['net']
    connected_via = result[0]['via_ip']
    connected_via1 = result[1]['via_ip']
   
    if ip == DUT1['host_ip']:
      assert_that (prefix == '192.168.42.0/24', 'Некорректное значение prefix, вместо 192.168.42.0/24 получаем %s'%prefix)
      assert_that (connected_via == '1.0.0.2', 'Некорректное значение connected_via, вместо 1.0.0.2 получаем %s'%connected_via)

      assert_that (prefix1 == '192.168.168.42/32', 'Некорректное значение prefix1, вместо 192.168.168.42/32 получаем %s'%prefix1)
      assert_that (connected_via1 == '1.0.0.2', 'Некорректное значение connected_via1, вместо 1.0.0.2 получаем %s'%connected_via1)
      
    if ip == DUT2['host_ip']:
      assert_that (prefix == '192.168.47.0/24', 'Некорректное значение prefix, вместо 192.168.47.0/24 получаем %s'%prefix)
      assert_that (connected_via == '1.0.0.3', 'Некорректное значение connected_via, вместо 1.0.0.3 получаем %s'%connected_via)

      assert_that (prefix1 == '192.168.168.47/32', 'Некорректное значение prefix1, вместо 192.168.168.47/32 получаем %s'%prefix1)
      assert_that (connected_via1 == '1.0.0.3', 'Некорректное значение connected_via1, вместо 1.0.0.3 получаем %s'%connected_via1)
