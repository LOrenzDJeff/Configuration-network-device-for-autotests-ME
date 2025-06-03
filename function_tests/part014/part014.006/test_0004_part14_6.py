from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.6:Функциональное тестирование свичинга сервиса при работе RSVP-TE E2E protection')
@allure.title('Ручное переключение сервисного трафика RSVP LSP main->backup->main при включенном E2E protection')
@pytest.mark.part14_6
@pytest.mark.check_manual_switchover_e2e_protection
@pytest.mark.dependency(depends=["load_config146_dut1","load_config146_dut2","load_config146_dut3","load_config146_dut4"],scope='session')
@pytest.mark.parametrize('ip, login, password', [(DUT3['host_ip'], DUT3['login'], DUT3['password'])])
def test_manual_switchover_e2e_protection_part14_6 (ip, login, password): 
    allure.attach.file('./network-schemes/part14_6_check_l2vpn_traffic_manual_switchover_between_main_and_backup_rsvp_lsp.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
#    allure.attach.file('./network-schemes/part14_5_show_mpls_rsvp_tunnels_lsp_e2e_cmd.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    result_loss=0
    wait_timer=20 # Время которое ждем для обновления счётчиков на интерфейсах
    conn4 = Telnet()
    acc4 = Account(DUT4['login'] , DUT4['password'])
    conn4.connect(DUT4['host_ip'])
    conn4.login(acc4)
    conn4.set_prompt('#')

# Запустим процедуру пингов между СЕ-устройствами чтобы дождаться когда связность между ними появится.

    cmd='ping vrf vrf41 192.168.41.2 packets 10'
    packet_loss=0
    resp=''
    return_list=four_attempts_ping_from_labr02(conn4,cmd,10,packet_loss,resp)
    result1_loss=return_list[0]
    resp=return_list[1]
    resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Шаг0. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    assert_that(int(result1_loss)<=10,"Шаг0. Обнаружены потери пакетов между CE2 и CE1 в размере %s %%"%result1_loss)
# Только после того как связность появилась имеет смысл приступать к тестироованию функционала E2E Protection

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
        result = fsm.ParseText(resp)
        bu1_sent=result[0][0]
        bu1_recv=result[0][1]
        bu2_sent=result[0][2]
        bu2_recv=result[0][3]
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
#        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    assert_that(int(packet_loss)==0,"Шаг1.Обнаружены потери пакетов в bridge домене BD-TEST между СЕ устройствами. Они составили %s %%"%packet_loss)
    assert_that((abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100)<=10, "Шаг1.Загрузка интерфейса bu2 во входящем и bu1 в исходящем направлениях отличается более чем на 10%% и разница составила %d%%"%(abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100))
    assert_that(int(bu1_sent)!=0,"Шаг1.Загрузка интерфейса bu1 в исходящем направлении должна быть не нулевой")
    assert_that(int(bu2_recv)!=0,"Шаг1.Загрузка интерфейса bu2 во входящем направлении должна быть не нулевой")
# Шаг2. Выполняем ручное переключение трафика с to_atAR2@main на to_atAR2@backup
    conn.execute('mpls rsvp switchover tunnel to_atAR2 backup')
    print("\rШаг2. Выполнили ручное переключение main->backup\r")
    with concurrent.futures.ThreadPoolExecutor() as executor:

#        future = executor.submit(generate_trafic_from_labs01, DUT5['host_ip'],'1000','1496' , DUT5['login'] , DUT5['password'] , '172.16.70.1', result_loss)
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'70000', DUT4['login'] , DUT4['password'], '192.168.41.2', 'vrf41', result_loss)        
        time.sleep(wait_timer)
        conn.execute(cmd)
        resp=conn.response
#       print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces  utilization | incl bu'
        allure.attach(resp, 'Шаг2. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces  utilization | incl bu' c шаблоном в файле parse_show_int_util_bu.txt 
        template = open('./templates/parse_show_int_util_bu.txt') 
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
        bu1_sent=result[0][0]
        bu1_recv=result[0][1]
        bu2_sent=result[0][2]
        bu2_recv=result[0][3]
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
#        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.execute('mpls rsvp switchover tunnel to_atAR2 main') # Перед assert-ами вернем трафик обратно на main LSP. Иначе, если assert-ы сработают, для последующих тестов могут быть последствия
    print("\rШаг4. Выполнили ручное переключение backup->main\r")
    assert_that(int(packet_loss)==0,"Шаг3.Обнаружены потери пакетов в bridge домене BD-TEST между СЕ устройствами. Они составили %s %%"%packet_loss)
    assert_that((abs(int(bu2_sent)-int(bu2_recv))/int(bu2_sent)*100)<=10, "Шаг3.Разница в загрузке интерфейса bu2 в исходящем и входящем направлении больше чем на 10%% и составила %d%%"%(abs(int(bu2_sent)-int(bu2_recv))/int(bu2_sent)*100))
    assert_that(int(bu2_sent)!=0 and int(bu2_recv)!=0,"Шаг3.Загрузка интерфейса bu2 должна быть не нулевой")
# Шаг3.  Выполняем обратное ручное переключение трафика с to_atAR2@backup на to_atAR2@main   
#    conn.execute('mpls rsvp switchover tunnel to_atAR2 main') # Закоментировал переключение трафика здесь и перенёс его  чуть выше т.к. при срабатывании assert-а выше, следующий тест (авто свичовер трафика) уже не проходит
#  Вновь проверяем загрузки интефейсов bu1 и bu2 на atDR1.
    with concurrent.futures.ThreadPoolExecutor() as executor:

        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'70000', DUT4['login'] , DUT4['password'], '192.168.41.2', 'vrf41', result_loss)
        time.sleep(wait_timer)
        conn.execute(cmd)
        resp=conn.response
#       print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces  utilization | incl bu'
        allure.attach(resp, 'Шаг3. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces  utilization | incl bu' c шаблоном в файле parse_show_int_util_bu.txt 
        template = open('./templates/parse_show_int_util_bu.txt') 
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
        bu1_sent=result[0][0]
        bu1_recv=result[0][1]
        bu2_sent=result[0][2]
        bu2_recv=result[0][3]
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
#        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    assert_that(int(packet_loss)==0,"Шаг5.Обнаружены потери пакетов в bridge домене BD-TEST между СЕ устройствами. Они составили %s %%"%packet_loss)
    assert_that((abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100)<=10, "Шаг3.Загрузка интерфейсов bu2 во входящем и bu1 в исходящем направлениях отличается более чем на 10%% и разница составила %d%%"%(abs(int(bu1_sent)-int(bu2_recv))/int(bu1_sent)*100))
    assert_that(int(bu1_sent)!=0 and int(bu1_recv)!=0,"Шаг5.Загрузка интерфейсов bu1 и bu2 должна быть не нулевой")
    conn.send('quit\r')
    conn.close()
