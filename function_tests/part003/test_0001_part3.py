from conftest import *

@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 3')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part3
@pytest.mark.init_config3
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config003_dut1",scope="session")), 
 			 pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config003_dut2",scope="session")), 
 			 pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config003_dut3",scope="session"))
			]
			)
 
def test_me_init_config(DUT):
	DUT.connection()
	DUT.startup()
	DUT.lacp()
	DUT.ipv4()
	DUT.loopback_ipv4()
	DUT.lldp_agent_add()
	print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)
	DUT.close()