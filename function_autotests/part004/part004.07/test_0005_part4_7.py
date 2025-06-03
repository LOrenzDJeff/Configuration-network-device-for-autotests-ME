from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.07:Функциональное тестирование LDPoRSVP')
@allure.story('Проверка наличия транспортного туннеля')
@pytest.mark.part4_7
@pytest.mark.ldp_over_rsvp
@pytest.mark.dependency(depends=["load_config47_dut1","load_config47_dut2","load_config47_dut3","load_config47_dut4","load_config47_dut6"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password', [(DUT3['host_ip'], DUT3['hostname'] , DUT3['login'] , DUT3['password'])])
def test_ldporsvp_P_P_part4_7 (ip, hostname, login, password):   
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('show mpls rsvp tunnels')
    resp = conn.response
    allure.attach(resp, 'Вывод команды: show mpls rsvp tunnels', attachment_type=allure.attachment_type.TEXT)
    conn.execute('show mpls ldp forwarding nexthop 1.0.0.4')
    resp1 = conn.response
    allure.attach(resp1, 'Вывод команды: show mpls ldp forwarding nexthop 1.0.0.4', attachment_type=allure.attachment_type.TEXT)
    template = open('./templates/parse_show_mpls_rsvp_tunnel.txt')
    template1 = open('./templates/parse_show_mpls_ldp_forw.txt')
    fsm = textfsm.TextFSM(template)
    fsm1 = textfsm.TextFSM(template1)
    result = fsm.ParseTextToDicts(resp)
    result1 = fsm1.ParseTextToDicts(resp1)
    tun_name = result[0]['tun_name']
    tun_src = result[0]['tun_src']
    tun_dst = result[0]['tun_dst']
    tun_status = result[0]['tun_status']
    tun_state = result[0]['tun_state']
    
    prefix = result1[0]['pref']
    prefix1 = result1[1]['pref']
    label_out = result1[0]['label_out']
    label_out1 = result1[1]['label_out']
    outgoing_int = result1[0]['outgoing_int']
    outgoing_int1 = result1[1]['outgoing_int']
    next_hop = result1[0]['next_hop']
    next_hop1 = result1[1]['next_hop']
    
    
    assert_that (tun_name == 'to_labr01', 'Некорректное значение tun_name, вместо to_labr01 получаем %s'%tun_name)
    assert_that (tun_src == '1.0.0.1', 'Некорректное значение tun_src, вместо 1.0.0.1 получаем %s'%tun_src)
    assert_that (tun_dst == '1.0.0.4', 'Некорректное значение tun_dst, вместо 1.0.0.4 получаем %s'%tun_dst)
    assert_that (tun_status == 'up', 'Некорректное значение tun_status, вместо up получаем %s'%tun_status)
    assert_that (tun_state == 'up','Некорректное значение tun_state, вместо up получаем %s'%tun_state)
    
    assert_that (prefix == '1.0.0.2/32', 'Некорректное значение prefix, вместо 1.0.0.2/32 получаем %s'%prefix)
    assert_that (label_out != 'ImpNull', 'Некорректное значение label_out, ожидалась не ImpNull-метка')
    assert_that (outgoing_int == 'tuto_labr01@lsp1', 'Некорректное значение outgoing_int, вместо tuto_labr01@lsp1 получаем %s'%outgoing_int)
    assert_that (next_hop == '1.0.0.4', 'Некорректное значение next_hop, вместо 1.0.0.4 получаем %s'%next_hop)
    
    assert_that (prefix1 == '1.0.0.4/32', 'Некорректное значение prefix1, вместо 1.0.0.4/32 получаем %s'%prefix)
    assert_that (label_out1 == 'ImpNull', 'Некорректное значение label_out1, вместо ImpNull получаем %s'%label_out1)
    assert_that (outgoing_int1 == 'tuto_labr01@lsp1', 'Некорректное значение outgoing_int1, вместо tuto_labr01@lsp1 получаем %s'%outgoing_int1)
    assert_that (next_hop1 == '1.0.0.4', 'Некорректное значение next_hop1, вместо 1.0.0.4 получаем %s'%next_hop1)
