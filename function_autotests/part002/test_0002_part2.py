from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.002:Проверка syslog, backup')
@allure.title('В данном тесте будем проверять формирование backup-файла конфигурации ME маршрутизатора на TFTP сервере')
@pytest.mark.part2
@pytest.mark.check_backup
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
#@pytest.mark.usefixtures('me_init_configuration')
def test_backup_part2(DUT):
# Подключаемся к tftp-серверу и удаляем все ранее сохраненные backup-файлы, если они есть
    conn3 = SSH2()
    acc3 = Account(DUT.server['login'], DUT.server['password'])
    conn3.connect(DUT.server['ip'])
    conn3.set_prompt('$')
    conn3.login(acc3)
    conn3.set_prompt(':')
    conn3.execute('sudo su')
    conn3.set_prompt('#')
    conn3.execute(DUT.server['password'])

    cmd=("rm -f /tftp/%s/*.*"%DUT.dir)
    conn3.execute(cmd)
#    conn3.execute('rm -f /home/pryahin/me5k/tftpd/%s/*.*'%hostname) # Папка /tftd/ является домашней директорией tftp-сервера на момент написания этого теста

# Подключаемся к маршрутизатору hostname  чтобы изменить его конфигурацию и проверить как сформировался backup-файл на tftp-сервере
    conn2 = Telnet()
    acc2 = Account(DUT.login, DUT.password)
    conn2.connect(DUT.host_ip)
    conn2.login(acc2)
    conn2.set_prompt('#')
    conn2.execute('configure')
    if DUT.hostname==DUT1.hostname:
        conn2.execute('backup to tftp://%s/%s/ interval 60 pre-commit vrf MGN'%(DUT.server['ip'],DUT.dir))
    elif DUT.hostname == DUT2.hostname:
        conn2.execute('backup to tftp://%s/%s/ daily 13:00:00 post-commit'%(DUT.server['ip'],DUT.dir))
    elif DUT.hostname == DUT3.hostname:
        conn2.execute('backup to tftp://%s/%s/ pre-commit vrf mgmt-intf'%(DUT.server['ip'],DUT.dir))    
    conn2.execute('commit')

    conn2.execute('exit')
    conn2.execute('hostname %s-XYZ' %DUT.hostname)
    conn2.execute('commit')
    conn2.execute('hostname %s' %DUT.hostname)
    conn2.execute('commit')

    if DUT.hostname==DUT1.hostname:
        conn2.execute('no backup to tftp://%s/%s/'%(DUT.server['ip'],DUT.dir))
    elif DUT.hostname == DUT2.hostname:
        conn2.execute('no backup to tftp://%s/%s/'%(DUT.server['ip'],DUT.dir))
    elif DUT.hostname == DUT3.hostname:
        conn2.execute('no backup to tftp://%s/%s/'%(DUT.server['ip'],DUT.dir))    
    conn2.execute('commit')
    conn2.execute('exit')
    conn2.send('quit\r')
    conn2.close()
    conn3.execute('ls -lah /tftp/%s/'%DUT.dir) # Путь к backup файлам на виртуальном syslog-сервере
    resp = conn3.response
    allure.attach(resp)
    number =resp.find('backup_cfg')
    conn3.set_prompt('$')
    conn3.send('exit\r')
    conn3.send('exit\r')
    assert_that(number > 1,"backup_cfg файл не найден на tftp сервере %s"%DUT.server['ip'])
#    assert  number > 1 # Значит искомые backup файлы присутсвуют в каталоге
    return

