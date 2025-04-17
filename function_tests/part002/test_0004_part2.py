from conftest import *


def execute_command(ip, login, password):
    conn = Telnet()
    acc = Account(login, password)
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('show ntp associations')
        return conn.response
    except Exception as e:
        pytest.fail(f"Error in execute_command: {e}")
    finally:
        if conn is not None:
            conn.close()


@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.004:Проверка времени и NTP')
@allure.title('Проверка вывода команды show ntp associations')
@pytest.mark.part2
@pytest.mark.ntp
@pytest.mark.dependency(depends=["load_config002_dut1", "load_config002_dut2", "load_config002_dut3"], scope='session')
@pytest.mark.parametrize('ip, login, password', [(DUT1['host_ip'], DUT1['login'], DUT1['password']),
                                                 (DUT2['host_ip'], DUT2['login'], DUT2['password']),
                                                 (DUT3['host_ip'], DUT3['login'], DUT3['password'])])
def test_ntp_part2(ip, login, password):
    resp = execute_command(ip, login, password)
    allure.attach(resp, 'Вывод команды show ntp associations', attachment_type=allure.attachment_type.TEXT)

    # Символ '*' нужно добавить перед ip адресом сервера т.к. он указывает на факт синхронизации
    number = resp.find('*%s' % ntp_server_ip)
    assert number != -1, \
        "В выводе команды show ntp associations не обнаружен символ '*', нет синхронизации с одноранговым узлом"
