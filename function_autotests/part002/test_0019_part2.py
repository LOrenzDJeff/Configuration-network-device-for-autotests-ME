from conftest import *


@pytest.mark.part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.009:Проверка banner login и banner motd')
@allure.title('В данном тесте будем тестировать banner motd и banner login для ssh-соединения при выключенном tacacs-сервере')
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')     
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_login_banner(DUT):
    banner_login='This device can be used by authorized users only. Unauthorized access is prosecuted by federal law (Federal law 63, article 272 of the Criminal Code of the Russian Federation'
    banner_motd='Test motd banner'
    resp = connection_test_ssh(DUT.host_ip,'admin','password')
    allure.attach(resp,'Вывод banner login и banner motd для %s'%DUT.host_ip, attachment_type=allure.attachment_type.TEXT)
    assert_that(resp.find(banner_login)!=-1,"Ожидаемое сообщение banner_login - %s не обнаружено при подключении к узлу %s"%(banner_login, DUT.host_ip))
    assert_that(resp.find(banner_motd)!=-1,"Ожидаемое сообщение banner_motd - %s не обнаружено при подключении к узлу %s"%(banner_motd,DUT.host_ip))
    
