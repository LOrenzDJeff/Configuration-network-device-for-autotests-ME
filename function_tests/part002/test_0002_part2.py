from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.002:Проверка syslog, backup')
@allure.title('В данном тесте будем проверять формирование backup-файла конфигурации ME маршрутизатора на TFTP сервере')
@pytest.mark.part2
@pytest.mark.check_backup
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param("DUT1"), 
 			 pytest.param("DUT2"), 
 			 pytest.param("DUT3")
			]
			)
#@pytest.mark.usefixtures('me_init_configuration')
def test_backup_part2(DUT):
# Подключаемся к tftp-серверу и удаляем все ранее сохраненные backup-файлы, если они есть
    router = setting_ME(DUT)
    with open('config_OOP.json', 'r', encoding='utf-8') as file:
        check = json.load(file)
    conn3 = Telnet()
    acc3 = Account(router.server['login'], router.server['password'])
    conn3.connect(router.server['ip'])
    conn3.login(acc3)
    cmd=("rm -f /home/pryahin/me5k/tftpd/%s/*.*"%router.hostname)
    conn3.execute(cmd)
#    conn3.execute('rm -f /home/pryahin/me5k/tftpd/%s/*.*'%hostname) # Папка /tftd/ является домашней директорией tftp-сервера на момент написания этого теста

# Подключаемся к маршрутизатору hostname  чтобы изменить его конфигурацию и проверить как сформировался backup-файл на tftp-сервере
    conn2 = Telnet()
    acc2 = Account(router.login, router.password)
    conn2.connect(router.host_ip)
    conn2.login(acc2)
    conn2.set_prompt('#')
    conn2.execute('configure')
    if router.hostname==check["DUT1"]['hostname']:
        conn2.execute('backup to tftp://%s/%s/ interval 60 pre-commit vrf MGN'%(router.server['ip'],router.hostname))
    elif router.hostname == check["DUT2"]['hostname']:
        conn2.execute('backup to tftp://%s/%s/ daily 13:00:00 post-commit'%(router.server['ip'],router.hostname))
    elif router.hostname == check["DUT3"]['hostname']:
        conn2.execute('backup to tftp://%s/%s/ pre-commit vrf mgmt-intf'%(router.server['ip'],router.hostname))    
    conn2.execute('commit')

    conn2.execute('exit')
    conn2.execute('hostname %s-XYZ' %router.hostname)
    conn2.execute('commit')
    conn2.execute('hostname %s' %router.hostname)
    conn2.execute('commit')
    conn2.execute('exit')
    conn2.send('quit\r')
    conn2.close()
    conn3.execute('ls -lah /home/pryahin/me5k/tftpd/%s/'%router.hostname) # Путь к backup файлам на виртуальном syslog-сервере
    resp = conn3.response
    allure.attach(resp)
    number =resp.find('backup_cfg')

    conn3.send('exit')
    conn3.close()
    assert_that(number > 1,"backup_cfg файл не найден на tftp сервере %s"%check["DUT7"]["ip"])
#    assert  number > 1 # Значит искомые backup файлы присутсвуют в каталоге
    return

