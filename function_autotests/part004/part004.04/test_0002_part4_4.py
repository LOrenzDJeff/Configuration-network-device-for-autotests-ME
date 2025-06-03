from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.4')
@allure.story('Загрузка конфигурации на Juniper маршрутизатор')
@allure.title('Загрузка конфигурации на Juniper маршрутизатор')
@pytest.mark.part4_4
@pytest.mark.junos_init_config4_4
@pytest.mark.dependency(depends=["load_config044_dut1","load_config044_dut2","load_config044_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT4, marks=pytest.mark.dependency(name="load_config044_dut4"))
			]
        )	

def test_junos_init_config_upload_part4_4(DUT):
	DUT.connection()
	DUT.loopback_ipv4()
	DUT.ipv6()
	DUT.loopback_ipv6()
	DUT.isis_add()
	DUT.isis_metric(DUT.vlanid1, 20)
	DUT.isis_metric(DUT.vlanid2, 20)
	DUT.isis_metric(DUT.vlanid3, 20)
	DUT.close()
	print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)
