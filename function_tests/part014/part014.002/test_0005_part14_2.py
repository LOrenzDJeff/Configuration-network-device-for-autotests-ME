from conftest import *

#debug_cmd_list=['debug pp-mgr cmd','debug pp-mgr general','debug pp-mgr arp','debug pp-mgr bfd','debug pp-mgr egress']

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.2:Функциональное тестирование форвардинга в BGP L3VPN через RSVP LSP')
@allure.title('Проверка вывода команд show route vrf VRF40 на PE маршрутизаторах atAR1, atAR2, atDR1')
@pytest.mark.part14_2
@pytest.mark.show_route_VRF40_RSVP
@pytest.mark.dependency(depends=["load_config142_dut1","load_config142_dut2","load_config142_dut3","load_config142_dut4"],scope='session')
#@pytest.mark.parametrize('ip , hostname , login, password, debug_cmd_list', [(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'], debug_cmd_list),(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'], debug_cmd_list),(DUT3['host_ip'], DUT3['hostname'], DUT3['login'], DUT3['password'],debug_cmd_list)])
@pytest.mark.parametrize('ip , hostname , login, password', [(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password']),(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password']),(DUT3['host_ip'], DUT3['hostname'], DUT3['login'], DUT3['password'])])
def test_show_route_VRF40_part14_2 (ip, hostname, login, password): 
#def test_show_route_VRF40_part14_2 (me_open_debug_collect_logs, ip, hostname, login, password, debug_cmd_list):     
# В данном тесте будем проверять вывод команды 'show route vrf VRF40' на PE маршрутизаторах atAR1, atAR2, atDR1
    allure.attach.file('./network-schemes/part14_2_ping_over_L3VPN_VRF40.png','Схема теста:', attachment_type=allure.attachment_type.PNG)      
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    time.sleep(30)  # Надо подождать пока марщруты от CE1 будут приняты на atDR1 иначе будет assert об отстуствии соответсвующих маршрутов (см ниже)
    conn.execute('show route vrf VRF40') 
    resp = conn.response    
    resp_output=resp.partition('show route vrf VRF40') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды show route vrf VRF40', attachment_type=allure.attachment_type.TEXT)
