from conftest import *

@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 1')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part1
@pytest.mark.init_config_part1
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config001_dut1")), 
 			 pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config001_dut2")), 
 			 pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config001_dut3")),
			]
			)
 
def test_me_init_config_ME2001(DUT): 
# В данном тесте будем загружать начальную конфигурацию на ME маршрутизаторы для тестов из Части 1 документа
	for i in range(2):
		try:
			DUT.ipv4()
			DUT.lacp()
			print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)
			break
		except BrokenPipeError:
			print("Пропало подключение, пытаемся восстановить")
			DUT.connection()
