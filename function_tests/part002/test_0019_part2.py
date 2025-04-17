from conftest import *


@pytest.mark.part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.009:Проверка banner login и banner motd')
@allure.title('Проверка banner motd и banner login для ssh-соединения при выключенном tacacs-сервере')
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')     
@pytest.mark.parametrize('host_ip , login , password', [(DUT1['host_ip'] , DUT1['login'] , DUT1['password']),(DUT2['host_ip'] , DUT2['login'] , DUT2['password']),(DUT3['host_ip'] , DUT3['login'] , DUT3['password'])])
def test_login_banner(host_ip, login, password):
    banner_login='This device can be used by authorized users only. Unauthorized access is prosecuted by federal law (Federal law 63, article 272 of the Criminal Code of the Russian Federation'
    banner_motd='Test motd banner'
    resp = connection_test_ssh(host_ip,'admin','password')
    allure.attach(resp,'Вывод banner login и banner motd для %s'%host_ip, attachment_type=allure.attachment_type.TEXT)
    assert_that(resp.find(banner_login)!=-1,"Ожидаемое сообщение banner_login - %s не обнаружено при подключении к узлу %s"%(banner_login, host_ip))
    assert_that(resp.find(banner_motd)!=-1,"Ожидаемое сообщение banner_motd - %s не обнаружено при подключении к узлу %s"%(banner_motd,host_ip))
    
