from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('terminal datadump')
        conn.execute('config')
        conn.execute('router isis test')
        conn.execute('interface bundle-ether 1')
        conn.execute('lfa protection disable')
        conn.execute('commit')
        conn.execute('do show route isis')
        resp = conn.response
        conn.execute('no lfa protection disable')
        conn.execute('commit')
        conn.execute('end')
        conn.send('quit\r')
        return resp
    except OSError as osE:
        pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
    except Exception as e:
        pytest.fail(f"Error in execute_command: {e}")
    finally:
        if conn is not None:
            conn.close()


@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.04:Функциональное тестирование IGP LFA')
@allure.title(
    'Выполнение команды lfa protection disable на интерфейсе bu1 и проверка вывода команды show route isis')
@pytest.mark.part4_4
@pytest.mark.lfa_protect_disable
@pytest.mark.dependency(depends=["load_config044_dut1","load_config044_dut2","load_config044_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_lfa_protect_disable_part4_4(DUT):
    # В данном тесте будем проверять вывод команды 'show route isis' после того как выполним команду lfa protection disable в режиме конфигурации isis interface bu1
    # Ожидаем что не найдем ни каких маршрутов с backup информацией через bu1
    #    allure.attach.file('./network-schemes/part4_2_show_route_isis_lfa_disable_bu1.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show route isis при lfa protection disable для bu1',
                  attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_route_isis_lfa_protect_disable.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
    #    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    assert len(result) == 4, f'Кол-во маршрутов в результате парсинга должно быть равно 4, а не {len(result)}'

    prefix1_ipv4 = result[0][0]
    nexthop1_ipv4 = result[0][1]
    interface1_ipv4 = result[0][2]

    prefix2_ipv4 = result[1][0]
    nexthop2_ipv4 = result[1][1]
    interface2_ipv4 = result[1][2]

    prefix1_ipv6 = result[2][3]
    nexthop1_ipv6 = result[2][4]
    interface1_ipv6 = result[2][5]

    prefix2_ipv6 = result[3][3]
    nexthop2_ipv6 = result[3][4]
    interface2_ipv6 = result[3][5]

    if DUT.hostname == DUT1.hostname:
        allure.attach.file('./network-schemes/part4_2_show_route_isis_lfa_disable_bu1_atAR1.png',
                           'Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)
        assert_that((prefix1_ipv4 == DUT3.loopback['ip']) and (nexthop1_ipv4 == DUT3.neighor1["ip"][0:-3]) and 
                    (interface1_ipv4 == DUT.neighor1["int_name"]),
                    "Маршрут к IPv4 префиксу 1 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 1.0.0.1/32, nexthop - 192.168.55.2, outgoing interface - bu1" % (
                    prefix1_ipv4, nexthop1_ipv4, interface1_ipv4))
        assert_that(
            (prefix2_ipv4 == DUT3.neighor3["ip_network"]) and (nexthop2_ipv4 == DUT3.neighor1["ip"][0:-3]) and 
            (interface2_ipv4 == DUT.neighor1["int_name"]),
            "Маршрут к IPv4 префиксу 2 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 192.168.55.16/30, nexthop - 192.168.55.5, outgoing interface - bu1" % (
            prefix2_ipv4, nexthop2_ipv4, interface2_ipv4))
        assert_that((prefix1_ipv6 == DUT3.loopback['ipv6']) and (nexthop1_ipv6 != '') and (
                    interface1_ipv6 == DUT.neighor1["int_name"]),
                    "Маршрут к IPv6 префиксу 1 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 2001:0:10:1::1/128, nexthop - fe80::aaf9:4bff:fe8b:9402, outgoing interface - bu1" % (
                    prefix1_ipv6, nexthop1_ipv6, interface1_ipv6))
        assert_that((prefix2_ipv6 == DUT4.vlanipv6_1) and (nexthop2_ipv6 != '') and (
                    interface2_ipv6 == DUT.neighor1["int_name"]),
                    "Маршрут к IPv6 префиксу 2 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 2001:db8:cafe:a011::/64, nexthop - fe80::aaf9:4bff:fe8b:9402, outgoing interface - bu1" % (
                    prefix2_ipv6, nexthop2_ipv6, interface2_ipv6))
    elif DUT.hostname == DUT2.hostname:
        allure.attach.file('./network-schemes/part4_2_show_route_isis_lfa_disable_bu1_atAR2.png',
                           'Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)

        assert_that((prefix1_ipv4 == DUT3.loopback['ip']) and (nexthop1_ipv4 == DUT3.neighor2["ip"][0:-3]) and (interface1_ipv4 == DUT.neighor1["int_name"]),
                    "Маршрут к IPv4 префиксу 1 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 1.0.0.1/32, nexthop - 192.168.55.5, outgoing interface - bu1" % (
                    prefix1_ipv4, nexthop1_ipv4, interface1_ipv4))
        assert_that(
            (prefix2_ipv4 == DUT3.neighor3["ip_network"]) and (nexthop2_ipv4 == DUT3.neighor2["ip"][0:-3]) and (interface2_ipv4 == DUT.neighor1["int_name"]),
            "Маршрут к IPv4 префиксу 2 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 192.168.55.16/30, nexthop - 192.168.55.5, outgoing interface - bu1" % (
            prefix2_ipv4, nexthop2_ipv4, interface2_ipv4))
        assert_that((prefix1_ipv6 == DUT3.loopback['ipv6']) and (nexthop1_ipv6 != '') and (
                    interface1_ipv6 == DUT.neighor1["int_name"]),
                    "Маршрут к IPv6 префиксу 1 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 2001:0:10:1::1/128, nexthop - fe80::aaf9:4bff:fe8b:9403, outgoing interface - bu1" % (
                    prefix1_ipv6, nexthop1_ipv6, interface1_ipv6))
        assert_that((prefix2_ipv6 == DUT4.vlanipv6_1) and (nexthop2_ipv6 != '') and (
                    interface2_ipv6 == DUT.neighor1["int_name"]),
                    "Маршрут к IPv6 префиксу 2 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 2001:db8:cafe:a011::/64, nexthop - fe80::aaf9:4bff:fe8b:9403, outgoing interface - bu1" % (
                    prefix2_ipv6, nexthop2_ipv6, interface2_ipv6))
    elif DUT.hostname == DUT3.hostname:
        allure.attach.file('./network-schemes/part4_2_show_route_isis_lfa_disable_bu1_atDR1.png',
                           'Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)

        assert_that(prefix1_ipv4 == DUT1.loopback['ip'] and nexthop1_ipv4 == DUT1.neighor1["ip"][0:-3] and interface1_ipv4 == DUT.neighor1["int_name"],
                    "Маршрут к IPv4 префиксу 1 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 1.0.0.3/32, nexthop - 192.168.55.1, outgoing interface - bu1" % (
                    prefix1_ipv4, nexthop1_ipv4, interface1_ipv4))
        assert_that(prefix2_ipv4 == DUT1.neighor3["ip_network"] and nexthop2_ipv4 == DUT1.neighor1["ip"][0:-3] and interface2_ipv4 == DUT.neighor1["int_name"],
                    "Маршрут к IPv4 префиксу 2 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 192.168.55.8/30, nexthop - 192.168.55.1, outgoing interface - bu1" % (
                    prefix2_ipv4, nexthop2_ipv4, interface2_ipv4))
        assert_that(
            prefix1_ipv6 ==  DUT4.vlanipv6_2 and nexthop1_ipv6 != '' and interface1_ipv6 == DUT.neighor1["int_name"],
            "Маршрут к IPv6 префиксу 1 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 2001:db8:cafe:a013::/64, nexthop - fe80::e2d9:e3ff:fedf:34b6, outgoing interface - bu1" % (
            prefix1_ipv6, nexthop1_ipv6, interface1_ipv6))
        assert_that(
            prefix2_ipv6 == DUT1.loopback['ipv6'] and nexthop2_ipv6 != '' and interface2_ipv6 == DUT.neighor1["int_name"],
            "Маршрут к IPv6 префиксу 2 %s через nexthop %s и исходящий интерфейс %s не соответствует шаблону. Ожидаемые значения: prefix - 2003:0:10:1::3/128, nexthop - fe80::e2d9:e3ff:fedf:34b6, outgoing interface - bu1" % (
            prefix2_ipv6, nexthop2_ipv6, interface2_ipv6))
