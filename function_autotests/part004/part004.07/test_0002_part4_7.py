from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.7')
@allure.story('Загрузка конфигурации на ESR маршрутизатор')
@allure.title('Загрузка конфигурации на ESR маршрутизатор')
@pytest.mark.part4_7
@pytest.mark.init_config4_7
@pytest.mark.parametrize('ip , hostname , login, password, part', 
			[pytest.param(DUT4['host_ip'], DUT4['hostname'], DUT4['login'], DUT4['password'], 'part4.7',
            marks=pytest.mark.dependency(name="load_config47_dut4",depends=["load_config47_dut1","load_config47_dut2","load_config47_dut3"],scope='session'))])

@pytest.mark.usefixtures('esr_init_configuration')
def test_esr_init_config_upload_part4_7 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ESR LABR02 для тестов из Части 4.7 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

