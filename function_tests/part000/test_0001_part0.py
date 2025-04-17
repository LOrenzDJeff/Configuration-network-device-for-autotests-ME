from conftest import *

# Обновление ПО на маршрутизаторах стенда перед запуском функциональных тестов
@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 0')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы. Перед upgrade-ом')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part0
@pytest.mark.parametrize('ip, hostname, login, password, part', 
			[(DUT1['host_ip'], DUT1['dir_hostname'], DUT1['login'], DUT1['password'], 'before_upgrade'), 
 			 (DUT2['host_ip'], DUT2['dir_hostname'], DUT2['login'], DUT2['password'], 'before_upgrade'), 
 			 (DUT3['host_ip'], DUT3['dir_hostname'], DUT3['login'], DUT3['password'], 'before_upgrade')])

@pytest.mark.usefixtures('me_init_configuration')
def test_me_init_config0_upload (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ME маршрутизаторы для тестов из Части 0 документа
	print('Стартовая конфигурация на %s прошла успешно!'%(hostname))
