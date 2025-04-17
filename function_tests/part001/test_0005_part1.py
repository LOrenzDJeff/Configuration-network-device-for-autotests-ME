from conftest import *


def execute_commands(ip, login, password, interfaces):
    acc = Account(login, password)
    conn = Telnet()
    try:
        conn.connect(ip)
        conn.login(acc)
        resp_list = []
        neighbors = []
        for inter in interfaces:
            neighbor = locate_ipv4_neighbor(conn, inter)
            neighbors.append(neighbor)
            conn.set_prompt('#')
            conn.execute(f'ping {neighbor} count 10')
            resp_list.append(conn.response)
        return neighbors, resp_list
    except OSError as osE:
        pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
        conn.close()
    except Exception as e:
        pytest.fail(f"Error in execute_command: {e}")
    finally:
        if conn is not None:
            conn.send('quit\r')
            conn.close()


@allure.feature('01:Подготовка основного стенда-квадрата')
@allure.story('1.2:Проверка связности и управления')
@allure.title('Проверка IP связности с P2P соседями маршрутизатора')
@pytest.mark.part1
@pytest.mark.neighbor_connect
@pytest.mark.dependency(
    depends=["load_config001_dut1", "load_config001_dut2", "load_config001_dut3", "load_config001_dut6"],
    scope='session')
@pytest.mark.parametrize('ip, int1, int2, int3, login, password',
                         [(DUT1['host_ip'], DUT1['int']["to_phys1"]["int_name"], DUT1['int']["to_phys2"]["int_name"], DUT1['int']["to_virt"]["int_name"], DUT1['login'], DUT1['password']),
                          (DUT2['host_ip'], DUT2['int']["to_phys1"]["int_name"], DUT2['int']["to_phys2"]["int_name"], DUT2['int']["to_virt"]["int_name"], DUT2['login'], DUT2['password']),
                          (DUT3['host_ip'], DUT3['int']["to_phys1"]["int_name"], DUT3['int']["to_phys2"]["int_name"], DUT3['int']["to_virt"]["int_name"], DUT3['login'], DUT3['password'])])
def test_ping_neighbors_part1(ip, int1, int2, int3, login, password):
    allure.attach.file('./network-schemes/part1_ping_neighbors.png', 'Схема теста',
                       attachment_type=allure.attachment_type.PNG)
    interfaces = [int1, int2, int3]
    neighbors, resp_list = execute_commands(ip, login, password, interfaces)

    for k in range(3):
        with open('./templates/parse_ping_from_me.txt', 'r') as template:
            fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp_list[k])
        allure.attach(resp_list[k], f'Вывод команды ping {neighbors[k]} count 10', attachment_type=allure.attachment_type.TEXT)
        assert int(result[0]['send_pkt']) > 8, \
            f"Нет связности с P2P соседом {neighbors[k]}, % успешности = {result[0]['success_rate']}"
