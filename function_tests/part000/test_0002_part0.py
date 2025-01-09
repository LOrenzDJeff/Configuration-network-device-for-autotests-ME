from conftest import *


@allure.feature('Обновление ПО на МЕ маршрутизаторах')
@allure.story('Обновление ПО на МЕ маршрутизаторах')
@pytest.mark.part0
@pytest.mark.upgrade_software
@pytest.mark.parametrize('ip, login,password,target_version, path_version', [(DUT1.host_ip,DUT1.login,DUT1.password,'3.9.7.16RC','./tftpd/')])
def test_upgrade_me(ip,login,password,target_version, path_version):
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(me_software_upgrade, DUT1.host_ip,  DUT1.login, DUT1.password,DUT1.hostname, target_version, path_version,int(DUT1.boot_timer))
            future2 = executor.submit(me_software_upgrade, DUT2.host_ip, DUT2.login, DUT2.password,DUT2.hostname, target_version, path_version,int(DUT2.boot_timer))
            future3 = executor.submit(me_software_upgrade, DUT3.host_ip, DUT3.login, DUT3.password,DUT3.hostname, target_version, path_version,int(DUT3.boot_timer))
            DUT1_soft_ver = future.result() # Получаем из параллельного потока версию ПО!
            DUT2_soft_ver = future2.result()
            DUT3_soft_ver = future3.result()
            print('Target software version для %s - %s\r'%(DUT1.hostname,DUT1_soft_ver))
            print('Target software version для %s - %s\r'%(DUT2.hostname,DUT2_soft_ver))
            print('Target software version для %s - %s\r'%(DUT3.hostname,DUT3_soft_ver))
        resp = ''
        conn = Telnet()
        acc = Account(DUT1.login , DUT1.password)
        conn.connect(DUT1.host_ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('show system') 
        resp = conn.response
        print(resp) # Раскомментируй, если хочешь посмотреть вывод команды show system
# C помощью магии модуля textFSM сравниваем вывод команды 'show firmware' c шаблоном в файле parse_show_privilege.txt 
        template = open('./templates/parse_show_system_after_upgrade.txt')
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
        print(result) # Раскомментируй, если хочешь посмотреть результат парсинга
        DUT1_version=result[0][2]
        DUT1_uptime=result[0][3]
        conn.send('quit\r')
        conn.close()

        conn2 = Telnet()
        acc2 = Account(DUT2.login, DUT2.password)
        conn2.connect(DUT2.host_ip)
        conn2.login(acc2)
        conn2.set_prompt('#')
        conn2.execute('show system') 
        resp2 = conn2.response
# C помощью магии модуля textFSM сравниваем вывод команды 'show firmware' c шаблоном в файле parse_show_privilege.txt 
        template2 = open('./templates/parse_show_system_after_upgrade.txt')
        fsm2 = textfsm.TextFSM(template2)
        result2 = fsm2.ParseText(resp2)
        print(result2) # Раскомментируй, если хочешь посмотреть результат парсинга
        DUT2_version=result2[0][2]
        DUT2_uptime=result2[0][3]
        conn2.send('quit\r')
        conn2.close()

        conn3 = Telnet()
        acc3 = Account(DUT3.login, DUT3.password)
        conn3.connect(DUT3.host_ip)
        conn3.login(acc3)
        conn3.set_prompt('#')
        conn3.execute('show system') 
        resp3 = conn3.response
# C помощью магии модуля textFSM сравниваем вывод команды 'show firmware' c шаблоном в файле parse_show_privilege.txt 
        template3 = open('./templates/parse_show_system_after_upgrade.txt')
        fsm3 = textfsm.TextFSM(template3)
        result3 = fsm3.ParseText(resp3)
        print(result3) # Раскомментируй, если хочешь посмотреть результат парсинга
        DUT3_version=result3[0][2]
        DUT3_uptime=result3[0][3]
        conn3.send('quit\r')
        conn3.close()
        assert_that(DUT1_uptime!='',"Параметр uptime после обновления ПО у %s не соответсвует шаблону"%DUT1.hostname)
        assert_that(DUT1_version==DUT1_soft_ver,"Software version после обновления у %s не соответсвует target_version -%s"%(DUT1.hostname,DUT1_soft_ver))
        assert_that(DUT2_uptime!='',"Параметр uptime после обновления ПО у %s не соответсвует шаблону"%DUT2.hostname)
        assert_that(DUT2_version==DUT2_soft_ver,"Software version после обновления у %s не соответсвует target_version -%s"%(DUT2.hostname,DUT2_soft_ver))
        assert_that(DUT3_uptime!='',"Параметр uptime после обновления ПО у %s не соответсвует шаблону"%DUT3.hostname)
        assert_that(DUT3_version==DUT3_soft_ver,"Software version после обновления у %s не соответсвует target_version -%s"%(DUT3.hostname,DUT3_soft_ver))
    except SystemExit as e:
        exit_message=str(e)
        print(exit_message)
        assert_that(exit_message=="Версия уже используется","Произошел странный system exit")

