from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.5')
@allure.story('Загрузка конфигурации на Juniper маршрутизаторы')
@allure.title('Загрузка конфигурации на Juniper маршрутизатор')
@pytest.mark.part14_5
@pytest.mark.junos_init_config14_5
@pytest.mark.parametrize('ip, hostname, login, password, part', 
			[pytest.param(DUT6['host_ip'], DUT6['hostname'], DUT6['login'], DUT6['password'], 'part14.5', marks=pytest.mark.dependency(name="load_config145_dut6"))])
			
@pytest.mark.usefixtures('junos_init_configuration')
def test_junos_init_config_upload_part14_5 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на vMX LABR01 для тестов из Части 14.5 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

