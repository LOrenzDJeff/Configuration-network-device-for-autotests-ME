from conftest import *

# Обновление ПО на маршрутизаторах стенда перед запуском функциональных тестов
@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 0')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы. Перед upgrade-ом')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part0
@pytest.mark.parametrize("DUT",
			[ DUT1, DUT2, DUT3])
@pytest.mark.usefixtures('move_mgmt_int_from_mgmt_intf')
def test_me_init_config0_upload (DUT): 
# В данном тесте будем загружать начальную конфигурацию на ME маршрутизаторы для тестов из Части 0 документа
	DUT.startup()
	print('Стартовая конфигурация на %s прошла успешно!'%(DUT.hostname))
