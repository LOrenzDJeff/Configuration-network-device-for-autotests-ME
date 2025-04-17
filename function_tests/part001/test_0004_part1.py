from conftest import *

@allure.feature('01:Подготовка основного стенда-квадрата')
@allure.story('1.2:Проверка связности и управления')
@allure.title('Проверка доступности маршрутизатора по протоколу SSH')
@pytest.mark.part1
@pytest.mark.login
@pytest.mark.dependency(depends=["load_config001_dut1","load_config001_dut2","load_config001_dut3","load_config001_dut6"],scope='session')
@pytest.mark.parametrize('ip , login , password', [(DUT1['host_ip'] , DUT1['login'] , DUT1['password']) , (DUT2['host_ip'] , DUT2['login'] , DUT2['password']) , (DUT3['host_ip'] , DUT3['login'] , DUT3['password'])])
def test_ssh_login_part1(ip, login, password):
    """Проверяем доступность по ssh2"""
    acc = Account(login, password)
    conn = SSH2()
    conn.connect(ip)
    conn.login(acc)
    conn.send('quit\r')
    conn.close()
    time.sleep(1)  # Добавил задержку в рамках решения пробелмы http://red.eltex.loc/issues/208028
    if conn.response == None:
        login_fail = True
    else:
        login_fail = False
    assert login_fail == False

