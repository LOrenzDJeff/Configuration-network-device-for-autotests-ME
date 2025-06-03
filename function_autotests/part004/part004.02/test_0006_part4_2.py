from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('terminal datadump')
        conn.execute('show route')
        return conn.response
    except OSError as osE:
        pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
        conn.close()
    except Exception as e:
        pytest.fail(f"Error in execute_command: {e}")
    finally:
        if conn is not None:
            conn.send('quit\r')
            conn.close()


@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.02:Функциональное тестирование IS-IS')
@allure.title('Проверка вывода команды show route')
@pytest.mark.part4_2
@pytest.mark.show_route
@pytest.mark.dependency(
    depends=["load_config042_dut1", "load_config042_dut2", "load_config042_dut3"],
    scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_route_part4_2(DUT):
    # В данном тесте будем проверять вывод команды 'show route', а точнее парсить наличие отдельных ipv4 маршрутов
    # (1.0.0.1/32; 1.0.0.2/32; 1.0.0.3/32; 1.0.0.4/32) и ipv6 маршрутов (2001:0:10:1::1/128; 2002:0:10:1::2/128; 2003:0:10:1::3/128)
    # А так же общее кол-во маршрутов (26 для atAR1 и atDR1; 29 для atAR2)
    if DUT.hostname == DUT1.hostname or DUT.hostname == DUT3.hostname:
        route_count = "26"
    else:
        route_count = "29"

    allure.attach.file('./network-schemes/part4_show_route.png', 'Что анализируется в выводе команды',
                       attachment_type=allure.attachment_type.PNG)
    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show route', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_route(isis).txt') as template:
        fsm = textfsm.TextFSM(template)
    result = fsm.ParseTextToDicts(resp)
    # print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    assert len(result) > 0, "Парсинг команды show route вернул пустой результат"
    assert result[-1]['total_entries'] == route_count, f"Общее кол-во маршрутов равно не {route_count}, а {result[-1]['total_entries']}"

    values = []
    if DUT.host_ip == DUT1.host_ip:
        values = [
            {'prefix': DUT3.loopback["ip"], 'code': 'i L2', 'int': DUT.neighor1["int_name"], 'next_hop': DUT3.neighor1["ip"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT.loopback["ip"], 'code': 'L', 'int': 'lo10', 'next_hop': '', 'metric': ''},
            {'prefix': DUT4.loip, 'code': 'i L2', 'int': DUT.neighor3["int_name"], 'next_hop': DUT4.vlanip2[:-3], 'metric': '[116/10]'},
            {'prefix': DUT2.loopback["ip"], 'code': 'i L2', 'int': DUT.neighor2["int_name"], 'next_hop': DUT2.neighor2["ip"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT3.loopback["ipv6"], 'code': 'i L2', 'int': DUT.neighor1["int_name"], 'next_hop': DUT3.neighor1["ipv6"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT2.loopback["ipv6"], 'code': 'i L2', 'int': DUT.neighor2["int_name"], 'next_hop': DUT2.neighor2["ipv6"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT.loopback["ipv6"], 'code': 'L', 'int': 'lo10', 'next_hop': '', 'metric': ''}
        ]
    elif DUT.host_ip == DUT2.host_ip:
        values = [
            {'prefix': DUT3.loopback["ip"], 'code': 'i L2', 'int': DUT.neighor1["int_name"], 'next_hop': DUT3.neighor2["ip"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT1.loopback["ip"], 'code': 'i L2', 'int': DUT.neighor2["int_name"], 'next_hop': DUT1.neighor2["ip"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT4.loip, 'code': 'i L2', 'int': DUT.neighor3["int_name"], 'next_hop': DUT4.vlanip3[:-3], 'metric': '[116/10]'},
            {'prefix': DUT.loopback["ip"], 'code': 'L', 'int': 'lo10', 'next_hop': '', 'metric': ''},
            {'prefix': DUT3.loopback["ipv6"], 'code': 'i L2', 'int': DUT.neighor1["int_name"], 'next_hop': DUT3.neighor2["ipv6"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT.loopback["ipv6"], 'code': 'L', 'int': 'lo10', 'next_hop': '', 'metric': ''},
            {'prefix': DUT1.loopback["ipv6"], 'code': 'i L2', 'int': DUT.neighor2["int_name"], 'next_hop': DUT1.neighor2["ipv6"][:-3], 'metric': '[116/10]'}
        ]
    elif DUT.host_ip == DUT3.host_ip:
        values = [
            {'prefix': DUT.loopback["ip"], 'code': 'L', 'int': 'lo10', 'next_hop': '', 'metric': ''},
            {'prefix': DUT1.loopback["ip"], 'code': 'i L2', 'int': DUT.neighor1["int_name"], 'next_hop': DUT1.neighor1["ip"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT4.loip, 'code': 'i L2', 'int': DUT.neighor3["int_name"], 'next_hop': DUT4.vlanip1[:-3], 'metric': '[116/10]'},
            {'prefix': DUT2.loopback["ip"], 'code': 'i L2', 'int': DUT.neighor2["int_name"], 'next_hop': DUT2.neighor1["ip"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT.loopback["ipv6"], 'code': 'L', 'int': 'lo10', 'next_hop': '', 'metric': ''},
            {'prefix': DUT2.loopback["ipv6"], 'code': 'i L2', 'int': DUT.neighor2["int_name"], 'next_hop': DUT2.neighor1["ipv6"][:-3], 'metric': '[116/10]'},
            {'prefix': DUT1.loopback["ipv6"], 'code': 'i L2', 'int': DUT.neighor1["int_name"], 'next_hop': DUT1.neighor1["ipv6"][:-3], 'metric': '[116/10]'}
        ]
    for k in range(4):
        assert result[k]['prefix'] == values[k]['prefix'], \
            f"Префикс маршрута вместо {values[k]['prefix']} равен {result[k]['prefix']}"
        assert result[k]['codes'] == values[k]['code'], \
            f"Коды маршрута {result[k]['prefix']} вместо {values[k]['code']} равны {result[k]['codes']}"
        assert result[k]['next_hop'] == values[k]['next_hop'], \
            f"Next hop маршрута {result[k]['prefix']} вместо {values[k]['next_hop']} равен {result[k]['next_hop']}"
        assert result[k]['metric'] == values[k]['metric'], \
            f"Метрика маршрута {result[k]['prefix']} вместо [116/10] равна {result[k]['metric']}"
        assert result[k]['int'] == values[k]['int'], \
            f"Интерфейс маршрута {result[k]['prefix']} вместо {values[k]['int']} равен {result[k]['int']}"
    for k in range(4,7):
        assert result[k]['prefix'] == values[k]['prefix'], \
            f"Префикс маршрута вместо {values[k]['prefix']} равен {result[k]['prefix']}"
        assert result[k]['codes'] == values[k]['code'], \
            f"Коды маршрута {result[k]['prefix']} вместо {values[k]['code']} равны {result[k]['codes']}"
        assert result[k]['metric'] == values[k]['metric'], \
            f"Метрика маршрута {result[k]['prefix']} вместо [116/10] равна {result[k]['metric']}"
        assert result[k]['int'] == values[k]['int'], \
            f"Интерфейс маршрута {result[k]['prefix']} вместо {values[k]['int']} равен {result[k]['int']}"