from conftest import *

@allure.feature('01:Подготовка основного стенда-квадрата')
@allure.story('1.2:Проверка связности и управления')
@allure.title('В данном тесте будем  проверять доступность маршрутизатора по протоколу SSH')
@pytest.mark.part1
@pytest.mark.login
@pytest.mark.dependency(depends=["load_config001_dut1","load_config001_dut2","load_config001_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3),
			]
			)

def test_ssh_login_part1(DUT):
    acc = Account(DUT.login, DUT.password)
    con = SSH2()
    con.connect(DUT.host_ip)
    con.set_prompt('#')
    con.login(acc)
    con.send('quit\r')
    con.close()
    time.sleep(1)
    if con.response == None:
        login_fail = False
    else:
        login_fail = True
    assert login_fail