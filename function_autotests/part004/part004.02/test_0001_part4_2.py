from conftest import *

@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.2')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part4_2
@pytest.mark.init_config4_2
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config042_dut1",scope="session")), 
 			 pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config042_dut2",scope="session")), 
 			 pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config042_dut3",scope="session"))
			]
			)

def test_me_init_config_upload_part4_2(DUT): 
	DUT.connection()
	DUT.startup()
	DUT.lacp()
	DUT.ipv4()
	DUT.loopback_ipv4()
	DUT.lldp_agent_add()
	DUT.ipv6()
	DUT.loopback_ipv6()
	DUT.isis_add()
	DUT.close()
	print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)

