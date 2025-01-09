from conftest import *


def connect_router(ip, protocol, acc):
    protocol.set_timeout(60)
    conn = protocol
    try:
        conn.connect(ip)
        conn.login(acc)
        print('Connect')
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None


def set_session_limit(ip, protocol, acc, vrf, limit, proto):
    protocol.set_timeout(60)
    conn = protocol
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.execute('configure')
        conn.execute(f'{proto} server vrf {vrf} session-limit {limit}')
        conn.send('commit\n')
        return conn
    except Exception as e:
        print(f"Error set_session_limit: {e}")
        return None
    finally:
        if conn is not None:
            conn.send('logout\n')
            conn.close()


def close_connections(connections):
    for conn in connections:
        if conn is not None:
            conn.send('logout\n')
            conn.close()


# def check_active_sessions(connections):
#     for conn in connections:
#         if conn is not None:
#             conn.execute('show users')
#             print(conn.response)

@pytest.fixture()
def set_no_session_limit(DUT):
    yield
    flag = False
    router = setting_ME(DUT)
    with open('config_OOP.json', 'r', encoding='utf-8') as file:
        check = json.load(file)
    if router.hostname == check['DUT1']['hostname'] or router.hostname == check['DUT2']['hostname']:
        flag = True
    if flag:
        acc = Account(router.login, router.password)
        conn = Telnet()
        try:
            conn.connect(router.host_ip)
            conn.login(acc)
            conn.execute('configure')
            conn.execute(f'telnet server vrf {router.vrf}')
            conn.execute('no session-limit')
            conn.execute('exit')
            conn.execute(f'ssh server vrf {router.vrf}')
            conn.execute('no session-limit')
            conn.send('commit\n')
            return conn
        except Exception as e:
            print(f"Error set_no_session_limit: {e}")
            return None
        finally:
            if conn is not None:
                conn.send('logout\n')
                conn.close()


@pytest.mark.part2
@pytest.mark.session_limit
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.010:Проверка session-limit для telnet/ssh, show processes memory и show process cpu')
@allure.title('В данном тесте проверяется session-limit для telnet/ssh')
@pytest.mark.dependency(depends=["load_config002_dut1", "load_config002_dut2", "load_config002_dut3"], scope='session')
@pytest.mark.parametrize("DUT, limits",
			[
			 pytest.param("DUT1",[1, 20]),
 			 pytest.param("DUT2",[1, 20]), 
 			 pytest.param("DUT3",[10])
			]
			)
@pytest.mark.usefixtures('set_no_session_limit')
def test_session_limit_part2(DUT, limits):
    with open('./tests_descriptions/part002/test0022_procedure.txt', 'rb') as desc:
        allure.attach(desc.read(), name='Описание теста', attachment_type=allure.attachment_type.TEXT)
    connections = []
    router = setting_ME(DUT)
    acc = Account(router.login, router.password)
    for limit in limits:
        try:
            connections = []
            conn = set_session_limit(router.host_ip, Telnet(), acc, router.vrf, limit, 'telnet')
            time.sleep(10)
            if conn is not None:
                for _ in range(limit + 1):
                    conn = connect_router(router.host_ip, Telnet(), acc)
                    if conn is not None:
                        connections.append(conn)
            conn_length = len(connections)
            assert conn_length == limit, \
                        f"Протокол telnet, получено {conn_length} успешных подключений при лимите = {limit}"
        finally:
            close_connections(connections)
        try:
            connections = []
            conn = set_session_limit(router.host_ip, Telnet(), acc, router.vrf, limit, 'ssh')
            time.sleep(10)
            if conn is not None:
                for _ in range(limit + 1):
                    conn = connect_router(router.host_ip, SSH2(), acc)
                    if conn is not None:
                        connections.append(conn)
            conn_length = len(connections)
            assert conn_length == limit, \
                        f"Протокол ssh, получено {conn_length} успешных подключений при лимите = {limit}"
        finally:
            close_connections(connections)
