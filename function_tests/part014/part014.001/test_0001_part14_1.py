from conftest import *

@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.1')
@allure.story('Загрузка конфигурации на ME маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part14_1
@pytest.mark.init_config14_1
@pytest.mark.parametrize("DUT",
						 [
							 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config014_1_dut1", scope="session")),
							 pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config014_1_dut2", scope="session")),
							 pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config014_1_dut3", scope="session"))
						 ]
						 )
def test_me_init_config(DUT):
	DUT.connection()
	DUT.startup()
	DUT.lacp()
	DUT.ipv4()
	print("Загрузка конфигурации на %s прошла успешно!" % DUT.hostname)
	DUT.close()

# @pytest.mark.parametrize('ip, hostname, login, password, part',
# 			[(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'], 'part14.1'),
#  			 (DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'], 'part14.1'),
#  			 (DUT3['host_ip'], DUT3['hostname'], DUT3['login'], DUT3['password'], 'part14.1')])
#
# @pytest.mark.usefixtures('me_init_configuration')
# def test_me_init_config_upload_part14_1 (ip, hostname, login, password, part):
# # В данном тесте будем загружать начальную конфигурацию на ME маршрутизатор для тестов из Части 14.1 документа
#     print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

