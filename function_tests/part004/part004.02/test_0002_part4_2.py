from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.2')
@allure.story('Загрузка конфигурации на Juniper маршрутизатор')
@allure.title('Загрузка конфигурации на Juniper маршрутизатор')
@pytest.mark.part4_2
@pytest.mark.junos_init_config4_2
@pytest.mark.dependency(depends=["load_config042_dut1","load_config042_dut2","load_config042_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT4, marks=pytest.mark.dependency(name="load_config042_dut4"))
			]
        )			
		
def test_junos_init_config_upload_part4_2(DUT): 
# В данном тесте будем загружать начальную конфигурацию на ESR LABR02 для тестов из Части 4_2 документа     
	DUT.connection()
	DUT.loopback_ipv4()
	DUT.ipv6()
	DUT.loopback_ipv6()
	DUT.isis_add()
	DUT.close()
	print("Загрузка конфигурации на %s прошла успешно!"%DUT.hostname)

