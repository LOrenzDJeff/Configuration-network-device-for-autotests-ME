from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 0')
@allure.story('Загрузка конфигурации на MES коммутатор. Перед upgrade-ом.')
@allure.title('Загрузка конфигурации на MES коммутатор')
@pytest.mark.part0
@pytest.mark.mes_init_config0
@pytest.mark.parametrize("DUT",
			[ DUT5 ])
#@pytest.mark.usefixtures('mes_init_configuration')
@pytest.mark.usefixtures('mes_init_reboot')
def test_mes_init_config_reboot_part0(DUT): 
# В данном тесте будем загружать начальную конфигурацию на MES LABS01 для тестов из Части 5 документа     
    DUT.init_reboot()
    DUT.connection()
