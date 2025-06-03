from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.002:Проверка syslog, backup')
@allure.title('В данном тесте будем выполнять команду-маркер на ME маршрутизаторе, а затем искать её в журнале выполненных команд syslog-сервера')
@pytest.mark.part2
@pytest.mark.syslog
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_syslog_part2(DUT):
# Подключаемся к маршрутизатору c адресом ip, а затем выполняем команду-маркер 'show vrf bla-bla-bla', чтобы потом её искать на syslog-сервере
    resp1 = ''
    resp2 = ''
    conn2 = Telnet()
    acc2 = Account(DUT.login, DUT.password)
    conn2.connect(DUT.host_ip)
    conn2.login(acc2)
    conn2.set_prompt('#')
    conn2.execute('configure')
    if DUT.hostname == DUT1.hostname:
        conn2.execute('logging host %s vrf MGN facility local3'%DUT.server['ip'])
    elif DUT.hostname == DUT2.hostname:
        conn2.execute('logging host %s vrf default facility local3'%DUT.server['ip'])
    elif DUT.hostname == DUT3.hostname:
        conn2.execute('logging host %s vrf mgmt-intf facility local3'%DUT.server['ip'])    
    conn2.execute('commit')
    conn2.execute('end')
    var_time = int(time.time())   # Получаем кол-во секунд с момента начала эпохи Unix. Они будут нужны для формирования уникальной команды-маркера
    cmd = ('show vrf %s'%var_time)  # Уникальная команда-маркер которую будем искать в syslog-файле
    conn2.execute(cmd)


    time.sleep(10)
# Подключаемся к syslog серверу  и анализируем файл 'syslog' на предмет содержания команды-маркера
#    conn3 = Telnet()
    conn3 = SSH2()
    acc3 = Account(DUT.server['login'], DUT.server['password'])
    conn3.connect(DUT.server['ip'])   # Подключаемся к syslog-серверу
    conn3.set_prompt('$')
    conn3.login(acc3)
    conn3.set_prompt(':')
    conn3.execute('sudo su')
    conn3.set_prompt('#')
    conn3.execute(DUT.server['password'])
    conn3.execute('grep -e "%s" /var/log/me5000/%s/me5k.log'%(cmd,DUT.host_ip))
    resp1 = conn3.response
    #print("\nРезультат парсинга  команды grep -e - %s\n"%resp1)
    allure.attach(resp1,'Парсинг syslog-файла на предмет нахождения в нем команды-маркера %s'%cmd)
    number = resp1.count('command: \'%s\''%cmd) # Считаем сколько раз команда-маркер встречается в log-файле
    # print('Кол-во обнаруженных маркеров number1 - %i\r'%number1)

    conn2.execute('configure')
    if DUT.hostname == DUT1.hostname:
        conn2.execute('no logging host %s vrf MGN'%DUT.server['ip'])
    elif DUT.hostname == DUT2.hostname:
        conn2.execute('no logging host %s vrf default'%DUT.server['ip'])
    elif DUT.hostname == DUT3.hostname:
        conn2.execute('logging host %s vrf mgmt-intf'%DUT.server['ip'])    
    conn2.execute('commit')
    conn2.execute('end')
    conn2.send('quit\r')
    # conn2.close()
    # conn3.close()     
    assert_that(number == 1,"Команда-маркер %s в syslog-файле  обнаружена %s раз, хотя её ожидали только один"%(cmd,number))   
    return
