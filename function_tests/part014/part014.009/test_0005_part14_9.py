from conftest import *

@pytest.fixture(scope='function')
def restore_config_after_test5_part14_9(ip,login, password): # Передаём в фикстуру параметры: ip - адрес куда подключаемся; hostname -имя узла куда подключаемся
    yield
    conn = Telnet()
    acc = Account(login, password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('config')
    conn.execute('interface te0/0/11.352')
    conn.execute('no shutdown')
    conn.execute('commit')


@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.9:Функциональное тестирование MPLS TE FRR node-protection')
@allure.title('Проверка свичинга ICMP пакетов при срабатывании TE FRR Facility protection NNHOP на atAR1:')
@pytest.mark.part14_9
#@pytest.mark.timeout(timeout=180, method='signal')
@pytest.mark.switching_L3VPN_TE_FRR_Faclity_NNHOP_protection
@pytest.mark.dependency(depends=["load_config149_dut1","load_config149_dut2","load_config149_dut3","load_config149_dut6"],scope='session')
@pytest.mark.parametrize('ip , login, password, int1', [(DUT1['host_ip'] , DUT1['login'] , DUT1['password'] , 'te0/0/11.352')])
@pytest.mark.usefixtures('restore_config_after_test5_part14_9')
def test_switching_L3VPN_TE_FRR_Faclity_NNHOP_protection_atAR1_part14_9 (ip, login, password, int1):   
# В данном тесте запустим пинг между 192.168.41.2 (CE1) и 192.168.42.2 (CE2) а затем вызывовем переключение TE FRR protection. Т.е. защищаемый RSVP LSP to_atAR2@atDR1_to_atAR2-lsp1 будет
# перенаправлен в защитный RSVP LSP bypass  

    result_loss=0 # Данная переменная нужна для процедуры generate_uu_trafic_from_labr02
    allure.attach.file('./network-schemes/part14_9_L3VPN_TE_FRR_Facility_NNHOP_protection_atAR1.png','Схема Теста', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(DUT3['login'] , DUT3['password'])
    allure.step('Подключаемся к atDR1  по протоколу telnet')
    conn.connect(DUT3['host_ip'])
    conn.login(acc)
    conn.set_prompt('#') 

    conn1 = Telnet()
    acc1 = Account(login , password)
    allure.step('Подключаемся к atAR1  по протоколу telnet')
    conn1.connect(ip)
    conn1.login(acc1)


# Шаг1. Начинаем проверку по переключению трафика путем отправки в shutdown интерфейса bu1 на atAR1     
    conn.execute('terminal datadump ')   
    cmd='show mpls rsvp lsps tunnel to_atAR2'
    conn.execute(cmd)
    resp = conn.response 
    allure.attach(resp, 'Шаг1. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    cmd1='show mpls rsvp lsps tunnel bypass'
    conn1.execute(cmd1)
    resp1 = conn1.response 
    allure.attach(resp1, 'Шаг1. Вывод команды %s'%cmd1, attachment_type=allure.attachment_type.TEXT)
    time.sleep(15)  # Подождем пока появится маршрутная информация на CE1 о префиксах CE2. Часто тест заканчивается по причине Network Unreachable  
# Запустим генерацию трафика с ESR-a путем запуска функции generate_uu_trafic_from_labr02 данный способ позволяет получить результат из функции в родительский thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
#        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'40027' , DUT4['login'] , DUT4['password'] , '192.168.42.2', 'vrf41' ,result_loss)
        future = executor.submit(generate_slow_trafic_from_labr02, DUT4['host_ip'],'100' , DUT4['login'] , DUT4['password'] , '192.168.42.2', 'vrf41',200 ,result_loss)
        conn1.execute('config')
        cmd1=('interface %s'%int1)
        conn1.execute(cmd1)
        conn1.execute('shutdown')
        time.sleep(5) # Подождем пока трфик генерируется в параллельном потоке через защищаемый RSVP LSP
        conn1.execute('commit') # После этого ожидаем что трафик переключится в bypass RSVP LSP
        conn1.execute('end')
        print('Шаг1. Выполнили shutdown интерфейса %s на %s\r'%(int1,DUT1['host_ip']))
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
        packet_sent = param_list[1]
        packet_recv = param_list[2]
        net_unreach = param_list[3]
    if (int(packet_sent) != int(packet_recv)):
        final_result=('Обнаружены потери пакетов (%s %%) между CE1 и CE2. Отправлено - %s пакетов, получено - %s пакетов'%(packet_loss,packet_sent,packet_recv))
        allure.attach(final_result,'Результат НЕ успешного теста на Шаге 1:')
    elif (int(packet_sent) == int(packet_recv)):
        final_result=('Потери пакетов между CE1 и CE2 НЕ обнаружены. Отправлено - %s пакетов, получено - %s пакетов'%(packet_sent,packet_recv))
        allure.attach(final_result,'Результат успешного теста на Шаге 1:')


#    assert_that(int(packet_sent) == int(packet_recv),"Шаг1. Обнаружены потери пакетов (%s %%) между CE1 и CE2. Отправлено - %s пакетов, получено - %s пакетов"%(packet_loss,packet_sent,packet_recv))


# Шаг2. Анализируем вывод команды show mpls rsvp lsp tunnel to_atAR2 после перевода защищаемого туннеля в bypass
    
    conn.execute(cmd)
    resp = conn.response 
    allure.attach(resp, 'Шаг2. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    print(processed_result)
    tun_name=processed_result[0]['tun_name']
    tun_id_step2=processed_result[0]['tun_id']
    lsp_name=processed_result[0]['lsp_name']
    lsp_signal_name=processed_result[0]['lsp_signal_name']
    lsp_id_step2=processed_result[0]['lsp_id']
    lsp_src=processed_result[0]['lsp_src']
    lsp_dst=processed_result[0]['lsp_dst']
    lsp_state=processed_result[0]['lsp_state']
    plr_id=processed_result[0]['plr_id']
    lsp_signal_int=processed_result[0]['lsp_signal_int']
    hop0=processed_result[0]['hop_number']
    hop0_incoming_ERO=processed_result[0]['incoming_ERO']
    hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
    hop1=processed_result[1]['hop_number']
    hop1_incoming_ERO=processed_result[1]['incoming_ERO']
    hop1_outgoing_ERO=processed_result[1]['outgoing_ERO']
    hop2=processed_result[2]['hop_number']
    hop2_incoming_ERO=processed_result[2]['incoming_ERO']
    hop2_outgoing_ERO=processed_result[2]['outgoing_ERO']
    hop3=processed_result[3]['hop_number']
    hop3_incoming_ERO=processed_result[3]['incoming_ERO']
    hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
    assert_that(lsp_signal_int=='Bundle-ether1',"Шаг2. В выводе команды %s параметр Signalling interface не равен ожидаемому значению Bundle-ether1, а равен - %s"%(cmd,lsp_signal_int))
    assert_that(plr_id=='1.0.0.3',"Шаг2. В выводе команды %s параметр PLR (LSP repaired at) не равен ожидаемому значению 1.0.0.3, а равен - %s"%(cmd,plr_id))

    assert_that(tun_name=='to_atAR2',"Шаг2. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
    assert_that(lsp_name=='lsp1',"Шаг2. Имя LSP в выводе команды не соответствует ожидаемому lsp1, вместо этого значение равно %s"%lsp_name)
    assert_that(lsp_signal_name=='to_atAR2@lsp1',"Шаг2. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR2@lsp1, вместо этого значение равно %s"%lsp_signal_name)
    assert_that(lsp_src=='1.0.0.1',"Шаг2. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.1, вместо этого значение равно %s"%lsp_src)
    assert_that(lsp_dst=='1.0.0.2',"Шаг2. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_dst)
    assert_that(lsp_state=='up',"Шаг2. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)

# Шаг3. Проверяем работспособность после возвращения на исходный путь
# Поднимаем интерфейс bu1 и ждем пока вернётся трафик обратно на исходный путь обозначенный синим пунктиром на схеме.

# Запустим генерацию трафика с ESR-a путем запуска функции generate_uu_trafic_from_labr02 данный способ позволяет получить результат из функции в родительский thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_slow_trafic_from_labr02, DUT4['host_ip'],'1000' , DUT4['login'] , DUT4['password'] , '192.168.42.2', 'vrf41',200 ,result_loss)
        conn1.execute('config')
        cmd1=('interface %s'%int1)
        conn1.execute(cmd1)
        conn1.execute('no shutdown')
        time.sleep(5) # Подождем пока трфик генерируется в параллельном потоке через защищаемый RSVP LSP
        conn1.execute('commit') # После этого ожидаем что трафик вернётся на исходный путь т.е. уйдет из bypass RSVP LSP
        print('Шаг3. Выполнили no shutdown интерфейса %s на %s\r'%(int1,DUT1['host_ip']))
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
        packet_sent = param_list[1]
        packet_recv = param_list[2]
        net_unreach = param_list[3]
    if (int(packet_sent) != int(packet_recv)):
        final_result=('Обнаружены потери пакетов (%s %%) между CE1 и CE2. Отправлено - %s пакетов, получено - %s пакетов'%(packet_loss,packet_sent,packet_recv))
        allure.attach(final_result,'Результат НЕ успешного теста на Шаге 3:')
    elif (int(packet_sent) == int(packet_recv)):
        final_result=('Потери пакетов между CE1 и CE2 НЕ обнаружены. Отправлено - %s пакетов, получено - %s пакетов'%(packet_sent,packet_recv))
        allure.attach(final_result,'Результат успешного теста на Шаге 3:')
    
#    assert_that(int(packet_sent) == int(packet_recv),"Шаг3. Обнаружены потери пакетов (%s %%) между CE1 и CE2. Отправлено - %s пакетов, получено - %s пакетов"%(packet_loss,packet_sent,packet_recv))



# Шаг4. Анализируем вывод команды show mpls rsvp lsp tunnel to_atAR2 после ухода из bypass туннеля
    
    conn.execute(cmd)
    resp = conn.response 
    allure.attach(resp, 'Шаг4. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    print(processed_result)
    tun_name=processed_result[0]['tun_name']
    tun_id_step4=processed_result[0]['tun_id']
    lsp_name=processed_result[0]['lsp_name']
    lsp_signal_name=processed_result[0]['lsp_signal_name']
    lsp_id_step4=processed_result[0]['lsp_id']
    lsp_src=processed_result[0]['lsp_src']
    lsp_dst=processed_result[0]['lsp_dst']
    lsp_state=processed_result[0]['lsp_state']
    plr_id=processed_result[0]['plr_id']
    lsp_signal_int=processed_result[0]['lsp_signal_int']
    hop0=processed_result[0]['hop_number']
    hop0_incoming_ERO=processed_result[0]['incoming_ERO']
    hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
    hop1=processed_result[1]['hop_number']
    hop1_incoming_ERO=processed_result[1]['incoming_ERO']
    hop1_outgoing_ERO=processed_result[1]['outgoing_ERO']
    hop2=processed_result[2]['hop_number']
    hop2_incoming_ERO=processed_result[2]['incoming_ERO']
    hop2_outgoing_ERO=processed_result[2]['outgoing_ERO']
    hop3=processed_result[3]['hop_number']
    hop3_incoming_ERO=processed_result[3]['incoming_ERO']
    hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
    assert_that(lsp_signal_int=='Bundle-ether1',"Шаг4. В выводе команды %s параметр Signalling interface не равен ожидаемому значению Bundle-ether1, а равен - %s"%(cmd,lsp_signal_int))
    assert_that(plr_id=='',"Шаг4. В выводе команды %s параметр PLR (LSP repaired at) обнаружен и равен - %s, хотя его быть не должно"%(cmd,plr_id))

    assert_that(tun_name=='to_atAR2',"Шаг2. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
    assert_that(lsp_name=='lsp1',"Шаг2. Имя LSP в выводе команды не соответствует ожидаемому lsp1, вместо этого значение равно %s"%lsp_name)
    assert_that(lsp_signal_name=='to_atAR2@lsp1',"Шаг2. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR2@lsp1, вместо этого значение равно %s"%lsp_signal_name)
    assert_that(lsp_src=='1.0.0.1',"Шаг2. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.1, вместо этого значение равно %s"%lsp_src)
    assert_that(lsp_dst=='1.0.0.2',"Шаг2. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_dst)
    assert_that(lsp_state=='up',"Шаг2. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
