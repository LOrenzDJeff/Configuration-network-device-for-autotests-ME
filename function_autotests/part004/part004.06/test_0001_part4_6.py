from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.6')
@allure.story('Загрузка конфигурации на МЕ маршрутизаторы')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part4_6
@pytest.mark.init_config4_6
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config046_dut1",scope="session")), 
 			 pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config046_dut2",scope="session")), 
 			 pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config046_dut3",scope="session"))
			]
			)

def test_me_init_config_upload_part4_6(DUT):
	DUT.connection()
	DUT.startup()
	DUT.lacp()
	DUT.ipv4()
	DUT.loopback_ipv4()
	DUT.lldp_agent_add()
	DUT.isis_add()
	DUT.isis_add_lfa()
	DUT.mpls_add()
	DUT.ldp_add()
	for i in [DUT1.loopback['ip_witout_mask'], DUT2.loopback['ip_witout_mask'],DUT3.loopback['ip_witout_mask']]:
		if DUT.loopback['ip_witout_mask'] != i:
			DUT.add_neighbor_ldp(i)
	DUT.close()
	print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)
