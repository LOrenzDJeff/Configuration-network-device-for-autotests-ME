from conftest import *


@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.06:Функциональное тестирование MPLS LDP')
@allure.title('Проверка вывода команды show mpls ldp binding remote')
@pytest.mark.part4_6
@pytest.mark.show_mpls_ldp_bind_remote
@pytest.mark.dependency(depends=["load_config046_dut1", "load_config046_dut2", "load_config046_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_mpls_ldp_bind_remote_part4_6(DUT):
    # В данном тесте будем проверять вывод команды 'show mpls ldp bindings remote' на соответствие шаблону из файла parse_show_mpls_ldp_bind_remote.txt
    allure.attach.file('./network-schemes/part4_6_show_mpls_ldp_bind_remote.png', 'Схема теста',
                       attachment_type=allure.attachment_type.PNG)
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    cmd_list = ['show route | include /32', 'show mpls ldp bindings remote']
    for i in range(len(cmd_list)):
        conn.execute(cmd_list[i])
        resp = conn.response
        allure.attach(resp, 'Вывод команды %s' % cmd_list[i], attachment_type=allure.attachment_type.TEXT)
    conn.send('quit\r')
    conn.close()

    with open('./templates/parse_show_mpls_ldp_bind_remote.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp)
    # print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    # Предполагается, что многомерный список result будет содержать как минимум 4 FEC-a (считаем, что 4 FEC-а ровно)
    assert_that((len(result) == 4) or (len(result) == 5) or (len(result) == 6),
                "В выводе команды %s общее кол-во записей равно не ожидаемым 4/5/6, а равно %s" % (
                    cmd_list[1], len(result)))

    if DUT.hostname == DUT1.hostname:
        loc_index = 0
        located_index = locate2_index_in_ListOfDict(result, 'FEC', DUT3.loopback['ip'], 'neighbor_addr', (DUT3.loopback['ip_witout_mask'] + ":0"),
                                                    loc_index)
        assert_that(located_index != 999,
                    "В выводе команды %s не обнаружено метки с Prefix равным 1.0.0.1/32 и Peer ID равным 1.0.0.1:0" %
                    cmd_list[1])
        located_index1 = locate2_index_in_ListOfDict(result, 'FEC', DUT2.loopback['ip'], 'neighbor_addr', (DUT2.loopback['ip_witout_mask'] + ":0"),
                                                     loc_index)
        assert_that(located_index1 != 999,
                    "В выводе команды %s не обнаружено метки с Prefix равным 1.0.0.2/32 и Peer ID равным 1.0.0.2:0" %
                    cmd_list[1])

        FEC1 = result[located_index]['FEC']
        FEC1_neighbor_addr = result[located_index]['neighbor_addr']
        FEC1_label = result[located_index]['label']
        FEC1_neighbor_state = result[located_index]['neighbor_state']
        FEC1_type = result[located_index]['type']
        FEC1_interface = result[located_index]['interface']

        FEC2 = result[located_index1]['FEC']
        FEC2_neighbor_addr = result[located_index1]['neighbor_addr']
        FEC2_label = result[located_index1]['label']
        FEC2_neighbor_state = result[located_index1]['neighbor_state']
        FEC2_type = result[located_index1]['type']
        FEC2_interface = result[located_index1]['interface']

        # assert_that(FEC1 == DUT3.loopback['ip'], "Значение FEC1 на %s равно не ожидаемому 1.0.0.1/32, а %s" %(DUT1.hostname, FEC1))
        # assert_that(FEC1_neighbor_addr == (DUT3.loopback['ip_witout_mask'] + ":0"), "Значение Peer ID на %s для FEC1 равно не ожидаемому 1.0.0.1:0, а %s" %(DUT1.hostname, FEC1_neighbor_addr))
        assert_that(FEC1_label == '3', "Значение label на %s для метки с Prefix %s равно не ожидаемому 3, а %s" % (
            DUT1.hostname, FEC1, FEC1_label))
        assert_that(FEC1_neighbor_state == 'mapping-established',
                    "Значение state на %s для метки с Prefix %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT1.hostname, FEC1, FEC1_neighbor_state))
        assert_that(FEC1_type == 'prefix',
                    "Значение type на %s для метки с Prefix %s равно не ожидаемому prefix, а %s" % (
                        DUT1.hostname, FEC1, FEC1_type))
        assert_that(FEC1_interface == DUT1.neighor1['full_int_name'],
                    "Значение interface на %s для метки с Prefix %s равно не ожидаемому значению bu1, а %s" % (
                        DUT1.hostname, FEC1, FEC1_interface))

        # assert_that(FEC2 == DUT2.loopback['ip'], "Значение FEC2 на %s равно не ожидаемому 1.0.0.2/32, а %s" %(DUT1.hostname, FEC2))
        # assert_that(FEC2_neighbor_addr == (DUT2.loopback['ip_witout_mask'] + ":0"), "Значение Peer ID на %s для FEC2 равно не ожидаемому 1.0.0.2:0, а %s" %(DUT1.hostname, FEC2_neighbor_addr))
        assert_that(FEC2_label == '3', "Значение label на %s для метки с Prefix %s равно не ожидаемому 3, а %s" % (
            DUT1.hostname, FEC2, FEC2_label))
        assert_that(FEC2_neighbor_state == 'mapping-established',
                    "Значение state на %s для для метки с Prefix %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT1.hostname, FEC2, FEC2_neighbor_state))
        assert_that(FEC2_type == 'prefix',
                    "Значение type на %s для метки с Prefix %s равно не ожидаемому значению prefix, а %s" % (
                        DUT1.hostname, FEC2, FEC2_type))
        assert_that(FEC2_interface == DUT1.neighor2['full_int_name'],
                    "Значение interface на %s для метки с Prefix %s равно не ожидаемому значению bu2, а %s" % (
                        DUT1.hostname, FEC2, FEC2_interface))

    if DUT.hostname == DUT2.hostname:
        loc_index = 0
        located_index = locate2_index_in_ListOfDict(result, 'FEC', DUT3.loopback['ip'], 'neighbor_addr', (DUT3.loopback['ip_witout_mask'] + ":0"),
                                                    loc_index)
        assert_that(located_index != 999,
                    "В выводе команды %s не обнаружено метки с Prefix равным 1.0.0.1/32 и Peer ID равным 1.0.0.1:0" %
                    cmd_list[1])
        located_index1 = locate2_index_in_ListOfDict(result, 'FEC', DUT1.loopback['ip'], 'neighbor_addr', (DUT1.loopback['ip_witout_mask'] + ":0"),
                                                     loc_index)
        assert_that(located_index1 != 999,
                    "В выводе команды %s не обнаружено метки с Prefix равным 1.0.0.3/32 и Peer ID равным 1.0.0.3:0" %
                    cmd_list[1])

        FEC1 = result[located_index]['FEC']
        FEC1_neighbor_addr = result[located_index]['neighbor_addr']
        FEC1_label = result[located_index]['label']
        FEC1_neighbor_state = result[located_index]['neighbor_state']
        FEC1_type = result[located_index]['type']
        FEC1_interface = result[located_index]['interface']

        FEC2 = result[located_index1]['FEC']
        FEC2_neighbor_addr = result[located_index1]['neighbor_addr']
        FEC2_label = result[located_index1]['label']
        FEC2_neighbor_state = result[located_index1]['neighbor_state']
        FEC2_type = result[located_index1]['type']
        FEC2_interface = result[located_index1]['interface']

        # assert_that(FEC1 == DUT3.loopback['ip'], "Значение FEC1 на %s равно не ожидаемому 1.0.0.1/32, а %s" %(DUT2.hostname, FEC1))
        # assert_that(FEC1_neighbor_addr == (DUT3.loopback['ip_witout_mask'] + ":0"), "Значение Peer ID на %s для FEC1 равно не ожидаемому 1.0.0.1:0, а %s" %(DUT2.hostname, FEC1_neighbor_addr))
        assert_that(FEC1_label == '3', "Значение label на %s для метки с Prefix %s равно не ожидаемому 3, а %s" % (
            DUT2.hostname, FEC1, FEC1_label))
        assert_that(FEC1_neighbor_state == 'mapping-established',
                    "Значение state на %s для метки с Prefix %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT2.hostname, FEC1, FEC1_neighbor_state))
        assert_that(FEC1_type == 'prefix',
                    "Значение type на %s для метки с Prefix %s равно не ожидаемому prefix, а %s" % (
                        DUT2.hostname, FEC1, FEC1_type))
        assert_that(FEC1_interface == DUT1.neighor1['full_int_name'],
                    "Значение interface на %s для метки с Prefix %s равно не ожидаемому значению bu1, а %s" % (
                        DUT2.hostname, FEC1, FEC1_interface))

        # assert_that(FEC2 == DUT1.loopback['ip'], "Значение FEC2 на %s равно не ожидаемому 1.0.0.3/32, а %s" %(DUT2.hostname, FEC2))
        # assert_that(FEC2_neighbor_addr == (DUT1.loopback['ip_witout_mask'] + ":0"), "Значение Peer ID на %s для FEC2 равно не ожидаемому 1.0.0.3:0, а %s" %(DUT2.hostname, FEC2_neighbor_addr))
        assert_that(FEC2_label == '3', "Значение label на %s для метки с Prefix %s равно не ожидаемому 3, а %s" % (
            DUT2.hostname, FEC2, FEC2_label))
        assert_that(FEC2_neighbor_state == 'mapping-established',
                    "Значение state на %s для метки с Prefix %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT2.hostname, FEC2, FEC2_neighbor_state))
        assert_that(FEC2_type == 'prefix',
                    "Значение type на %s для метки с Prefix %s равно не ожидаемому значению prefix, а %s" % (
                        DUT2.hostname, FEC2, FEC2_type))
        assert_that(FEC2_interface == DUT1.neighor2['full_int_name'],
                    "Значение interface на %s для метки с Prefix %s равно не ожидаемому значению bu2, а %s" % (
                        DUT2.hostname, FEC2, FEC2_interface))

    if DUT.hostname == DUT3.hostname:
        loc_index = 0
        located_index = locate2_index_in_ListOfDict(result, 'FEC', DUT2.loopback['ip'], 'neighbor_addr', (DUT2.loopback['ip_witout_mask'] + ":0"),
                                                    loc_index)
        assert_that(located_index != 999,
                    "В выводе команды %s не обнаружено метки с Prefix равным 1.0.0.2/32 и Peer ID равным 1.0.0.2:0" %
                    cmd_list[1])
        located_index1 = locate2_index_in_ListOfDict(result, 'FEC', DUT1.loopback['ip'], 'neighbor_addr', (DUT1.loopback['ip_witout_mask'] + ":0"),
                                                     loc_index)
        assert_that(located_index1 != 999,
                    "В выводе команды %s не обнаружено метки с Prefix равным 1.0.0.3/32 и Peer ID равным 1.0.0.3:0" %
                    cmd_list[1])

        FEC1 = result[located_index]['FEC']
        FEC1_neighbor_addr = result[located_index]['neighbor_addr']
        FEC1_label = result[located_index]['label']
        FEC1_neighbor_state = result[located_index]['neighbor_state']
        FEC1_type = result[located_index]['type']
        FEC1_interface = result[located_index]['interface']

        FEC2 = result[located_index1]['FEC']
        FEC2_neighbor_addr = result[located_index1]['neighbor_addr']
        FEC2_label = result[located_index1]['label']
        FEC2_neighbor_state = result[located_index1]['neighbor_state']
        FEC2_type = result[located_index1]['type']
        FEC2_interface = result[located_index1]['interface']

        # assert_that(FEC1 == DUT2.loopback['ip'], "Значение FEC1 на %s равно не ожидаемому 1.0.0.2/32, а %s" %(DUT3.hostname, FEC1))
        # assert_that(FEC1_neighbor_addr == (DUT2.loopback['ip_witout_mask'] + ":0"), "Значение Peer ID на %s для FEC1 равно не ожидаемому 1.0.0.2:0, а %s" %(DUT3.hostname, FEC1_neighbor_addr))
        assert_that(FEC1_label == '3', "Значение label на %s для метки с Prefix %s равно не ожидаемому 3, а %s" % (
            DUT3.hostname, FEC1, FEC1_label))
        assert_that(FEC1_neighbor_state == 'mapping-established',
                    "Значение state на %s для метки с Prefix %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT3.hostname, FEC1, FEC1_neighbor_state))
        assert_that(FEC1_type == 'prefix',
                    "Значение type на %s для метки с Prefix %s равно не ожидаемому prefix, а %s" % (
                        DUT3.hostname, FEC1, FEC1_type))
        assert_that(FEC1_interface == DUT1.neighor2['full_int_name'],
                    "Значение interface на %s для метки с Prefix %s равно не ожидаемому значению bu2, а %s" % (
                        DUT3.hostname, FEC1, FEC1_interface))

        # assert_that(FEC2 == DUT1.loopback['ip'], "Значение FEC2 на %s равно не ожидаемому 1.0.0.3/32, а %s" %(DUT3.hostname, FEC2))
        # assert_that(FEC2_neighbor_addr == (DUT1.loopback['ip_witout_mask'] + ":0"), "Значение Peer ID на %s для FEC2 равно не ожидаемому 1.0.0.3:0, а %s" %(DUT3.hostname, FEC2_neighbor_addr))
        assert_that(FEC2_label == '3', "Значение label на %s для метки с Prefix %s равно не ожидаемому 3, а %s" % (
            DUT3.hostname, FEC2, FEC2_label))
        assert_that(FEC2_neighbor_state == 'mapping-established',
                    "Значение state на %s для метки с Prefix %s равно не ожидаемому значению mapping-established, а %s" % (
                        DUT3.hostname, FEC2, FEC2_neighbor_state))
        assert_that(FEC2_type == 'prefix',
                    "Значение type на %s для метки с Prefix %s равно не ожидаемому значению prefix, а %s" % (
                        DUT3.hostname, FEC2, FEC2_type))
        assert_that(FEC2_interface == DUT1.neighor1['full_int_name'],
                    "Значение interface на %s для метки с Prefix %s равно не ожидаемому значению bu1, а %s" % (
                        DUT3.hostname, FEC2, FEC2_interface))
