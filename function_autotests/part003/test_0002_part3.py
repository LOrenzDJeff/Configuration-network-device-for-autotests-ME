from conftest import *
from tabulate import tabulate


def parse_show_lldp(ip, login, password):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('terminal datadump')
        conn.execute("show lldp")
        resp = conn.response
        assert len(resp) > 0, 'Пустой вывод команды show lldp'
        allure.attach(resp, 'Вывод команды show lldp', attachment_type=allure.attachment_type.TEXT)
        with open('./templates/parse_show_lldp.txt') as template:
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseTextToDicts(resp)
        return result
    except Exception as e:
        print(f"Error parse_show_lldp: {e}")
        return None
    finally:
        if conn is not None:
            conn.send('logout\r')
            conn.close()


def check_global_info(info):
    # Получаем значение из словаря по ключу, затем сравниваем с ожидаемым
    print(info)
    current_value = info[0].get('ADVERT')
    assert current_value == '30', (f'Параметр LLDP advertisements не равен ожидаемому значению 30, '
                                   f'а равен - {current_value}')
    current_value = info[0].get('HOLD_TIME_ADVERT')
    assert current_value == '121', (f'Параметр LLDP hold time advertised не равен ожидаемому значению 121, '
                                    f'а равен - {current_value}')
    current_value = info[0].get('REINIT_DELAY')
    assert current_value == '2', (f'Параметр LLDP interface reinitialization delay не равен ожидаемому значению 2, '
                                  f'а равен - {current_value}')
    current_value = info[0].get('NOTIF_INT')
    assert current_value == '30', (f'Параметр LLDP notifications interval не равен ожидаемому значению 30, '
                                   f'а равен - {current_value}')


def check_ports_info(info, DUT):
    exist_port1 = exist_port2 = exist_port3 = exist_port4 = 0  # Переменные для проверки существования порта в словаре
    port1 = port2 = port3 = port4 = ''
    # Разные порты у устройств
    port1 = DUT.neighor2["interface"][0]
    port2 = DUT.neighor2["interface"][1]
    port3 = DUT.neighor1["interface"][0]
    port4 = DUT.neighor1["interface"][1]
    # В цикле обходим список словарей
    for row in info:
        # Проверяем соответствие значений, получая их по ключу
        assert row.get('STATE_TX') == 'enabled', (f'Параметр State TX у порта {row.get("PORT")} не равен ожидаемому '
                                                  f'значению enabled, а равен - {row.get("STATE_TX")}')
        assert row.get('STATE_RX') == 'enabled', (f'Параметр State RX у порта {row.get("PORT")} не равен ожидаемому '
                                                  f'значению enabled, а равен - {row.get("STATE_TX")}')
        assert row.get('OPTIONAL_TLVs') == 'MM PD SC SD SM', (f'Параметр Optional TLVs у порта {row.get("PORT")} '
                                                              f'не равен ожидаемому значению MM PD SC SD SM, а равен '
                                                              f'- {row.get("OPTIONAL_TLVs")}')
        assert row.get('NOTIFICATIONS_TABLES') == 'enabled', (f'Параметр Notifications tables у порта {row.get("PORT")}'
                                                              f' не равен ожидаемому значению enabled, а равен - '
                                                              f'{row.get("NOTIFICATIONS_TABLES")}')
        assert row.get('NOTIFICATIONS_DEVICE') == 'enabled', (f'Параметр Notifications device у порта {row.get("PORT")}'
                                                              f' не равен ожидаемому значению enabled, а равен - '
                                                              f'{row.get("NOTIFICATIONS_DEVICE")}')
        assert row.get('AGENT') == 'N', (f'Параметр Agent у порта {row.get("PORT")} не равен ожидаемому значению N, '
                                         f'а равен - {row.get("AGENT")}')
        # Проверяем наличие портов в выводе
        if port1 in row.values():
            exist_port1 = 1
        if port2 in row.values():
            exist_port2 = 1
        if port3 in row.values():
            exist_port3 = 1
        if port4 in row.values():
            exist_port4 = 1

    assert exist_port1 == 1, f'В выводе не обнаружен порт {port1}'
    assert exist_port2 == 1, f'В выводе не обнаружен порт {port2}'
    assert exist_port3 == 1, f'В выводе не обнаружен порт {port3}'
    assert exist_port4 == 1, f'В выводе не обнаружен порт {port4}'


@allure.feature('03:Функциональное тестирование протокола LLDP')
@allure.story('3.2:Проверка LLDP')
@allure.title('В данном тесте будем  проверять вывод команды show lldp')
@pytest.mark.part3
@pytest.mark.show_lldp
@pytest.mark.dependency(depends=["load_config003_dut1","load_config003_dut2","load_config003_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_lldp_part3(DUT):
    allure.attach.file('./network-schemes/part3_show_lldp.png', 'Что анализируется в выводе команды',
                       attachment_type=allure.attachment_type.PNG)
    # Эта функция подключается к устройству, выполняет команду, парсит результат и возвращает его
    result = parse_show_lldp(DUT.host_ip, DUT.login, DUT.password)
    assert result != 0, 'Парсинг команды вернул пустой результат'

    # Разделяем данные на глобальную информацию и информацию о портах
    global_info = [entry for entry in result if entry['PORT'] == '']
    ports_info = [entry for entry in result if entry['PORT'] != '']

    # Удаляем пустые ключи, чтобы корректно отобразить таблицы
    global_info_cleaned = [{key: value for key, value in item.items() if value} for item in global_info]
    ports_info_cleaned = [{key: value for key, value in item.items() if value} for item in ports_info]

    # Печать таблиц
    # print('\n', tabulate(global_info_cleaned, headers="keys", tablefmt="grid"))
    # print('\n', tabulate(ports_info_cleaned, headers="keys", tablefmt="grid"))

    # Проверяем глобальные параметры на соответствие ожидаемым значениям
    check_global_info(global_info_cleaned)
    # Если таблица с портами есть, то также проверяем на соответствие ожидаемым значениям
    if ports_info_cleaned:
        check_ports_info(ports_info_cleaned, DUT)
