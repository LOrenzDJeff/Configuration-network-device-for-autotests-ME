from conftest import *


@pytest.mark.part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.009:Проверка banner login и banner motd')
@allure.title('В данном тесте будем тестировать banner motd и banner login для telnet-соединения при включенном tacacs-сервере')    
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session') 
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
@pytest.mark.usefixtures('run_tacacs_server')
@pytest.mark.skip(reason="Сервер не поддерживает docker")
def test_banner_login_tacacs(DUT):
    banner_login='This device can be used by authorized users only. Unauthorized access is prosecuted by federal law (Federal law 63, article 272 of the Criminal Code of the Russian Federation'
    banner_login_1='Access to this device is allowed only for authorized users. STOP if you are not authorized! Violation of this rule is prosecuted by federal law.'
    banner_motd='Test motd banner'
    resp= connection_test(DUT.host_ip,'admin','test_password','part2')
    allure.attach(resp,'Вывод banner login и banner motd для %s'%DUT.host_ip, attachment_type=allure.attachment_type.TEXT)
    assert_that(resp.find(banner_login)!=-1,"Ожидаемое сообщение banner_login - %s не обнаружено при подключении к узлу %s"%(banner_login, DUT.host_ip))
    assert_that(resp.find(banner_login_1)!=-1,"Ожидаемое сообщение banner_login_1 - %s не обнаружено при подключении к узлу %s, хотя tacacs-сервер включен"%(banner_login_1, DUT.host_ip))
    assert_that(resp.find(banner_motd)!=-1,"Ожидаемое сообщение banner_motd - %s не обнаружено при подключении к узлу %s"%(banner_motd, DUT.host_ip))

