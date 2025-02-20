from conftest import *

def locate_ipv4_neighbor(conn,interface):
    conn.execute('terminal datadump')
    conn.execute('show interface %s'%interface)
    resp = conn.response
    template = open('./templates/parse_show_interface.txt')
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
    ipv4_int_addr=processed_result[0]['ipv4_addr']
    int1 = ipaddress.ip_interface(ipv4_int_addr)
    subnet=ipaddress.ip_network(int1.network)
    if subnet[1] == int1.ip:
        return(subnet[2])
    else :
        return(subnet[1])

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
@allure.title('В данном тесте будем  проверять IP связность с P2P соседями маршрутизатора')
@pytest.mark.part1
@pytest.mark.neighbor_connect
@pytest.mark.dependency(depends=["load_config001_dut1","load_config001_dut2","load_config001_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3),
			]
			)

def test_ping_neighbors_part1(DUT):
    allure.attach.file('./network-schemes/part1_ping_neighbors.png', 'Схема теста',
                       attachment_type=allure.attachment_type.PNG)
    interfaces = [DUT.neighor1["int_name"], DUT.neighor2["int_name"], DUT.neighor3["int_name"]]
    neighbors, resp_list = execute_commands(DUT.host_ip, DUT.login, DUT.password, interfaces)

    for k in range(3):
        with open('./templates/parse_ping_from_me.txt', 'r') as template:
            fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(resp_list[k])
        allure.attach(resp_list[k], f'Вывод команды ping {neighbors[k]} count 10', attachment_type=allure.attachment_type.TEXT)
        assert int(result[0]['send_pkt']) > 8, \
            f"Нет связности с P2P соседом {neighbors[k]}, % успешности = {result[0]['success_rate']}"
