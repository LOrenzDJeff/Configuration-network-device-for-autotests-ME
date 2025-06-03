from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.7')
@allure.story('Загрузка конфигурации на ME маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part14_7
@pytest.mark.init_config14_7
@pytest.mark.parametrize('ip, hostname, login, password, part', 
			[pytest.param(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'], 'part14.7', marks=pytest.mark.dependency(name="load_config147_dut1")), 
 			 pytest.param(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'], 'part14.7', marks=pytest.mark.dependency(name="load_config147_dut2")), 
 			 pytest.param(DUT3['host_ip'], DUT3['hostname'], DUT3['login'], DUT3['password'], 'part14.7', marks=pytest.mark.dependency(name="load_config147_dut3"))])
 
@pytest.mark.usefixtures('me_init_configuration')
def test_me_init_config_upload_part14_7 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ME маршрутизатор для тестов из Части 14.7 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

