from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.02:Функциональное тестирование IS-IS') 
@allure.title('Проверка вывода команды show route rib summary точное кол-во различных типов маршрутов НЕ проверяется, т.к. оно отличается у разных рутеров тестового стенда')
@pytest.mark.part4_2
@pytest.mark.show_route_rib_summary
@pytest.mark.dependency(depends=["load_config042_dut1","load_config042_dut2","load_config042_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_route_rib_summary_part4_2 (DUT): 
# В данном тесте будем проверять вывод команды 'show route rib summary' точное кол-во различных типов маршрутов НЕ проверяется, т.к. оно отличается у разных рутеров тестового стенда
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('show route rib summary') 
    resp = conn.response
    resp_output=resp.partition('show route rib summary') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды show route rib summary', attachment_type=allure.attachment_type.TEXT)    
#    print('show route rib summary  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show route rib summary'
# C помощью магии модуля textFSM сравниваем вывод команды 'show route rib summary' c шаблоном в файле parse_show_route_rib_summary.txt 
    template = open('./templates/parse_show_route_rib_summary.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга 
    conn.send('quit\r')
    conn.close()
    Top = result[0][0]
    static_ipv4 = result[0][1]
    static_ipv6 = result[0][2]
    connected_ipv4 = result[0][3]
    connected_ipv6 = result[0][4]
    local_ipv4 = result[0][5]
    local_ipv6 = result[0][6]
    ospf_ipv4 = result[0][7]
    ospf_ipv6 = result[0][8]
    isis_ipv4 = result[0][9]
    isis_ipv6 = result[0][10]
    bgp_ipv4 = result[0][11]
    bgp_ipv6 = result[0][12]
    lfa_ipv4 = result[0][13]
    lfa_ipv6 = result[0][14]
    summary_ipv4 = result[0][15]
    summary_ipv6 = result[0][16]
    def_origin_ipv4 = result[0][17]
    def_origin_ipv6 = result[0][18]
    fib_installed_ipv4 = result[0][19]
    fib_installed_ipv6 = result[0][20]
    assert_that((ospf_ipv4=='0') and (ospf_ipv6=='0'),"Количество OSPFv2 маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 0, однако ospf_ipv4=%s и ospf_ipv6=%s"%(ospf_ipv4,ospf_ipv6))
    assert_that((isis_ipv4=='13') and (isis_ipv6=='13'),"Количество ISIS маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 13, однако isis_ipv4=%s и isis_ipv6=%s"%(isis_ipv4,isis_ipv6))
    assert_that((bgp_ipv4=='0') and (bgp_ipv6=='0'),"Количество BGP маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 0, однако bgp_ipv4=%s и bgp_ipv6=%s"%(bgp_ipv4,bgp_ipv6))
    assert_that((lfa_ipv4=='0') and (lfa_ipv6=='0'),"Количество LFA маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 0, однако lfa_ipv4=%s и lfa_ipv6=%s"%(lfa_ipv4,lfa_ipv6))
    assert_that((summary_ipv4=='0') and (summary_ipv6=='0'),"Количество Summary маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 0, однако summary_ipv4=%s и summary_ipv6=%s"%(summary_ipv4,summary_ipv6))
    assert_that((def_origin_ipv4=='0') and (def_origin_ipv6=='0'),"Количество default origin маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 0, однако def_origin_ipv4=%s и def_origin_ipv6=%s"%(def_origin_ipv4,def_origin_ipv6))
    assert_that((static_ipv4=='0') or (static_ipv4=='1') and (static_ipv6=='0'),"Количество статических маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 0, однако static_ipv4=%s и static_ipv6=%s"%(static_ipv4,static_ipv6))
    assert_that((connected_ipv4=='3') or (connected_ipv4=='4') and (connected_ipv6=='3'),"Количество connected маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 3, однако connected_ipv4=%s и connected_ipv6=%s"%(connected_ipv4,connected_ipv6))
    assert_that((local_ipv4=='4') or (local_ipv4=='5') and (local_ipv6=='4'),"Количество local маршрутов (ipv4/ipv6) в RIB в данном тесте должно быть равно 4, однако local_ipv4=%s и local_ipv6=%s"%(local_ipv4,local_ipv6))
