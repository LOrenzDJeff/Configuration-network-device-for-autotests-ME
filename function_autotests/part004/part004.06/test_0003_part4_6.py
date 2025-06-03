from conftest import *


@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.06:Функциональное тестирование MPLS LDP')
@allure.title('Проверка вывода команды show mpls ldp binding local')
@pytest.mark.part4_6
@pytest.mark.show_mpls_ldp_bind_local
@pytest.mark.dependency(depends=["load_config046_dut1", "load_config046_dut2", "load_config046_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_mpls_ldp_bind_local_part4_6(DUT):
    # В данном тесте будем проверять вывод команды 'show mpls ldp bindings local' на соответствие шаблону из файла parse_show_mpls_ldp_bind_local.txt
    allure.attach.file('./network-schemes/part4_6_show_mpls_ldp_bind_local.png', 'Схема теста',
                       attachment_type=allure.attachment_type.PNG)
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    i = 0
    cmd_list = ['show route | include /32', 'show mpls ldp bindings local']
    for i in range(len(cmd_list)):
        conn.execute(cmd_list[i])
        resp = conn.response
        allure.attach(resp, 'Вывод команды %s' % cmd_list[i], attachment_type=allure.attachment_type.TEXT)
    conn.send('quit\r')
    conn.close()

    with open('./templates/parse_show_mpls_ldp_bind_local.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp)
    # print(result)  # Раскомментируй, если хочешь посмотреть результат парсинга

    # Предполагается что многомерный список result будет содержать как минимум 4 FEC-a
    assert_that(len(result) == 4,
                "В выводе команды %s общее кол-во записей не равно ожидаемым 4, а равно %d " % (
                    cmd_list[i], len(result)))

    FEC1 = result[0]['FEC']
    FEC1_neighbor_addr = result[0]['neighbor_addr']
    FEC1_neighbor_state = result[0]['neighbor_state']
    FEC1_type = result[0]['type']

    FEC2 = result[1]['FEC']
    FEC2_neighbor_addr = result[1]['neighbor_addr']
    FEC2_neighbor_state = result[1]['neighbor_state']
    FEC2_type = result[1]['type']

    FEC3 = result[2]['FEC']
    FEC3_neighbor_addr = result[2]['neighbor_addr']
    FEC3_neighbor_state = result[2]['neighbor_state']
    FEC3_type = result[2]['type']

    FEC4 = result[3]['FEC']
    FEC4_neighbor_addr = result[3]['neighbor_addr']
    FEC4_neighbor_state = result[3]['neighbor_state']
    FEC4_type = result[3]['type']

    if DUT.hostname == DUT1.hostname:
        assert_that(FEC1 == DUT3.loopback['ip'],
                    "Значение FEC1 на %s равно не ожидаемому 1.0.0.1/32, а %s" % (DUT1.hostname, FEC1))
        assert_that(FEC1_neighbor_addr == (DUT2.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC1 равно не ожидаемому 1.0.0.2:0, а %s" % (
                        DUT1.hostname, FEC1_neighbor_addr))
        assert_that(FEC1_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT1.hostname, FEC1, FEC1_neighbor_addr, FEC1_neighbor_state))
        assert_that(FEC1_type == 'prefix',
                    "Значение type на %s для FEC1 равно не ожидаемому prefix, а %s" % (DUT1.hostname, FEC1_type))

        assert_that(FEC2 == DUT.loopback['ip'],
                    "Значение FEC2 на %s равно не ожидаемому 1.0.0.2/32, а %s" % (DUT1.hostname, FEC2))
        assert_that(FEC2_neighbor_addr == (DUT3.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC2 равно не ожидаемому 1.0.0.1:0, а %s" % (
                        DUT1.hostname, FEC2_neighbor_addr))
        assert_that(FEC2_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT1.hostname, FEC2, FEC2_neighbor_addr, FEC2_neighbor_state))
        assert_that(FEC2_type == 'prefix', "Значение type на %s для FEC2 равно не ожидаемому значению prefix, а %s" % (
            DUT1.hostname, FEC2_type))

        assert_that(FEC3 == DUT.loopback['ip'],
                    "Значение FEC3 на %s равно не ожидаемому 1.0.0.3/32, а %s" % (DUT1.hostname, FEC3))
        assert_that(FEC3_neighbor_addr == (DUT2.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC3 равно не ожидаемому 1.0.0.1:0, а %s" % (
                        DUT1.hostname, FEC3_neighbor_addr))
        assert_that(FEC3_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT1.hostname, FEC3, FEC3_neighbor_addr, FEC3_neighbor_state))
        assert_that(FEC3_type == 'prefix', "Значение type на %s для FEC3 равно не ожидаемому значению prefix, а %s" % (
            DUT1.hostname, FEC3_type))

        assert_that(FEC4 == DUT2.loopback['ip'],
                    "Значение FEC4 на %s равно не ожидаемому 1.0.0.2/32, а %s" % (DUT1.hostname, FEC4))
        assert_that(FEC4_neighbor_addr == (DUT3.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC4 равно не ожидаемому 1.0.0.2:0, а %s" % (
                        DUT1.hostname, FEC4_neighbor_addr))
        assert_that(FEC4_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT1.hostname, FEC4, FEC4_neighbor_addr, FEC4_neighbor_state))
        assert_that(FEC4_type == 'prefix', "Значение type на %s для FEC4 равно не ожидаемому значению prefix, а %s" % (
            DUT1.hostname, FEC4_type))

    elif DUT.hostname == DUT2.hostname:
        assert_that(FEC1 == DUT3.loopback['ip'],
                    "Значение FEC1 на %s равно не ожидаемому 1.0.0.1/32, а %s" % (DUT2.hostname, FEC1))
        assert_that(FEC1_neighbor_addr == (DUT1.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC1 равно не ожидаемому 1.0.0.3:0, а %s" % (
                        DUT2.hostname, FEC1_neighbor_addr))
        assert_that(FEC1_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT2.hostname, FEC1, FEC1_neighbor_addr, FEC1_neighbor_state))
        assert_that(FEC1_type == 'prefix',
                    "Значение type на %s для FEC1 равно не ожидаемому prefix, а %s" % (DUT2.hostname, FEC1_type))

        assert_that(FEC2 == DUT1.loopback['ip'],
                    "Значение FEC2 на %s равно не ожидаемому 1.0.0.2/32, а %s" % (DUT2.hostname, FEC2))
        assert_that(FEC2_neighbor_addr == (DUT3.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC2 равно не ожидаемому 1.0.0.1:0, а %s" % (
                        DUT2.hostname, FEC2_neighbor_addr))
        assert_that(FEC2_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT2.hostname, FEC2, FEC2_neighbor_addr, FEC2_neighbor_state))
        assert_that(FEC2_type == 'prefix', "Значение type на %s для FEC2 равно не ожидаемому значению prefix, а %s" % (
            DUT2.hostname, FEC2_type))

        assert_that(FEC3 == DUT.loopback['ip'],
                    "Значение FEC3 на %s равно не ожидаемому 1.0.0.2/32, а %s" % (DUT2.hostname, FEC3))
        assert_that(FEC3_neighbor_addr == (DUT3.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC3 равно не ожидаемому 1.0.0.3:0, а %s" % (
                        DUT2.hostname, FEC3_neighbor_addr))
        assert_that(FEC3_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT2.hostname, FEC3, FEC3_neighbor_addr, FEC3_neighbor_state))
        assert_that(FEC3_type == 'prefix', "Значение type на %s для FEC3 равно не ожидаемому значению prefix, а %s" % (
            DUT2.hostname, FEC3_type))

        assert_that(FEC4 == DUT.loopback['ip'],
                    "Значение FEC4 на %s равно не ожидаемому 1.0.0.3/32, а %s" % (DUT2.hostname, FEC4))
        assert_that(FEC4_neighbor_addr == (DUT1.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC4 равно не ожидаемому 1.0.0.1:0, а %s" % (
                        DUT2.hostname, FEC4_neighbor_addr))
        assert_that(FEC4_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT2.hostname, FEC4, FEC4_neighbor_addr, FEC4_neighbor_state))
        assert_that(FEC4_type == 'prefix', "Значение type на %s для FEC4 равно не ожидаемому значению prefix, а %s" % (
            DUT2.hostname, FEC4_type))

    elif DUT.hostname == DUT3.hostname:
        assert_that(FEC1 == DUT.loopback['ip'],
                    "Значение FEC1 на %s равно не ожидаемому 1.0.0.1/32, а %s" % (DUT3.hostname, FEC1))
        assert_that(FEC1_neighbor_addr == (DUT1.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC1 равно не ожидаемому 1.0.0.2:0, а %s" % (
                        DUT3.hostname, FEC1_neighbor_addr))
        assert_that(FEC1_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT3.hostname, FEC1, FEC1_neighbor_addr, FEC1_neighbor_state))
        assert_that(FEC1_type == 'prefix',
                    "Значение type на %s для FEC1 равно не ожидаемому prefix, а %s" % (DUT3.hostname, FEC1_type))

        assert_that(FEC2 == DUT.loopback['ip'],
                    "Значение FEC2 на %s равно не ожидаемому 1.0.0.1/32, а %s" % (DUT3.hostname, FEC2))
        assert_that(FEC2_neighbor_addr == (DUT2.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC2 равно не ожидаемому 1.0.0.3:0, а %s" % (
                        DUT3.hostname, FEC2_neighbor_addr))
        assert_that(FEC2_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT3.hostname, FEC2, FEC2_neighbor_addr, FEC2_neighbor_state))
        assert_that(FEC2_type == 'prefix', "Значение type на %s для FEC2 равно не ожидаемому значению prefix, а %s" % (
            DUT3.hostname, FEC2_type))

        assert_that(FEC3 == DUT1.loopback['ip'],
                    "Значение FEC3 на %s равно не ожидаемому 1.0.0.2/32, а %s" % (DUT3.hostname, FEC3))
        assert_that(FEC3_neighbor_addr == (DUT2.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC3 равно не ожидаемому 1.0.0.3:0, а %s" % (
                        DUT3.hostname, FEC3_neighbor_addr))
        assert_that(FEC3_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT3.hostname, FEC3, FEC3_neighbor_addr, FEC3_neighbor_state))
        assert_that(FEC3_type == 'prefix', "Значение type на %s для FEC3 равно не ожидаемому значению prefix, а %s" % (
            DUT3.hostname, FEC3_type))

        assert_that(FEC4 == DUT2.loopback['ip'],
                    "Значение FEC4 на %s равно не ожидаемому 1.0.0.3/32, а %s" % (DUT3.hostname, FEC4))
        assert_that(FEC4_neighbor_addr == (DUT1.loopback['ip_witout_mask'] + ":0"),
                    "Значение Peer ID на %s для FEC4 равно не ожидаемому 1.0.0.2:0, а %s" % (
                        DUT3.hostname, FEC4_neighbor_addr))
        assert_that(FEC4_neighbor_state == 'mapping-established',
                    "Значение state на %s для FEC %s c Peer ID %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT3.hostname, FEC4, FEC4_neighbor_addr, FEC4_neighbor_state))
        assert_that(FEC4_type == 'prefix', "Значение type на %s для FEC4 равно не ожидаемому значению prefix, а %s" % (
            DUT3.hostname, FEC4_type))
