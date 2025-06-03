from conftest import *
from driver import ME5000CliDriver


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 0')
@allure.story('Проверка статуса backup на FMC1 перед upgrade-ом')
@allure.title('Проверка статуса backup на FMC1 перед upgrade-ом')
@pytest.mark.part0
@pytest.mark.check_fmc0_backup_part0
@pytest.mark.parametrize('ip, login, password, hostname', [(DUT9['host_ip'], DUT9['login'], DUT9['password'], DUT9['hostname'])])
def test_atDR1_backup_status (ip, login, password, hostname): 

    conn2 = Telnet()
    conn2.set_prompt('#')
    acc2 = Account(login , password)
    conn2.connect(ip)
    conn2.login(acc2)
    conn2.set_driver(ME5000CliDriver())

    cmd='terminal datadump'
    try:
        conn2.execute(cmd) # пытаемся выполнить terminal datadump
    except Exception as err:
        exception_error_message='Сработал exception %s при выполнении команды %s'%(type(err),cmd)

        sys.exit(exception_error_message)        
    cmd='show redundancy' 
    try:
        conn2.execute(cmd) # пытаемся выполнить show redundancy
    except Exception as err:
        exception_error_message='Сработал exception %s при выполнении команды %s'%(type(err),cmd)

        sys.exit(exception_error_message)        
    
    resp2=conn2.response
#    print(resp2)
    resp2_index=resp2.find('This unit (0/FMC1) is in MASTER role') # Ищем в выводе команды show redundancy, выполненной на FMC1 эту строку
#    print(resp2_index)
    if (resp2_index !=-1):
        conn2.set_prompt('\[n\]') 
        cmd='redundancy switchover'
        try:
            conn2.execute(cmd)
        except Exception as err:
            exception_error_message='Сработал exception %s при выполнении команды %s'%(type(err),cmd)

            sys.exit(exception_error_message)

        conn2.set_prompt('#') 
        try:
            conn2.send('y')
            conn2.execute('') # Подсказано Хуторянским. см задачу 234205
            #print('\rОтправили yes на команду redundancy switchover\r')
        except Exception as err:
            exception_error_message='Сработал exception %s при выполнении yes для команды %s на FMC1'%(type(err),cmd)
            conn2.set_prompt('[n]')
            conn2.execute('reload system')
            conn2.send('y')
            conn2.execute('')
            print('\rFMC1 на %s отправлена в перезагрузку, ждем %s сек\r'%(DUT9['hostname'],DUT9['boot_timer']))
            time.sleep(DUT9['boot_timer'])
            assert_that(err =='',"Сработал exception при выполнении yes для команды %s на FMC1. Ошибка - %s"%(cmd,err))


            #sys.exit(exception_error_message)

        resp=conn2.response
        allure.attach(resp, 'Вывод второй команды redundancy switchover', attachment_type=allure.attachment_type.TEXT)
        time.sleep(15)
        print('Выполнили дополнительный redundancy switchover FMC1 -> FMC0\r')


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 0')
@allure.story('Проверка FMC0 на offline перед upgrade-ом')
@allure.title('Проверка FMC0 на offline статус перед upgrade-ом')
@pytest.mark.part0
@pytest.mark.check_fmc_offline_part0
@pytest.mark.parametrize('ip, login, password, hostname, boot_timer', [(DUT3.host_ip, DUT3.login, DUT3.password, DUT3.hostname, DUT3.boot_timer),
                                                                       (DUT9['host_ip'], DUT9['login'], DUT9['password'], DUT9['hostname'], DUT9['boot_timer'])])
def test_DUT_offline_status (ip, login, password, hostname, boot_timer): 

    conn = Telnet()
    conn.set_prompt('#')
    acc = Account(login , password)
    conn.connect(ip)
    offline_flag=-1
    try:
        conn.login(acc)
    except Exception as err:
        print('\nПри подключении к %s возникла ошибка -%s\n'%(hostname,err))
    
        resp = conn.response
        offline_flag=resp.find('offline mode')
#        print(offline_flag)
#        print(resp)
        if offline_flag!=-1:
            print('\nОбнаружен offline режим у %s Отправляем в перезагрузку на %s секунд\n'%(hostname,boot_timer))
            cmd="reload system"
            try:
                conn.set_prompt('[n]')
                conn.execute(cmd)
                conn.send('y')
                conn.execute('') # Подсказано Хуторянским. см задачу 234205
                print('\r%s отправлен в перезагрузку, ждем %s сек\r'%(hostname,boot_timer))
                time.sleep(int(boot_timer))

            except Exception as err:
                exception_error_message='Сработал exception %s при выполнении yes для команды %s на FMC1'%(type(err),cmd)
#                assert_that(err =='',"Сработал exception при выполнении yes для команды %s на FMC0. Ошибка - %s"%(cmd,err))
                assert_that(err=='',"На %s, сработал exception при выполнении yes для команды %s . Ошибка - %s"%(hostname,cmd,err))
# После истечения таймера перезагрузки пытаемся подключиться повторно и выполнить команды show firmware
            conn.close()
            time.sleep(5)
            conn = Telnet()
            conn.set_prompt('#')
            acc = Account(login , password)
            conn.connect(ip)
            offline_flag=-1
            try:
                conn.login(acc)
            except Exception as err:
                print('\nПри повторном подключении после перезагрузки к %s возникла ошибка - %s\n'%(hostname,err))
                resp = conn.response
                offline_flag=resp.find('offline mode')
                print(offline_flag)
                if offline_flag!=-1:
                    print('\nВторой раз обнаружен offline режим у %s перезагружаем через rootshell и ждем  %s секунд\n'%(hostname,boot_timer))
                    cmd="rootshell"
                    try:
                        conn.set_prompt('Password:')
                        conn.execute(cmd)
                        conn.send('password')
                        conn.execute('reboot')
                        print('\r%s отправлен в перезагрузку из rootshell, ждем %s сек\r'%(hostname,boot_timer))
                    except Exception as err:
                        exception_error_message='Сработал exception %s при выполнении yes для команды %s на FMC1'%(type(err),cmd)
                        assert_that(err=='',"На %s, сработал exception при попытке перезагрузки из %s . Ошибка - %s"%(hostname,cmd,err))



#                assert_that(err=='',"При повторном подключении после перезагрузки к %s возникла ошибка - %s\n'%(hostname,err)")

            print("Вывод команды %s после перезагрузки %s"%(cmd,hostname))



#    assert_that(offline_flag==-1,"Обнаружен offline режим у %s, устройство отправлено в перезагрузку"%DUT3['hostname'])




