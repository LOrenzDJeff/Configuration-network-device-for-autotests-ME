from conftest import *


def execute_command(ip, login, password, interface):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        ipv4_neighbor = locate_neighbor(conn, 'ipv4', interface)
        ipv6_neighbor = locate_neighbor(conn, 'ipv6', interface)
        conn.execute('terminal datadump')
        conn.execute('config')
        conn.execute('router isis test')
        conn.execute('interface  %s' % interface)
        conn.execute('lfa exclude')
        conn.execute('commit')
        conn.execute('do show route isis')
        resp = conn.response
        conn.execute('no lfa exclude')
        conn.execute('commit')
        conn.execute('end')
        conn.send('quit\r')
        return resp, ipv4_neighbor, ipv6_neighbor
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
    'Выполнение команды lfa exclude на интерфейсе int1 и проверка вывода команды show route isis')
@pytest.mark.part4_4
@pytest.mark.lfa_exclude
@pytest.mark.dependency(depends=["load_config044_dut1","load_config044_dut2","load_config044_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_lfa_exclude_part4_4(DUT):
    # В данном тесте будем проверять вывод команды 'show route isis' после того как выполним команду lfa exclude в режиме конфигурации isis interface bu1
    # Ожидаем что маршруты у которых был backup через bu1 лишаться этого backup-а
    # Поскольку в выводе команды 'show route isis' в backup-e блоке не отображается резервный интерфейс, а только ip адрес соседа, то будем использовать функцию locate_neighbor(type,int) для определения
    # ip адреса соседа на P2P интерфейсе, а уже потом искать присутствие этого backup-ого адреса в выводе 'show route isis', если найдем значит тест не пройден
    allure.attach.file('./network-schemes/part4_2_show_route_isis_lfa_exclude_bu1.png',
                       'Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)
    resp, ipv4_neighbor, ipv6_neighbor = execute_command(DUT.host_ip, DUT.login, DUT.password, DUT.neighor1["int_name"])
    allure.attach(resp, 'Вывод команды show route isis при lfa exclude для bu1', attachment_type=allure.attachment_type.TEXT)

    allure.attach(ipv4_neighbor, 'ipv4 сосед на интерфейсе %s' % DUT.neighor1["int_name"])
    allure.attach(ipv6_neighbor, 'ipv6 сосед на интерфейсе %s' % DUT.neighor1["int_name"])

    # вместо поиска по шаблону воспользуемся простым поиском подстроки в выводе команды 'show route isis'
    test_ipv4_result = resp.find('backup local-lfa, address: %s)' % ipv4_neighbor)
    test_ipv6_result = resp.find('backup local-lfa, address: %s' % ipv6_neighbor)

    # Ожидаем что backup информации с ipv4_neighbor и ipv6_neighbor не обнаружено в выводе show route isis, иначе тест не пройден!
    assert test_ipv4_result == -1, \
        "Обнаружены маршруты которые содержат ipv4 адреса в блоке backup local-lfa, являющиеся next-hop-ами для bu1. Таких маршрутов быть не должно"
    assert test_ipv6_result == -1, \
        "Обнаружены маршруты которые содержат ipv6 адреса в блоке backup local-lfa, являющиеся next-hop-ами для bu1. Таких маршрутов быть не должно"
