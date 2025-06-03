from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('terminal datadump')
        conn.execute('show mpls ldp parameters')
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
@allure.title('Проверка вывода команды show mpls ldp parameters')
@pytest.mark.part4_6
@pytest.mark.show_mpls_ldp_param
@pytest.mark.dependency(depends=["load_config046_dut1", "load_config046_dut2", "load_config046_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_mpls_ldp_param_part4_6(DUT):
    # В данном тесте будем проверять вывод команды 'show mpls ldp parameters' на соответствие шаблону из файла parse_show_mpls_ldp_parameters.txt
    allure.attach.file('./network-schemes/part4_5_show_mpls_ldp_param.png', 'Что анализируется в выводе команды',
                       attachment_type=allure.attachment_type.PNG)
    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show mpls ldp parameters', attachment_type=allure.attachment_type.TEXT)

    # парсим 2 LDP соседа
    with open('./templates/parse_show_mpls_ldp_parameters_peers.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
    # print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    # Тестовый стенд предполагает, что в выводе команды 'show mpls ldp param' будет как минимум 2 соседа и 3 интерфейса с включенным LDP протоколом
    assert len(result) == 6, f"В выводе команды должно быть 2 соседа и 3 интерфейса с включенным LDP протоколом, а не {len(result) - 1}"

    rt_id = result[0][0]
    lsr_id = result[0][1]
    transport_addr = result[0][2]
    GR = result[0][3]
    GR_status = result[0][4]
    GR_timers = result[0][5]
    neighbors = result[1][6]
    peer1 = result[1][7]
    peer1_bfd = result[1][8]
    peer1_hold = result[1][9]
    peer1_hello = result[1][10]
    peer2 = result[2][7]
    peer2_bfd = result[2][8]
    peer2_hold = result[2][9]
    peer2_hello = result[2][10]

    with open('./templates/parse_show_mpls_ldp_parameters_int.txt') as template:  # парсим 3 LDP интерфейса
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
    # print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    int1_name = result[2][1]
    int1_bfd = result[2][2]
    int1_hold = result[2][3]
    int1_hello = result[2][4]
    int2_name = result[3][1]
    int2_bfd = result[3][2]
    int2_hold = result[3][3]
    int2_hello = result[3][4]
    int3_name = result[4][1]
    int3_bfd = result[4][2]
    int3_hold = result[4][3]
    int3_hello = result[4][4]

    assert_that(rt_id != '', "Параметр Router Id не соответствует шаблону  и равен %s" % rt_id)
    assert_that(transport_addr != '', "Параметр Transport address не соответствует шаблону и равен %s" % transport_addr)
    assert_that(GR != '', "Параметр GR не соответствует шаблону и равен %s" % GR)
    assert_that(GR_status != '', "Параметр GR_status не соответствует шаблону и равен %s" % GR_status)
    assert_that(GR_timers != '', "Параметр GR_timers не соответствует шаблону и равен %s" % GR_timers)
    assert_that(neighbors != '', "Параметр neighbors не соответствует шаблону и равен %s" % neighbors)
    assert_that(peer1 != '', "Параметр peer1 не соответствует шаблону и равен %s" % peer1)
    assert_that(peer1_bfd != '', "Параметр peer1_bfd не соответствует шаблону и равен %s" % peer1_bfd)
    assert_that(peer1_hold != '', "Параметр peer1_hold не соответствует шаблону и равен %s" % peer1_hold)
    assert_that(peer1_hello != '', "Параметр peer1_hello не соответствует шаблону и равен %s" % peer1_hello)
    assert_that(peer2 != '', "Параметр peer2 не соответствует шаблону и равен %s" % peer2)
    assert_that(peer2_bfd != '', "Параметр peer2_bfd не соответствует шаблону и равен %s" % peer2_bfd)
    assert_that(peer2_hold != '', "Параметр peer2_hold не соответствует шаблону и равен %s" % peer2_hold)
    assert_that(peer2_hello != '', "Параметр peer2_hello не соответствует шаблону и равен %s" % peer2_hello)

    assert_that(int1_name != '', "Параметр interface1 name не соответствует шаблону и равен %s" % int1_name)
    assert_that(int1_bfd != '', "Параметр interface1 bfd status не соответствует шаблону и равен %s" % int1_bfd)
    assert_that(int1_hold != '', "Параметр interface1 holdtime interval не соответствует шаблону и равен %s" % int1_hold)
    assert_that(int1_hello != '', "Параметр interface1 hello interval не соответствует шаблону и равен %s" % int1_hello)

    assert_that(int2_name != '', "Параметр interface2 name не соответствует шаблону и равен %s" % int2_name)
    assert_that(int2_bfd != '', "Параметр interface2 bfd status не соответствует шаблону и равен %s" % int2_bfd)
    assert_that(int2_hold != '', "Параметр interface2 holdtime interval не соответствует шаблону и равен %s" % int2_hold)
    assert_that(int2_hello != '', "Параметр interface2 hello interval не соответствует шаблону и равен %s" % int2_hello)

    assert_that(int3_name != '', "Параметр interface3 name не соответствует шаблону и равен %s" % int3_name)
    assert_that(int3_bfd != '', "Параметр interface3 bfd status не соответствует шаблону и равен %s" % int3_bfd)
    assert_that(int3_hold != '', "Параметр interface3 holdtime interval не соответствует шаблону и равен %s" % int3_hold)
    assert_that(int3_hello != '', "Параметр interface3 hello interval не соответствует шаблону и равен %s" % int3_hello)
