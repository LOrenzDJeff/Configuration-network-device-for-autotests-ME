from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.4')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part4_4
@pytest.mark.init_config4_4
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config044_dut1",scope="session")), 
 			 pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config044_dut2",scope="session")), 
 			 pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config044_dut3",scope="session"))
			]
			)

def test_me_init_config_upload_part4_4(DUT):
	DUT.connection()
	DUT.startup()
	DUT.lacp()
	DUT.ipv4()
	DUT.loopback_ipv4()
	DUT.lldp_agent_add()
	DUT.ipv6()
	DUT.loopback_ipv6()
	DUT.isis_add()
	DUT.isis_add_lfa()
	DUT.isis_metric(DUT.neighor1["int_name"], 11)
	DUT.isis_metric(DUT.neighor2["int_name"], 9)
	DUT.isis_metric(DUT.neighor3["int_name"], 20)
	DUT.close()
	print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)