#    print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show route vrf VRF40'
# C помощью магии модуля textFSM сравниваем вывод команды 'show route vrf VRF40' c шаблоном в файле parse_show_bgp_vrf_VRF40.txt 
    template = open('./templates/parse_show_route_vrf_VRF40.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp) 
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга    

    route_src1=processed_result[0]['route_src1']
    prefix1=processed_result[0]['rt1']
    nexthop1=processed_result[0]['nexthop1']
    metric1=processed_result[0]['metric1']
    out_int1=processed_result[0]['out_int1']

    route_src2=processed_result[0]['route_src2']
    prefix2=processed_result[0]['rt2']
    nexthop2=processed_result[0]['nexthop2']
    metric2=processed_result[0]['metric2']
    out_int2=processed_result[0]['out_int2']

    route_src3=processed_result[0]['route_src3']
    prefix3=processed_result[0]['rt3']
    nexthop3=processed_result[0]['nexthop3']
    metric3=processed_result[0]['metric3']
    out_int3=processed_result[0]['out_int3']

    total_route=processed_result[0]['total_route']
    assert_that(prefix1=='192.168.168.41/32',"В выводе команды нет маршрута к префиксу 192.168.168.41/32")
    assert_that(prefix2=='192.168.168.42/32',"В выводе команды нет маршрута к префиксу 192.168.168.42/32")
    assert_that(prefix3=='192.168.168.43/32',"В выводе команды нет маршрута к префиксу 192.168.168.43/32")

    if (hostname=='atAR1'):
        assert_that(route_src1=='B BV',"В выводе команды в строке для 192.168.168.41 значение источника маршрутной информации не равно ожидаемому B BV, а равно %s"%route_src1)
        assert_that(nexthop1=='1.0.0.1',"В выводе команды в строке для 192.168.168.41 значение next hop не равно ожидаемому 1.0.0.1, а равно %s"%nexthop1)
        assert_that(metric1=='[200/2]',"В выводе команды в строке для 192.168.168.41 значение Admin dist/Metric не равно ожидаемому [200/2], а равно %s"%metric1)

        assert_that(route_src2=='B BV',"В выводе команды в строке для 192.168.168.42 значение источника маршрутной информации не равно ожидаемому B BV, а равно %s"%route_src2)
        assert_that(nexthop2=='1.0.0.2',"В выводе команды в строке для 192.168.168.42 значение next hop не равно ожидаемому 1.0.0.2, а равно %s"%nexthop2)
        assert_that(metric2=='[200/0]',"В выводе команды в строке для 192.168.168.42 значение Admin dist/Metric не равно ожидаемому [200/0], а равно %s"%metric2)

        assert_that(route_src3=='S',"В выводе команды в строке для 192.168.168.43 значение источника маршрутной информации не равно ожидаемому S, а равно %s"%route_src3)
        assert_that(nexthop3=='192.168.43.2',"В выводе команды в строке для 192.168.168.43 значение next hop не равно ожидаемому 192.168.42.2, а равно %s"%nexthop3)
        assert_that(metric3=='[1/1]',"В выводе команды в строке для 192.168.168.43 значение Admin dist/Metric не равно ожидаемому [1/1], а равно %s"%metric3)
        assert_that(out_int3=='te0/0/11.10043',"В выводе команды в строке для 192.168.168.43 значение outgoing interface не равно ожидаемому te0/0/11.10043, а равно %s"%out_int3)
    elif (hostname=='atAR2'):
        assert_that(route_src1=='B BV',"В выводе команды в строке для 192.168.168.41 значение источника маршрутной информации не равно ожидаемому B BV, а равно %s"%route_src1)
        assert_that(nexthop1=='1.0.0.1',"В выводе команды в строке для 192.168.168.41 значение next hop не равно ожидаемому 1.0.0.1, а равно %s"%nexthop1)
        assert_that(metric1=='[200/2]',"В выводе команды в строке для 192.168.168.41 значение Admin dist/Metric не равно ожидаемому [200/2], а равно %s"%metric1)

        assert_that(route_src2=='B BE',"В выводе команды в строке для 192.168.168.42 значение источника маршрутной информации не равно ожидаемому B BE, а равно %s"%route_src2)
        assert_that(nexthop2=='192.168.42.2',"В выводе команды в строке для 192.168.168.42 значение next hop не равно ожидаемому 192.168.42.2, а равно %s"%nexthop2)
        assert_that(metric2=='[20/0]',"В выводе команды в строке для 192.168.168.42 значение Admin dist/Metric не равно ожидаемому [20/0], а равно %s"%metric2)
        assert_that(out_int2=='te0/0/11.10042',"В выводе команды в строке для 192.168.168.42 значение outgoing interface не равно ожидаемому te0/0/11.10042, а равно %s"%out_int2)

        assert_that(route_src3=='B BV',"В выводе команды в строке для 192.168.168.43 значение источника маршрутной информации не равно ожидаемому B BV, а равно %s"%route_src3)
        assert_that(nexthop3=='1.0.0.3',"В выводе команды в строке для 192.168.168.43 значение next hop не равно ожидаемому 1.0.0.3, а равно %s"%nexthop3)
        assert_that(metric3=='[200/0]',"В выводе команды в строке для 192.168.168.43 значение Admin dist/Metric не равно ожидаемому [200/0], а равно %s"%metric3)

    elif (hostname=='atDR1'):
        assert_that(route_src1=='O EA',"В выводе команды в строке для 192.168.168.41 значение источника маршрутной информации не равно ожидаемому O EA, а равно %s"%route_src1)
        assert_that(nexthop1=='192.168.41.2',"В выводе команды в строке для 192.168.168.41 значение next hop не равно ожидаемому 192.168.41.2, а равно %s"%nexthop1)
        assert_that(metric1=='[30/1]',"В выводе команды в строке для 192.168.168.41 значение Admin dist/Metric не равно ожидаемому [30/1], а равно %s"%metric1)
        assert_that(out_int1=='te0/0/5.10041',"В выводе команды в строке для 192.168.168.41 значение outgoing interface не равно ожидаемому te0/0/5.10041, а равно %s"%out_int1)

        assert_that(route_src2=='B BV',"В выводе команды в строке для 192.168.168.42 значение источника маршрутной информации не равно ожидаемому B BV, а равно %s"%route_src2)
        assert_that(nexthop2=='1.0.0.2',"В выводе команды в строке для 192.168.168.42 значение next hop не равно ожидаемому 1.0.0.2, а равно %s"%nexthop2)
        assert_that(metric2=='[200/0]',"В выводе команды в строке для 192.168.168.42 значение Admin dist/Metric не равно ожидаемому [200/0], а равно %s"%metric2)

        assert_that(route_src3=='B BV',"В выводе команды в строке для 192.168.168.43 значение источника маршрутной информации не равно ожидаемому B BV, а равно %s"%route_src3)
        assert_that(nexthop3=='1.0.0.3',"В выводе команды в строке для 192.168.168.43 значение next hop не равно ожидаемому 1.0.0.3, а равно %s"%nexthop3)
        assert_that(metric3=='[200/0]',"В выводе команды в строке для 192.168.168.43 значение Admin dist/Metric не равно ожидаемому [200/0], а равно %s"%metric3)

    assert_that(total_route=='7',"Общее кол-во маршрутов в выводе команды не равно ожидаемым 7, а равно %s"%total_route)
