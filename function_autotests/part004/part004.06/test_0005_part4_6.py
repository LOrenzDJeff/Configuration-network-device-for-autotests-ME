from conftest import *


def execute_command(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('show mpls ldp forwarding')
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
@allure.title('Проверка вывода команды show mpls ldp forwarding')
@pytest.mark.part4_6
@pytest.mark.show_mpls_ldp_forwarding
@pytest.mark.dependency(depends=["load_config046_dut1", "load_config046_dut2", "load_config046_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_mpls_ldp_forward_part4_6(DUT):
    # В данном тесте будем проверять вывод команды 'show mpls ldp forwarding' на соответсвие шаблону из файла parse_show_mpls_ldp_forwarding.txt
    resp = execute_command(DUT.host_ip, DUT.login, DUT.password)
    allure.attach(resp, 'Вывод команды show mpls ldp forwarding', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_mpls_ldp_forwarding.txt', 'r') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp)
    # print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    # Предполагается, что многомерный список result будет содержать как минимум 2 записи из таблицы 'mpls ldp forwarding'
    assert len(result) == 2, f"В выводе команды содержится меньше 2-ух записей, а именно {len(result)}"
    if DUT.hostname == DUT1.hostname:
        assert result[0]['prefix'] == DUT3.loopback['ip'], f"Префикс маршрута вместо 1.0.0.1/32 равен {result[0]['prefix']}"
        assert result[0]['label'] == 'ImpNull', f"Метка маршрута с префиксом 1.0.0.1/32 вместо ImpNull равна {result[0]['label']}"
        assert result[0]['out_int'] == DUT.neighor1['int_name'], \
            f"Исходящий интерфейс маршрута с префиксом 1.0.0.1/32 вместо bu1 равен {result[0]['out_int']}"
        assert result[0]['next_hop'] == DUT3.neighor1['ip'][0:-3], \
            f"Next Hop маршрута с префиксом 1.0.0.1/32 вместо 192.168.55.2 равен {result[0]['next_hop']}"

        assert result[1]['prefix'] == DUT2.loopback['ip'], f"Префикс маршрута вместо 1.0.0.2/32 равен {result[1]['prefix']}"
        assert result[1]['label'] == 'ImpNull', f"Метка маршрута с префиксом 1.0.0.2/32 вместо ImpNull равна {result[1]['label']}"
        assert result[1]['out_int'] == DUT.neighor2['int_name'], \
            f"Исходящий интерфейс маршрута с префиксом 1.0.0.2/32 вместо bu2 равен {result[1]['out_int']}"
        assert result[1]['next_hop'] == DUT2.neighor2['ip'][0:-3], \
            f"Next Hop маршрута с префиксом 1.0.0.2/32 вместо 192.168.55.22 равен {result[1]['next_hop']}"
    elif DUT.hostname == DUT2.hostname:
        assert result[0]['prefix'] == DUT3.loopback['ip'], f"Префикс маршрута вместо 1.0.0.1/32 равен {result[0]['prefix']}"
        assert result[0]['label'] == 'ImpNull', f"Метка маршрута с префиксом 1.0.0.1/32 вместо ImpNull равна {result[0]['label']}"
        assert result[0]['out_int'] == DUT.neighor1['int_name'], \
            f"Исходящий интерфейс маршрута с префиксом 1.0.0.1/32 вместо bu1 равен {result[0]['out_int']}"
        assert result[0]['next_hop'] == DUT3.neighor2['ip'][0:-3], \
            f"Next Hop маршрута с префиксом 1.0.0.1/32 вместо 192.168.55.5 равен {result[0]['next_hop']}"

        assert result[1]['prefix'] == DUT1.loopback['ip'], f"Префикс маршрута вместо 1.0.0.3/32 равен {result[1]['prefix']}"
        assert result[1]['label'] == 'ImpNull', f"Метка маршрута с префиксом 1.0.0.3/32 вместо ImpNull равна {result[1]['label']}"
        assert result[1]['out_int'] == DUT.neighor2['int_name'], \
            f"Исходящий интерфейс маршрута с префиксом 1.0.0.3/32 вместо bu2 равен {result[1]['out_int']}"
        assert result[1]['next_hop'] == DUT1.neighor2['ip'][0:-3], \
            f"Next Hop маршрута с префиксом 1.0.0.3/32 вместо 192.168.55.21 равен {result[1]['next_hop']}"
    elif DUT.hostname == DUT3.hostname:
        assert result[0]['prefix'] == DUT1.loopback['ip'], f"Префикс маршрута вместо 1.0.0.2/32 равен {result[0]['prefix']}"
        assert result[0]['label'] == 'ImpNull', f"Метка маршрута с префиксом 1.0.0.2/32 вместо ImpNull равна {result[0]['label']}"
        assert result[0]['out_int'] == DUT.neighor1['int_name'], \
            f"Исходящий интерфейс маршрута с префиксом 1.0.0.2/32 вместо bu2 равен {result[0]['out_int']}"
        assert result[0]['next_hop'] == DUT1.neighor1['ip'][0:-3], \
            f"Next Hop маршрута с префиксом 1.0.0.2/32 вместо 192.168.55.6 равен {result[0]['next_hop']}"

        assert result[1]['prefix'] == DUT2.loopback['ip'], f"Префикс маршрута вместо 1.0.0.3/32 равен {result[1]['prefix']}"
        assert result[1]['label'] == 'ImpNull', f"Метка маршрута с префиксом 1.0.0.3/32 вместо ImpNull равна {result[1]['label']}"
        assert result[1]['out_int'] == DUT.neighor2['int_name'], \
            f"Исходящий интерфейс маршрута с префиксом 1.0.0.3/32 вместо bu1 равен {result[1]['out_int']}"
        assert result[1]['next_hop'] == DUT2.neighor1['ip'][0:-3], \
            f"Next Hop маршрута с префиксом 1.0.0.3/32 вместо 192.168.55.1 равен {result[1]['next_hop']}"
