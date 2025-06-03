from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.004:Проверка времени и NTP')
@allure.title('В данном тесте будем проверять вывод команды show ntp associations')
@pytest.mark.part2
@pytest.mark.ntp
@pytest.mark.dependency(depends=["load_config002_dut1", "load_config002_dut2", "load_config002_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_ntp_part2(DUT):
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    try:
        conn.connect(DUT.host_ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('show ntp associations')
        resp = conn.response
        assert len(resp) > 0, 'Пустой вывод команды show ntp associations'
        allure.attach(resp, 'Вывод команды show ntp associations', attachment_type=allure.attachment_type.TEXT)

        # Символ '*' нужно добавить перед ip адресом сервера т.к. он указывает на факт синхронизации
        number = resp.find('*%s' %DUT.server['ip'])
        assert number != -1, \
            "В выводе команды show ntp associations не обнаружен символ '*', нет синхронизации с одноранговым узлом"
    finally:
        conn.send('quit\r')
        conn.close()
