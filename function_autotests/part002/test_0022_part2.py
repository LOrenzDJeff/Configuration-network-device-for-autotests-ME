from conftest import *


def connect_DUT(ip, protocol, acc):
    protocol.set_timeout(60)
    conn = protocol
    try:
        conn.connect(ip)
        conn.login(acc)
        #print('Connect')
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
    except OSError as osE:
        pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
        conn.close()
    except Exception as e:
        pytest.fail(f"Error set_session_limit: {e}")
    finally:
        if conn is not None:
            conn.send('quit\r')
            conn.close()


def close_connections(connections):
    for conn in connections:
        if conn is not None:
            conn.send('quit\r')
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
    if DUT.hostname == DUT1.hostname or DUT.hostname == DUT2.hostname:
        flag = True
    if flag:
        acc = Account(DUT.login, DUT.password)
        conn = Telnet()
        try:
            conn.connect(DUT.host_ip)
            conn.login(acc)
            conn.execute('configure')
            conn.execute(f'telnet server vrf {DUT.vrf}')
            conn.execute('no session-limit')
            conn.execute('exit')
            conn.execute(f'ssh server vrf {DUT.vrf}')
            conn.execute('no session-limit')
            conn.send('commit\n')
            return conn
        except OSError as osE:
            pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
            conn.close()
        except Exception as e:
            pytest.fail(f"Error set_no_session_limit: {e}")
        finally:
            if conn is not None:
                conn.send('quit\r')
                conn.close()


@pytest.mark.part2
@pytest.mark.session_limit
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.010:Проверка session-limit для telnet/ssh, show processes memory и show process cpu')
@allure.title('В данном тесте проверяется session-limit для telnet/ssh')
@pytest.mark.dependency(depends=["load_config002_dut1", "load_config002_dut2", "load_config002_dut3"], scope='session')
@pytest.mark.parametrize("DUT, limits",
			[
			 pytest.param(DUT1,[1, 20]),
 			 pytest.param(DUT2,[1, 20]), 
 			 pytest.param(DUT3,[1, 20])
			]
			)
@pytest.mark.usefixtures('set_no_session_limit')
def test_session_limit_part2(DUT, limits):
    connections = []
    acc = Account(DUT.login, DUT.password)
    for limit in limits:
        try:
            connections = []
            conn = set_session_limit(DUT.host_ip, Telnet(), acc, DUT.vrf, limit, 'telnet')
            time.sleep(10)
            if conn is not None:
                for _ in range(limit + 1):
                    conn = connect_DUT(DUT.host_ip, Telnet(), acc)
                    if conn is not None:
                        connections.append(conn)
            conn_length = len(connections)
            assert conn_length == limit, \
                        f"Протокол telnet, получено {conn_length} успешных подключений при лимите = {limit}"
        finally:
            close_connections(connections)
        try:
            connections = []
            conn = set_session_limit(DUT.host_ip, Telnet(), acc, DUT.vrf, limit, 'ssh')
            time.sleep(10)
            if conn is not None:
                for _ in range(limit + 1):
                    conn = connect_DUT(DUT.host_ip, SSH2(), acc)
                    if conn is not None:
                        connections.append(conn)
            conn_length = len(connections)
            assert conn_length == limit, \
                        f"Протокол ssh, получено {conn_length} успешных подключений при лимите = {limit}"
        finally:
            close_connections(connections)
