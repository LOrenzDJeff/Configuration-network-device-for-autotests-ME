from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.9')
@allure.story('Загрузка конфигурации на ESR маршрутизатор')
@allure.title('Загрузка конфигурации на ESR маршрутизатор')
@pytest.mark.part14_9
@pytest.mark.init_config14_9
@pytest.mark.parametrize('ip, hostname, login, password, part', [(DUT4['host_ip'], DUT4['hostname'], DUT4['login'], DUT4['password'], 'part14.9')])
@pytest.mark.usefixtures('esr_init_configuration')
def test_esr_init_config_upload_part14_9 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ESR LABR02 для тестов из Части 14.9 документа     
    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

