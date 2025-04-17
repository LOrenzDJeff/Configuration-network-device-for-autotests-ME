from conftest import *

@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 2')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part2
@pytest.mark.init_config2
@pytest.mark.parametrize('ip , hostname , login, password, part', 
			[pytest.param(DUT1['host_ip'], DUT1['dir_hostname'], DUT1['login'], DUT1['password'], 'part2', marks=pytest.mark.dependency(name="load_config002_dut1")), 
 			 pytest.param(DUT2['host_ip'], DUT2['dir_hostname'], DUT2['login'], DUT2['password'], 'part2', marks=pytest.mark.dependency(name="load_config002_dut2")), 
 			 pytest.param(DUT3['host_ip'], DUT3['dir_hostname'], DUT3['login'], DUT3['password'], 'part2', marks=pytest.mark.dependency(name="load_config002_dut3"))])
 
@pytest.mark.usefixtures('me_init_configuration')
def test_me_init_config_upload_part2 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ME маршрутизаторы для тестов из Части 5 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

