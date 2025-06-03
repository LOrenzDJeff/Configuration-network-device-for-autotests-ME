from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.2')
@allure.story('Загрузка конфигурации на ESR маршрутизатор')
@allure.title('Загрузка конфигурации на ESR маршрутизатор')
@pytest.mark.part14_2
@pytest.mark.esr_init_config142
@pytest.mark.parametrize('ip, hostname, login, password, part', [(DUT4['host_ip'], DUT4['hostname'], DUT4['login'], DUT4['password'], 'part14.2')])
@pytest.mark.usefixtures('esr_init_configuration')
def test_esr_init_config_upload_part14_2 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ESR LABR02 для тестов из Части 14.2 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

