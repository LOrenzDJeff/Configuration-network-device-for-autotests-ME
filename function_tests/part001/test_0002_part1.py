from conftest import *

@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 1')
@allure.story('Загрузка конфигурации на Juniper маршрутизатор')
@allure.title('Загрузка конфигурации на Juniper маршрутизатор')
@pytest.mark.part1
@pytest.mark.init_config_part1
@pytest.mark.dependency(depends=["load_config001_dut1","load_config001_dut2","load_config001_dut3"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password, part', 
			[pytest.param(DUT4['host_ip'], DUT4['dir_hostname'], DUT4['login'], DUT4['password'], 'part1', 
             marks=pytest.mark.dependency(name="load_config001_dut4", depends=["load_config001_dut1","load_config001_dut2","load_config001_dut3"],scope='session'))])
			
@pytest.mark.usefixtures('cisco_init_configuration')
def test_junos_init_config_upload_part1 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на Junos LABR01 для тестов из Части 1 документа     
    print("Загрузка конфигурации на %s прошла успешно!"%hostname)
