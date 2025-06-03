from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('terminal datadump')
        conn.execute('show isis fast-reroute')
        resp = conn.response
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
@allure.title('Проверка вывода команды show isis fast-reroute')
@pytest.mark.part4_4
@pytest.mark.show_isis_fast_reroute
@pytest.mark.dependency(depends=["load_config044_dut1","load_config044_dut2","load_config044_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1),
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_isis_fast_reroute_part4_4(DUT):
    # В данном тесте будем проверять вывод команды 'show isis fast-reroute' на соответствие шаблону из файла parse_show_isis_fast_reroute.txt
    allure.attach.file('./network-schemes/part4_2_show_isis_fast_reroute_ipv4.png',
                       'Параметры ipv4 проверяемые в тесте', attachment_type=allure.attachment_type.PNG)
    allure.attach.file('./network-schemes/part4_2_show_isis_fast_reroute_ipv6.png',
                       'Параметры ipv6 проверяемые в тесте', attachment_type=allure.attachment_type.PNG)

    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show isis fast-reroute', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_isis_fast_reroute.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
    #    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    assert len(result) == 12, f'Кол-во маршрутов в результате парсинга должно быть равно 12, а не {len(result)}'

    prefix1_ipv4 = result[0][0]
    prefix1_prim_nexthop_ipv4 = result[0][1]
    prefix1_backup_nexthop_ipv4 = result[0][2]

    prefix2_ipv4 = result[1][0]
    prefix2_prim_nexthop_ipv4 = result[1][1]
    prefix2_backup_nexthop_ipv4 = result[1][2]

    prefix3_ipv4 = result[2][0]
    prefix3_prim_nexthop_ipv4 = result[2][1]
    prefix3_backup_nexthop_ipv4 = result[2][2]

    prefix4_ipv4 = result[3][0]
    prefix4_prim_nexthop_ipv4 = result[3][1]
    prefix4_backup_nexthop_ipv4 = result[3][2]

    prefix5_ipv4 = result[4][0]
    prefix5_prim_nexthop_ipv4 = result[4][1]
    prefix5_backup_nexthop_ipv4 = result[4][2]

    prefix6_ipv4 = result[5][0]
    prefix6_prim_nexthop_ipv4 = result[5][1]
    prefix6_backup_nexthop_ipv4 = result[5][2]

    prefix1_ipv6 = result[6][3]
    prefix1_prim_nexthop_ipv6 = result[6][4]
    prefix1_backup_nexthop_ipv6 = result[6][5]

    prefix2_ipv6 = result[7][3]
    prefix2_prim_nexthop_ipv6 = result[7][4]
    prefix2_backup_nexthop_ipv6 = result[7][5]

    prefix3_ipv6 = result[8][3]
    prefix3_prim_nexthop_ipv6 = result[8][4]
    prefix3_backup_nexthop_ipv6 = result[8][5]

    prefix4_ipv6 = result[9][3]
    prefix4_prim_nexthop_ipv6 = result[9][4]
    prefix4_backup_nexthop_ipv6 = result[9][5]

    prefix5_ipv6 = result[10][3]
    prefix5_prim_nexthop_ipv6 = result[10][4]
    prefix5_backup_nexthop_ipv6 = result[10][5]

    prefix6_ipv6 = result[11][3]
    prefix6_prim_nexthop_ipv6 = result[11][4]
    prefix6_backup_nexthop_ipv6 = result[11][5]

    if DUT.hostname == DUT1.hostname:
        assert_that(
            prefix1_ipv4 == DUT2.neighor1["ip_network"] and prefix1_prim_nexthop_ipv4 == DUT2.neighor2["ip"][0:-3] and prefix1_backup_nexthop_ipv4 == DUT3.neighor1["ip"][0:-3],
            " Маршрут к префиксу 192.168.55.4/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.22, резервного nexthop-a - 192.168.55.2" % (
            prefix1_prim_nexthop_ipv4, prefix1_backup_nexthop_ipv4))
        assert_that(
            prefix2_ipv4 == DUT2.neighor3["ip_network"] and prefix2_prim_nexthop_ipv4 == DUT2.neighor2["ip"][0:-3] and prefix2_backup_nexthop_ipv4 == DUT4.ip2,
            " Маршрут к префиксу 192.168.55.12/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.22, резервного nexthop-a - 192.168.55.10" % (
            prefix2_prim_nexthop_ipv4, prefix2_backup_nexthop_ipv4))
        assert_that(
            prefix3_ipv4 == DUT3.neighor3["ip_network"] and prefix3_prim_nexthop_ipv4 == DUT3.neighor1["ip"][0:-3] and prefix3_backup_nexthop_ipv4 == DUT4.ip2,
            " Маршрут к префиксу 192.168.55.16/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.2, резервного nexthop-a - 192.168.55.10" % (
            prefix3_prim_nexthop_ipv4, prefix3_backup_nexthop_ipv4))
        assert_that(
            prefix4_ipv4 == DUT3.loopback["ip"] and prefix4_prim_nexthop_ipv4 == DUT3.neighor1["ip"][0:-3] and prefix4_backup_nexthop_ipv4 == DUT2.neighor2["ip"][0:-3],
            " Маршрут к префиксу 1.0.0.1/32 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.2, резервного nexthop-a - 192.168.55.22" % (
            prefix4_prim_nexthop_ipv4, prefix4_backup_nexthop_ipv4))
        assert_that(
            prefix6_ipv4 == DUT2.loopback["ip"] and prefix6_prim_nexthop_ipv4 == DUT2.neighor2["ip"][0:-3] and prefix6_backup_nexthop_ipv4 == DUT3.neighor1["ip"][0:-3],
            " Маршрут к префиксу 1.0.0.2/32 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.22, резервного nexthop-a - 192.168.55.2" % (
            prefix6_prim_nexthop_ipv4, prefix6_backup_nexthop_ipv4))
        assert_that(
            prefix5_ipv4 == DUT4.loip and prefix5_prim_nexthop_ipv4 == DUT4.ip2 and prefix5_backup_nexthop_ipv4 == DUT2.neighor2["ip"][0:-3],
            " Маршрут к префиксу 1.0.0.4/32 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.10, резервного nexthop-a - 192.168.55.22" % (
            prefix5_prim_nexthop_ipv4, prefix5_backup_nexthop_ipv4))

        assert_that(prefix1_ipv6 == DUT2.neighor1["ipv6_network"] and
                    prefix1_prim_nexthop_ipv6 != '' and
                                prefix1_backup_nexthop_ipv6 != '',
                    " Маршрут к префиксу 2001:db8:cafe:a001::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:feff:48b3, резервного nexthop-a - fe80::aaf9:4bff:fe8b:9402" % (
                    prefix1_prim_nexthop_ipv6, prefix1_backup_nexthop_ipv6))
        assert_that(
            prefix2_ipv6 == DUT3.neighor3["ipv6_network"] and prefix2_prim_nexthop_ipv6 != '' and prefix2_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:db8:cafe:a011::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::aaf9:4bff:fe8b:9402, резервного nexthop-a - fe80::205:8601:6071:900" % (
            prefix2_prim_nexthop_ipv6, prefix2_backup_nexthop_ipv6))
        assert_that(
            prefix3_ipv6 == DUT2.neighor3["ipv6_network"] and prefix3_prim_nexthop_ipv6 != '' and prefix3_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:db8:cafe:a012::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:feff:48b3, резервного nexthop-a - fe80::205:8601:6071:900" % (
            prefix3_prim_nexthop_ipv6, prefix3_backup_nexthop_ipv6))
        assert_that(
            prefix4_ipv6 == DUT3.loopback["ipv6"] and prefix4_prim_nexthop_ipv6 != '' and prefix4_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:0:10:1::1/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::aaf9:4bff:fe8b:9402, резервного nexthop-a - fe80::e2d9:e3ff:feff:48b3" % (
            prefix4_prim_nexthop_ipv6, prefix4_backup_nexthop_ipv6))
        assert_that(
            prefix5_ipv6 == DUT2.loopback["ipv6"] and prefix5_prim_nexthop_ipv6 != '' and prefix5_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2002:0:10:1::2/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:feff:48b3, резервного nexthop-a - fe80::aaf9:4bff:fe8b:9402" % (
            prefix5_prim_nexthop_ipv6, prefix5_backup_nexthop_ipv6))
        assert_that(
            prefix6_ipv6 == DUT4.loipv6 and prefix6_prim_nexthop_ipv6 != '' and prefix6_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2004:0:10:1::4/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::205:8601:6071:900, резервного nexthop-a - fe80::e2d9:e3ff:feff:48b3" % (
            prefix6_prim_nexthop_ipv6, prefix6_backup_nexthop_ipv6))
    elif DUT.hostname == DUT2.hostname:
        assert_that(
            prefix1_ipv4 == DUT1.neighor1["ip_network"] and prefix1_prim_nexthop_ipv4 == DUT1.neighor2["ip"][0:-3] and prefix1_backup_nexthop_ipv4 == DUT3.neighor2["ip"][0:-3],
            " Маршрут к префиксу 192.168.55.0/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.21, резервного nexthop-a - 192.168.55.5" % (
            prefix1_prim_nexthop_ipv4, prefix1_backup_nexthop_ipv4))
        assert_that(
            prefix2_ipv4 == DUT1.neighor3["ip_network"] and prefix2_prim_nexthop_ipv4 == DUT1.neighor2["ip"][0:-3] and prefix2_backup_nexthop_ipv4 == DUT4.ip3,
            " Маршрут к префиксу 192.168.55.8/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.21, резервного nexthop-a - 192.168.55.14" % (
            prefix2_prim_nexthop_ipv4, prefix2_backup_nexthop_ipv4))
        assert_that(
            prefix3_ipv4 == DUT3.neighor3["ip_network"] and prefix3_prim_nexthop_ipv4 == DUT3.neighor2["ip"][0:-3] and prefix3_backup_nexthop_ipv4 == DUT4.ip3,
            " Маршрут к префиксу 192.168.55.16/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.5, резервного nexthop-a - 192.168.55.14" % (
            prefix3_prim_nexthop_ipv4, prefix3_backup_nexthop_ipv4))
        assert_that(
            prefix4_ipv4 == DUT3.loopback["ip"] and prefix4_prim_nexthop_ipv4 == DUT3.neighor2["ip"][0:-3] and prefix4_backup_nexthop_ipv4 == DUT1.neighor2["ip"][0:-3],
            " Маршрут к префиксу 1.0.0.1/32 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.5, резервного nexthop-a - 192.168.55.21" % (
            prefix4_prim_nexthop_ipv4, prefix4_backup_nexthop_ipv4))
        assert_that(
            prefix5_ipv4 == DUT1.loopback["ip"] and prefix5_prim_nexthop_ipv4 == DUT1.neighor2["ip"][0:-3] and prefix5_backup_nexthop_ipv4 == DUT3.neighor2["ip"][0:-3],
            " Маршрут к префиксу %s через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.21, резервного nexthop-a - 192.168.55.5" % (
            prefix5_ipv4, prefix5_prim_nexthop_ipv4, prefix5_backup_nexthop_ipv4))
        assert_that(
            prefix6_ipv4 == DUT4.loip and prefix6_prim_nexthop_ipv4 == DUT4.ip3 and prefix6_backup_nexthop_ipv4 == DUT1.neighor2["ip"][0:-3],
            " Маршрут к префиксу %s через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.14, резервного nexthop-a - 192.168.55.21" % (
            prefix6_ipv4, prefix6_prim_nexthop_ipv4, prefix6_backup_nexthop_ipv4))

        assert_that(
            prefix1_ipv6 == DUT1.neighor1["ipv6_network"] and prefix1_prim_nexthop_ipv6 != '' and prefix1_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:db8:cafe:a003::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:fedf:34b7, резервного nexthop-a - fe80::aaf9:4bff:fe8b:9403" % (
            prefix1_prim_nexthop_ipv6, prefix1_backup_nexthop_ipv6))
        assert_that(
            prefix2_ipv6 == DUT3.neighor3["ipv6_network"] and prefix2_prim_nexthop_ipv6 != '' and prefix2_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:db8:cafe:a011::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::aaf9:4bff:fe8b:9403, резервного nexthop-a - fe80::205:8601:5f71:900" % (
            prefix2_prim_nexthop_ipv6, prefix2_backup_nexthop_ipv6))
        assert_that(
            prefix3_ipv6 == DUT1.neighor3["ipv6_network"] and prefix3_prim_nexthop_ipv6 != '' and prefix3_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:db8:cafe:a013::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:fedf:34b7, резервного nexthop-a - fe80::205:8601:5f71:900" % (
            prefix3_prim_nexthop_ipv6, prefix3_backup_nexthop_ipv6))
        assert_that(
            prefix4_ipv6 == DUT3.loopback["ipv6"] and prefix4_prim_nexthop_ipv6 != '' and prefix4_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2001:0:10:1::1/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::aaf9:4bff:fe8b:9403, резервного nexthop-a - fe80::e2d9:e3ff:fedf:34b7" % (
            prefix4_prim_nexthop_ipv6, prefix4_backup_nexthop_ipv6))
        assert_that(
            prefix5_ipv6 == DUT1.loopback["ipv6"] and prefix5_prim_nexthop_ipv6 != '' and prefix5_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу %s через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:fedf:34b7, резервного nexthop-a - fe80::aaf9:4bff:fe8b:9403" % (
            prefix5_ipv6, prefix5_prim_nexthop_ipv6, prefix5_backup_nexthop_ipv6))
        assert_that(
            prefix6_ipv6 == DUT4.loipv6 and prefix6_prim_nexthop_ipv6 != '' and prefix6_backup_nexthop_ipv6 != '',
            " Маршрут к префиксу 2004:0:10:1::4/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::205:8601:5f71:900, резервного nexthop-a - fe80::e2d9:e3ff:fedf:34b7" % (
            prefix6_prim_nexthop_ipv6, prefix6_backup_nexthop_ipv6))
    elif DUT.hostname == DUT3.hostname:
        assert_that(
            prefix1_ipv4 == DUT1.neighor3["ip_network"] and prefix1_prim_nexthop_ipv4 == DUT1.neighor1["ip"][0:-3] and prefix1_backup_nexthop_ipv4 == DUT2.neighor1["ip"][0:-3],
            " Маршрут к префиксу 192.168.55.8/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.1, резервного nexthop-a - 192.168.55.6" % (
            prefix1_prim_nexthop_ipv4, prefix1_backup_nexthop_ipv4))
        assert_that(
            prefix2_ipv4 == DUT2.neighor3["ip_network"] and prefix2_prim_nexthop_ipv4 == DUT2.neighor1["ip"][0:-3] and prefix2_backup_nexthop_ipv4 == DUT4.ip1,
            " Маршрут к префиксу 192.168.55.12/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.6, резервного nexthop-a - 192.168.55.18" % (
            prefix2_prim_nexthop_ipv4, prefix2_backup_nexthop_ipv4))
        assert_that(
            prefix3_ipv4 == DUT2.neighor2["ip_network"] and prefix3_prim_nexthop_ipv4 == DUT2.neighor1["ip"][0:-3] and prefix3_backup_nexthop_ipv4 == DUT1.neighor1["ip"][0:-3],
            " Маршрут к префиксу 192.168.55.20/30 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.6, резервного nexthop-a - 192.168.55.1" % (
            prefix3_prim_nexthop_ipv4, prefix3_backup_nexthop_ipv4))
        assert_that(
            prefix6_ipv4 == DUT2.loopback["ip"] and prefix6_prim_nexthop_ipv4 == DUT2.neighor1["ip"][0:-3] and prefix6_backup_nexthop_ipv4 == DUT1.neighor1["ip"][0:-3],
            " Маршрут к префиксу %s через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.6, резервного nexthop-a - 192.168.55.1" % (
            prefix6_ipv4, prefix6_prim_nexthop_ipv4, prefix6_backup_nexthop_ipv4))
        assert_that(
            prefix4_ipv4 == DUT1.loopback["ip"] and prefix4_prim_nexthop_ipv4 == DUT1.neighor1["ip"][0:-3] and prefix4_backup_nexthop_ipv4 == DUT2.neighor1["ip"][0:-3],
            " Маршрут к префиксу 1.0.0.3/32 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.1, резервного nexthop-a - 192.168.55.6" % (
            prefix4_prim_nexthop_ipv4, prefix4_backup_nexthop_ipv4))
        assert_that(
            prefix5_ipv4 == DUT4.loip and prefix5_prim_nexthop_ipv4 == DUT4.ip1 and prefix5_backup_nexthop_ipv4 == DUT2.neighor1["ip"][0:-3],
            " Маршрут к префиксу %s через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a -192.168.55.18, резервного nexthop-a - 192.168.55.6" % (
            prefix5_ipv4, prefix5_prim_nexthop_ipv4, prefix5_backup_nexthop_ipv4))

        assert_that(
            prefix1_ipv6 == DUT1.neighor2["ipv6_network"] and prefix1_prim_nexthop_ipv6 !=  '' and prefix1_backup_nexthop_ipv6 !=  '',
            " Маршрут к префиксу 2001:db8:cafe:a002::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:feff:48b2 , резервного nexthop-a - fe80::e2d9:e3ff:fedf:34b6" % (
            prefix1_prim_nexthop_ipv6, prefix1_backup_nexthop_ipv6))
        assert_that(
            prefix2_ipv6 == DUT2.neighor3["ipv6_network"] and prefix2_prim_nexthop_ipv6 !=  '' and prefix2_backup_nexthop_ipv6 !=  '',
            " Маршрут к префиксу 2001:db8:cafe:a012::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:feff:48b2, резервного nexthop-a - fe80::205:8601:5e71:900" % (
            prefix2_prim_nexthop_ipv6, prefix2_backup_nexthop_ipv6))
        assert_that(
            prefix3_ipv6 == DUT1.neighor3["ipv6_network"] and prefix3_prim_nexthop_ipv6 !=  '' and prefix3_backup_nexthop_ipv6 !=  '',
            " Маршрут к префиксу 2001:db8:cafe:a013::/64 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:fedf:34b6, резервного nexthop-a - fe80::e2d9:e3ff:feff:48b2" % (
            prefix3_prim_nexthop_ipv6, prefix3_backup_nexthop_ipv6))
        assert_that(
            prefix4_ipv6 == DUT2.loopback["ipv6"] and prefix4_prim_nexthop_ipv6 !=  '' and prefix4_backup_nexthop_ipv6 !=  '',
            " Маршрут к префиксу 2002:0:10:1::2/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:feff:48b2, резервного nexthop-a - fe80::e2d9:e3ff:fedf:34b6" % (
            prefix4_prim_nexthop_ipv6, prefix4_backup_nexthop_ipv6))
        assert_that(
            prefix5_ipv6 == DUT1.loopback["ipv6"] and prefix5_prim_nexthop_ipv6 !=  '' and prefix5_backup_nexthop_ipv6 !=  '',
            " Маршрут к префиксу 2003:0:10:1::3/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::e2d9:e3ff:fedf:34b6, резервного nexthop-a - fe80::e2d9:e3ff:feff:48b2" % (
            prefix5_prim_nexthop_ipv6, prefix5_backup_nexthop_ipv6))
        assert_that(
            prefix6_ipv6 == DUT4.loipv6 and prefix6_prim_nexthop_ipv6 !=  '' and prefix6_backup_nexthop_ipv6 !=  '',
            " Маршрут к префиксу 2004:0:10:1::4/128 через основной nexthop - %s и через резервный nexthop - %s не соответствует шаблону. Ожидаемые значения основного nexthop-a - fe80::205:8601:5e71:900, резервного nexthop-a - fe80::e2d9:e3ff:feff:48b2" % (
            prefix6_prim_nexthop_ipv6, prefix6_backup_nexthop_ipv6))
