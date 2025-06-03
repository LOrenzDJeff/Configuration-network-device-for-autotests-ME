from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.3')
@allure.story('Загрузка конфигурации на Juniper маршрутизатор')
@allure.title('Загрузка конфигурации на Juniper маршрутизатор')
@pytest.mark.part14_3
@pytest.mark.junos_init_config14_3
@pytest.mark.parametrize('ip, hostname, login, password, part', 
			[pytest.param(DUT6['host_ip'], DUT6['hostname'], DUT6['login'], DUT6['password'], 'part14.3', marks=pytest.mark.dependency(name="load_config143_dut4"))])
			
@pytest.mark.usefixtures('junos_init_configuration')
def test_junos_init_config_upload_part14_3 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на vMX LABR01 для тестов из Части 14.3 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

