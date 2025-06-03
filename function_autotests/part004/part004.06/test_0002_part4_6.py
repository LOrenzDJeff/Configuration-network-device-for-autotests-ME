from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        time.sleep(15)  # Ждем когда поднимутся LDP соседства
        conn.set_prompt('#')
        conn.execute('show mpls ldp neighbors')
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
@allure.feature('4.06:Функциональное тестирование MPLS LDP')
@allure.title('Проверка вывода команды show mpls ldp neighbor')
@pytest.mark.part4_6
@pytest.mark.show_mpls_ldp_neighbors
@pytest.mark.dependency(depends=["load_config046_dut1", "load_config046_dut2", "load_config046_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_mpls_ldp_neighbor_part4_6(DUT):
    # В данном тесте будем проверять вывод команды 'show mpls ldp neighbor' на соответствие шаблону из файла parse_show_mpls_ldp_neighbors.txt
    allure.attach.file('./network-schemes/part4_5_show_mpls_ldp_neighbors.png', 'Что анализируется в выводе команды',
                       attachment_type=allure.attachment_type.PNG)

    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show mpls ldp neighbors', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_mpls_ldp_neighbors.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp)
    # print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    assert len(result) == 2, f"Кол-во соседей в выводе должно быть равно 2, а не {len(result)}"

    neighbor1 = result[0]['neighbor']
    neighbor1_uptime = result[0]['uptime']
    neighbor1_expires = result[0]['expires']
    neighbor1_adjcs = result[0]['adjcs']
    neighbor1_addrs = result[0]['addrs']
    neighbor1_labels = result[0]['labels']
    neighbor1_GR_flag = result[0]['GR_flag']
    neighbor2_uptime = result[1]['uptime']
    neighbor2_expires = result[1]['expires']
    neighbor2_adjcs = result[1]['adjcs']
    neighbor2_addrs = result[1]['addrs']
    neighbor2_labels = result[1]['labels']
    neighbor2_GR_flag = result[1]['GR_flag']

    if (DUT.hostname == DUT1.hostname) and (neighbor1 == DUT2.loopback['ip_witout_mask']):
        assert_that(neighbor1_uptime != '', "Uptime LDP соседа 1.0.0.1 не соответствует шаблону")
        assert_that(int(neighbor1_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.1 больше 40 секунд и равен - %s" % neighbor1_expires)
        assert_that(int(neighbor1_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.1 отличается от ожидаемых 2 и равен - %s" % neighbor1_adjcs)
        assert_that(int(neighbor1_addrs) == 3,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.1 отличается от ожидаемых 3 и равно - %s" % neighbor1_addrs)
        assert_that(int(neighbor1_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.1 отличается от ожидаемых 2 и равно - %s" % neighbor1_labels)
        assert_that(neighbor1_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.1 отличается от ожидаемого N и равен - %s" % neighbor1_GR_flag)
        assert_that(neighbor2_uptime != '', "Uptime LDP соседа 1.0.0.2 не соответствует шаблону")
        assert_that(int(neighbor2_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.2 больше 40 секунд и равен - %s" % neighbor2_expires)
        assert_that(int(neighbor2_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.2 отличается от ожидаемых 2 и равен - %s" % neighbor2_adjcs)
        assert_that(int(neighbor2_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.2 отличается от ожидаемых 4 и равно - %s" % neighbor2_addrs)
        assert_that(int(neighbor2_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.2 отличается от ожидаемых 2 и равно - %s" % neighbor2_labels)
        assert_that(neighbor2_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.2 отличается от ожидаемого N и равен - %s" % neighbor2_GR_flag)

    elif (DUT.hostname == DUT1.hostname) and (neighbor1 == DUT3.loopback['ip_witout_mask']):
        assert_that(neighbor1_uptime != '', "Uptime LDP соседа 1.0.0.2 не соответствует шаблону")
        assert_that(int(neighbor1_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.2 больше 40 секунд и равен - %s" % neighbor1_expires)
        assert_that(int(neighbor1_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.1 отличается от ожидаемых 2 и равен - %s" % neighbor1_adjcs)
        assert_that(int(neighbor1_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.1 отличается от ожидаемых 4 и равно - %s" % neighbor1_addrs)
        assert_that(int(neighbor1_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.1 отличается от ожидаемых 2 и равно - %s" % neighbor1_labels)
        assert_that(neighbor1_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.1 отличается от ожидаемого N и равен - %s" % neighbor1_GR_flag)
        assert_that(neighbor2_uptime != '', "Uptime LDP соседа 1.0.0.1 не соответствует шаблону")
        assert_that(int(neighbor2_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.1 больше 40 секунд и равен - %s" % neighbor2_expires)
        assert_that(int(neighbor2_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.1 отличается от ожидаемых 2 и равен - %s" % neighbor2_adjcs)
        assert_that(int(neighbor2_addrs) == 3,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.1 отличается от ожидаемых 3 и равно - %s" % neighbor2_addrs)
        assert_that(int(neighbor2_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.1 отличается от ожидаемых 2 и равно - %s" % neighbor2_labels)
        assert_that(neighbor2_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.1 отличается от ожидаемого N и равен - %s" % neighbor2_GR_flag)

    elif (DUT.hostname == DUT2.hostname) and (neighbor1 == DUT1.loopback['ip_witout_mask']):
        assert_that(neighbor1_uptime != '', "Uptime LDP соседа 1.0.0.3 не соответствует шаблону")
        assert_that(int(neighbor1_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.3 больше 40 секунд и равен - %s" % neighbor1_expires)
        assert_that(int(neighbor1_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.3 отличается от ожидаемых 2 и равен - %s" % neighbor1_adjcs)
        assert_that(int(neighbor1_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.3 отличается от ожидаемых 4 и равно - %s" % neighbor1_addrs)
        assert_that(int(neighbor1_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.3 отличается от ожидаемых 2 и равно - %s" % neighbor1_labels)
        assert_that(neighbor1_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.3 отличается от ожидаемого N и равен - %s" % neighbor1_GR_flag)
        assert_that(neighbor2_uptime != '', "Uptime LDP соседа 1.0.0.1 не соответствует шаблону")
        assert_that(int(neighbor2_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.1 больше 40 секунд и равен - %s" % neighbor2_expires)
        assert_that(int(neighbor2_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.1 отличается от ожидаемых 2 и равен - %s" % neighbor2_adjcs)
        assert_that(int(neighbor2_addrs) == 3,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.1 отличается от ожидаемых 3 и равно - %s" % neighbor2_addrs)
        assert_that(int(neighbor2_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.1 отличается от ожидаемых 2 и равно - %s" % neighbor2_labels)
        assert_that(neighbor2_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.1 отличается от ожидаемого N и равен - %s" % neighbor2_GR_flag)

    elif (DUT.hostname == DUT2.hostname) and (neighbor1 == DUT3.loopback['ip_witout_mask']):
        assert_that(neighbor2_uptime != '', "Uptime LDP соседа 1.0.0.3 не соответствует шаблону")
        assert_that(int(neighbor2_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.3 больше 40 секунд и равен - %s" % neighbor2_expires)
        assert_that(int(neighbor2_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.3 отличается от ожидаемых 2 и равен - %s" % neighbor2_adjcs)
        assert_that(int(neighbor2_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.3 отличается от ожидаемых 4 и равно - %s" % neighbor2_addrs)
        assert_that(int(neighbor2_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.3 отличается от ожидаемых 2 и равно - %s" % neighbor2_labels)
        assert_that(neighbor2_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.3 отличается от ожидаемого N и равен - %s" % neighbor2_GR_flag)
        assert_that(neighbor1_uptime != '', "Uptime LDP соседа 1.0.0.1 не соответствует шаблону")
        assert_that(int(neighbor1_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.1 больше 40 секунд и равен - %s" % neighbor1_expires)
        assert_that(int(neighbor1_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.1 отличается от ожидаемых 2 и равен - %s" % neighbor1_adjcs)
        assert_that(int(neighbor1_addrs) == 3,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.1 отличается от ожидаемых 3 и равно - %s" % neighbor1_addrs)
        assert_that(int(neighbor1_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.1 отличается от ожидаемых 2 и равно - %s" % neighbor1_labels)
        assert_that(neighbor1_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.1 отличается от ожидаемого N и равен - %s" % neighbor1_GR_flag)

    elif (DUT.hostname == DUT3.hostname) and (neighbor1 == DUT2.loopback['ip_witout_mask']):
        assert_that(neighbor1_uptime != '', "Uptime LDP соседа 1.0.0.2 не соответствует шаблону")
        assert_that(int(neighbor1_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.2 больше 40 секунд и равен - %s" % neighbor1_expires)
        assert_that(int(neighbor1_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.2 отличается от ожидаемых 2 и равен - %s" % neighbor1_adjcs)
        assert_that(int(neighbor1_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.2 отличается от ожидаемых 4 и равно - %s" % neighbor1_addrs)
        assert_that(int(neighbor1_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.2 отличается от ожидаемых 2 и равно - %s" % neighbor1_labels)
        assert_that(neighbor1_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.2 отличается от ожидаемого N и равен - %s" % neighbor1_GR_flag)
        assert_that(neighbor2_uptime != '', "Uptime LDP соседа 1.0.0.3 не соответствует шаблону")
        assert_that(int(neighbor2_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.3 больше 40 секунд и равен - %s" % neighbor2_expires)
        assert_that(int(neighbor2_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.3 отличается от ожидаемых 2 и равен - %s" % neighbor2_adjcs)
        assert_that(int(neighbor2_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.3 отличается от ожидаемых 4 и равно - %s" % neighbor2_addrs)
        assert_that(int(neighbor2_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.3 отличается от ожидаемых 2 и равно - %s" % neighbor2_labels)
        assert_that(neighbor2_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.3 отличается от ожидаемого N и равен - %s" % neighbor2_GR_flag)

    elif (DUT.hostname == DUT3.hostname) and (neighbor1 == DUT1.loopback['ip_witout_mask']):
        assert_that(neighbor2_uptime != '', "Uptime LDP соседа 1.0.0.2 не соответствует шаблону")
        assert_that(int(neighbor2_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.2 больше 40 секунд и равен - %s" % neighbor2_expires)
        assert_that(int(neighbor2_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.2 отличается от ожидаемых 2 и равен - %s" % neighbor2_adjcs)
        assert_that(int(neighbor2_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.2 отличается от ожидаемых 4 и равно - %s" % neighbor2_addrs)
        assert_that(int(neighbor2_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.2 отличается от ожидаемых 2 и равно - %s" % neighbor2_labels)
        assert_that(neighbor2_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.2 отличается от ожидаемого N и равен - %s" % neighbor2_GR_flag)
        assert_that(neighbor1_uptime != '', "Uptime LDP соседа 1.0.0.3 не соответствует шаблону")
        assert_that(int(neighbor1_expires) <= 40,
                    "Таймер Expire для LDP соседа 1.0.0.3 больше 40 секунд и равен - %s" % neighbor1_expires)
        assert_that(int(neighbor1_adjcs) == 2,
                    "Кол-во adjacency образованных на LDP соседе 1.0.0.3 отличается от ожидаемых 2 и равен - %s" % neighbor1_adjcs)
        assert_that(int(neighbor1_addrs) == 4,
                    "Кол-во ip-адресов связанных с LDP соседом 1.0.0.3 отличается от ожидаемых 4 и равно - %s" % neighbor1_addrs)
        assert_that(int(neighbor1_labels) == 2,
                    "Кол-во mpls меток полученных от LDP соседа 1.0.0.3 отличается от ожидаемых 2 и равно - %s" % neighbor1_labels)
        assert_that(neighbor1_GR_flag == 'N',
                    "Флаг GR  для  LDP соседа 1.0.0.3 отличается от ожидаемого N и равен - %s" % neighbor1_GR_flag)
