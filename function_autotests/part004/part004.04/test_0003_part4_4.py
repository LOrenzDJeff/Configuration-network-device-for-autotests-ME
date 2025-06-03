from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('terminal datadump')
        conn.execute('show route isis')
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
@allure.title('Проверка вывода команды show route isis при включённом функционале LFA')
@pytest.mark.part4_4
@pytest.mark.check_route_isis
@pytest.mark.dependency(depends=["load_config044_dut1","load_config044_dut2","load_config044_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_route_isis_part4_4(DUT):
    # В данном тесте будем проверять вывод команды 'show route isis' точное кол-во различных типов маршрутов НЕ проверяется,
    # т.к. оно отличается у разных рутеров тестового стенда
    allure.attach.file('./network-schemes/part4_2_show_route_isis.png', 'Что анализируется в выводе команды',
                       attachment_type=allure.attachment_type.PNG)
    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show route isis', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_route_isis.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp)
    #    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    assert len(result) == 3, f'Кол-во маршрутов в результате парсинга должно быть равно 2, а не {len(result) - 1}'
    assert result[-1]['total_route'] == '12', f"Общее количество маршрутов вместо ожидаемых 12 равно {result[-1]['total_route']}"

    values = []
    if DUT.hostname == DUT1.hostname:
        values = [
            {'next_hop': DUT4.ip2, 'lfa_addr': DUT2.neighor2['ip'][0:-3], 'int': DUT.neighor3["int_name"]},
            {'next_hop': 'fe80::205:8601:6071:900', 'lfa_addr': 'fe80::e2d9:e3ff:feff:48b3', 'int': DUT.neighor3["int_name"]}
        ]
    elif DUT.hostname == DUT2.hostname:
        values = [
            {'next_hop': DUT4.ip3, 'lfa_addr': DUT1.neighor2['ip'][0:-3] , 'int': DUT.neighor3["int_name"]},
            {'next_hop': 'fe80::205:8601:5f71:900','lfa_addr': 'fe80::e65a:d4ff:fede:c8a3', 'int': DUT.neighor3["int_name"]}
        ]
    elif DUT.hostname == DUT3.hostname:
        values = [
            {'next_hop': DUT4.ip1, 'lfa_addr': DUT2.neighor1['ip'][0:-3], 'int': DUT.neighor3["int_name"]},
            {'next_hop': 'fe80::205:8601:5e71:900', 'lfa_addr': 'fe80::e2d9:e3ff:feff:48b2', 'int': DUT.neighor3["int_name"]}
        ]

    assert result[0]['next_hop'] == values[0]['next_hop'], \
        f"Next hop маршрута с префиксом 1.0.0.4/32 вместо {values[0]['next_hop']} равен {result[0]['next_hop']}"
    assert result[0]['LFA_addr'] == values[0]['lfa_addr'], \
        f"Адрес LFA маршрута с префиксом 1.0.0.4/32 вместо {values[0]['lfa_addr']} равен {result[0]['LFA_addr']}"
    assert result[0]['int'] == values[0]['int'], \
        f"Интерфейс маршрута с префиксом 1.0.0.4/32 вместо {values[0]['int']} равен {result[0]['int']}"

    assert result[1]['next_hop'] != values[1]['next_hop'], \
        f"Next hop маршрута с префиксом 2004:0:10:1::4/128 вместо {values[1]['next_hop']} равен {result[1]['next_hop']}"
    assert result[1]['LFA_addr'] != values[1]['lfa_addr'], \
        f"Адрес LFA маршрута с префиксом 2004:0:10:1::4/128 вместо {values[1]['lfa_addr']} равен {result[1]['LFA_addr']}"
    assert result[1]['int'] == values[1]['int'], \
        f"Интерфейс маршрута с префиксом 2004:0:10:1::4/128 вместо {values[1]['int']} равен {result[1]['int']}"
