from conftest import *

@allure.feature('Загрузка начальной конфигурации')
@allure.story('Загрузка конфигурации на MES коммутатор с последующей перезагрузкой. Часть 14.1')
@pytest.mark.part14_1
@pytest.mark.init_config14_1
@pytest.mark.parametrize('ip , hostname , login, password, part', [(DUT5['host_ip'] , DUT5['hostname'] , DUT5['login'] , DUT5['password'] , 'part14.1')])
@pytest.mark.usefixtures('mes_init_reboot')
#@pytest.mark.usefixtures('mes_init_alt_configuration')
#def test_mes_init_alt_config_upload_part14_1 (ip, hostname, login, password, part):
def test_mes_init_config_upload_reload_part14_1 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на MES LABS01 для тестов из Части 14.1 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))
