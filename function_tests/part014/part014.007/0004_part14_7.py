from conftest import *

@allure.feature('Загрузка начальной конфигурации')
@allure.story('Загрузка конфигурации на MES коммутатор с последующей перезагрузкой. Часть 14.7')
@pytest.mark.part14_7
@pytest.mark.mes_init_config14_7
@pytest.mark.parametrize('ip , hostname , login, password, part', [(DUT5['host_ip'] , DUT5['hostname'] , DUT5['login'] , DUT5['password'] , 'part14.7')])
@pytest.mark.usefixtures('mes_init_reboot')
def test_mes_init_config_upload_reload_part14_7 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на MES LABS01 для тестов из Части 14.2 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))
