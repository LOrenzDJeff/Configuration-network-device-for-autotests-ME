from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.4:Функциональное тестирование L2VPN over RSVP-TE')
@allure.title('Проверка передачи сервисного L2VPN трафика через RSVP LSP TE туннелей')
@pytest.mark.part14_4
@pytest.mark.l2vpn_over_rsvp_lsp
@pytest.mark.dependency(depends=["load_config144_dut1","load_config144_dut2","load_config144_dut3","load_config144_dut4"],scope='session')
@pytest.mark.parametrize('ip, login, password', [(DUT1['host_ip'], DUT1['login'], DUT1['password'])])
def test_switching_l2vpn_over_rsvp_lsp_part14_4 (ip, login, password): 
    allure.attach.file('./network-schemes/part14_4_ping_l2vpn_over_rsvp_lsp.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    interval=20
    conn.execute('terminal datadump')
    cmd=('ping 172.16.70.2 vrf CE1 count 10')
    time.sleep(5) # Задержка для того чтобы  L2VPN успел подняться
    conn.execute(cmd)
    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'ping 172.16.70.2 vrf CE1'
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_ping_from_me.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга    
    success_percent=processed_result[0]['success_rate']
    if (float(success_percent)<100):
        print("\rС первого раза пинг был не успешен. %% успешности - %s %%. Ждем %d секунд\r"%(success_percent, interval))
        time.sleep(interval)
        conn.execute(cmd)  # Проверяем связность второй раз
        resp=conn.response
        allure.attach(resp, 'Вывод второй команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
        template = open('./templates/parse_ping_from_me.txt') 
        fsm = textfsm.TextFSM(template)
        resp=conn.response
        processed_result=fsm.ParseTextToDicts(resp)
#       print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга    
        success_percent=processed_result[0]['success_rate']
        if (float(success_percent)<100):
            print("\rСо второго раза пинг был не успешен. %% успешности - %s %%. Ждем %d секунд\r"%(success_percent, 2*interval))
            time.sleep(2*interval)
            conn.execute(cmd)  # Проверяем связность третий раз
            resp=conn.response
            allure.attach(resp, 'Вывод третьей команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
            template = open('./templates/parse_ping_from_me.txt') 
            fsm = textfsm.TextFSM(template)
            processed_result=fsm.ParseTextToDicts(resp)
#           print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга    
            success_percent=processed_result[0]['success_rate']
            if (float(success_percent)<100):
                print("\rС третьего раза пинг был не успешен. %% успешности - %s %%. Ждем %d секунд\r"%(success_percent, 3*interval))
                time.sleep(3*interval)
                conn.execute(cmd)  # Проверяем связность четвёртый раз
                resp=conn.response
                allure.attach(resp, 'Вывод четвертой команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
                template = open('./templates/parse_ping_from_me.txt') 
                fsm = textfsm.TextFSM(template)
                processed_result=fsm.ParseTextToDicts(resp)
    #           print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга    
                success_percent=processed_result[0]['success_rate']

    conn.send('quit\r')
    conn.close()
    assert_that(float(success_percent)>=90,"В выводе четвертой команды %s наблюдаются потери пакетов. Успешный обмен ICMP пакетами - %s %%"%(cmd,success_percent))

