from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.6:Функциональное тестирование свичинга сервиса при работе RSVP-TE E2E protection')
@allure.title('Автоматическое переключение сервисного трафика RSVP LSP main->backup->main при включенном E2E protection')
@pytest.mark.part14_6
@pytest.mark.check_auto_switchover_e2e_protection
@pytest.mark.dependency(depends=["load_config146_dut1","load_config146_dut2","load_config146_dut3","load_config146_dut4"],scope='session')
@pytest.mark.parametrize('ip, login, password', [(DUT3['host_ip'], DUT3['login'], DUT3['password'])])
def test_auto_switchover_e2e_protection_part14_6 (ip, login, password): 
    allure.attach.file('./network-schemes/part14_6_check_l2vpn_traffic_auto_switchover_between_main_and_backup_rsvp_lsp.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
#    allure.attach.file('./network-schemes/part14_5_show_mpls_rsvp_tunnels_lsp_e2e_cmd.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('config')
    conn.execute('mpls rsvp')
    conn.execute('no backup disable never') # Эту команду надо удалить т.к. с ней автоматическое переключеие main->backup->main работать не будет
    conn.execute('commit')
    conn.execute('end')
    result_loss=0
    wait_timer=20 # Время которое ждем для обновления счётчиков на интерфейсах
    cmd=('show interfaces  utilization | incl "Inter|bu"')
    with concurrent.futures.ThreadPoolExecutor() as executor:

        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'70000', DUT4['login'], DUT4['password'], '192.168.41.2', 'vrf41', result_loss)        
        time.sleep(wait_timer)
        conn.execute(cmd)
        resp=conn.response
#       print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces  utilization | incl bu'
        allure.attach(resp, 'Шаг1. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces  utilization | incl bu' c шаблоном в файле parse_show_int_util_bu.txt 
        template = open('./templates/parse_show_int_util_bu.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
#        result = fsm.ParseText(resp)
        bu1_sent=processed_result[0]['bu1_sent']
        bu1_recv=processed_result[0]['bu1_recv']
        bu2_sent=processed_result[0]['bu2_sent']
        bu2_recv=processed_result[0]['bu2_recv']
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
#        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    assert_that(int(packet_loss)==0,"Шаг1.Обнаружены потери пакетов в bridge домене BD-TEST между СЕ устройствами. Они составили %s %%"%packet_loss)
    assert_that((abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100)<=10, "Шаг1.Загрузка интерфейса bu2 во входящем и bu1 в исходящем направлениях отличается более чем на 10%% и разница составила %d%%"%(abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100))
    assert_that(int(bu1_sent)!=0 and int(bu2_recv)!=0,"Шаг1.Загрузка интерфейсов bu1 и bu2 должна быть не нулевой")
# Шаг3. Отправляем в shutdown интерфейс bu2 на atAR1
    conn1 = Telnet()
    acc1 = Account(DUT1['login'], DUT1['password'])
    conn1.connect(DUT1['host_ip'])
    conn1.login(acc1)
    conn1.set_prompt('#')
    conn1.execute('config')
    conn1.execute('interface bundle-ether 2')
    conn1.execute('shutdown')
    conn1.execute('commit')
    print('\rШаг3. atAR1:Отправили интерфейс bu2 в shutdown\r')

# Вновь проверяем загрузки интефейсов bu1 и bu2 на atDR1.	
    with concurrent.futures.ThreadPoolExecutor() as executor:

#        future = executor.submit(generate_trafic_from_labs01, DUT5['host_ip'],'1000','1496' , DUT5['login'] , DUT5['password'] , '172.16.70.1', result_loss)
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'70000', DUT4['login'], DUT4['password'], '192.168.41.2', 'vrf41', result_loss) 
        time.sleep(wait_timer)
        conn.execute(cmd)
        resp=conn.response
#       print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces  utilization | incl bu'
        resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
        allure.attach(resp_output[2], 'Шаг3. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces  utilization | incl bu' c шаблоном в файле parse_show_int_util_bu.txt 
        template = open('./templates/parse_show_int_util_bu.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
#        result = fsm.ParseText(resp)
        bu1_sent=processed_result[0]['bu1_sent']
        bu1_recv=processed_result[0]['bu1_recv']
        bu2_sent=processed_result[0]['bu2_sent']
        bu2_recv=processed_result[0]['bu2_recv']
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
#        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
# Шаг5. Поднимаем интерфейс bu2 на atAR1 (no shutdown)  
    conn1.execute('no shutdown')
    conn1.execute('commit')  # Восстановим конфигу еще на шаге 3 чтобы в случае срабатывания assert-a конфига была первоначальной
    print('\rШаг4. atAR1:Отправили интерфейс bu2 в shutdown\r')
    assert_that(int(packet_loss)==0,"Шаг3.Обнаружены потери пакетов в bridge домене BD-TEST между СЕ устройствами. Они составили %s %%"%packet_loss)
    assert_that((abs(int(bu2_sent)-int(bu2_recv))/int(bu2_sent)*100)<=10, "Шаг3.Разница в загрузке интерфейса bu2 во входящем и исходящем направлениях больше чем на 10%% и составила %d%%"%(abs(int(bu2_sent)-int(bu2_recv))/int(bu2_sent)*100))
    assert_that(int(bu2_sent)!=0 and int(bu2_recv)!=0,"Шаг3.Загрузка интерфейса bu2 должна быть не нулевой")

    time.sleep(220) # Подождем пока atDR1 по таймеру переключит трафик с backup на main
#  Вновь проверяем загрузки интефейсов bu1 и bu2 на atDR1.
    with concurrent.futures.ThreadPoolExecutor() as executor:

#        future = executor.submit(generate_trafic_from_labs01, DUT5['host_ip'],'1000','1496' , DUT5['login'] , DUT5['password'] , '172.16.70.1', result_loss)
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'70000', DUT4['login'], DUT4['password'], '192.168.41.2', 'vrf41', result_loss)
        time.sleep(wait_timer)

        conn.execute(cmd)
        resp=conn.response
#       print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces  utilization | incl bu'
        
        allure.attach(resp, 'Шаг5. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces  utilization | incl bu' c шаблоном в файле parse_show_int_util_bu.txt 
        template = open('./templates/parse_show_int_util_bu.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
#        result = fsm.ParseText(resp)
        bu1_sent=processed_result[0]['bu1_sent']
        bu1_recv=processed_result[0]['bu1_recv']
        bu2_sent=processed_result[0]['bu2_sent']
        bu2_recv=processed_result[0]['bu2_recv']
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
#        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.execute('configure')
    conn.execute('mpls rsvp backup disable never')
    conn.execute('commit')
    assert_that(int(packet_loss)==0,"Шаг5.Обнаружены потери пакетов в bridge домене BD-TEST между СЕ устройствами. Они составили %s %%"%packet_loss)
    assert_that((abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100)<=10, "Шаг5.Загрузка интерфейса bu2 во входящем и bu1 в исходящем направлениях отличается более чем на 10%% и разница составила %d%%"%(abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100))
    assert_that(int(bu1_sent)!=0 and int(bu2_recv)!=0,"Шаг5.Загрузка интерфейсов bu1 и bu2 должна быть не нулевой")
    conn.execute('end')
    conn.send('quit\r')
    conn.close()
