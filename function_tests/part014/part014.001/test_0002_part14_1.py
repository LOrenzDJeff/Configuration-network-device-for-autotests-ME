from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.1')
@allure.story('Загрузка конфигурации на Juniper маршрутизатор')
@allure.title('Загрузка конфигурации на Juniper маршрутизатор')
@pytest.mark.part14_1
@pytest.mark.init_config14_1
@pytest.mark.parametrize('ip, hostname, login, password, part', [(DUT6['host_ip'], DUT6['hostname'], DUT6['login'], DUT6['password'], 'part14.1')])
@pytest.mark.usefixtures('junos_init_configuration')
def test_junos_init_config_upload_part14_1 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на vMX LABR01 для тестов из Части 14.1 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

