from conftest import *

#debug_cmd_list=['debug pp-mgr cmd','debug pp-mgr general','debug pp-mgr arp','debug pp-mgr bfd','debug pp-mgr egress']

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.11:Функциональное тестирование MPLS TE AutoBandwidth')
@allure.title('Проверка перестроения RSVP LSP при изменении объема передаваемого через него трафика')
@pytest.mark.part14_11
@pytest.mark.mpls_te_autobandwidth_test1
@pytest.mark.parametrize('ip , hostname , login, password, tun_name', [(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'],'to_atAR2'),(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'],'to_atAR1')])
#@pytest.mark.parametrize('ip , hostname , login, password, tun_name', [(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'],'to_atAR1')])
def test_mpls_te_autobandwidth_test1_part14_11 (ip, hostname, login, password, tun_name): 
    if hostname==DUT1['hostname']:
        allure.attach.file('./network-schemes/part14_11_mpls_te_ab_atAR1_test1.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
        docker_compose_file='part14_11_atAR1_docker-compose.yaml'
        ip_iperf_server='192.168.74.1'
    if hostname==DUT2['hostname']:
        allure.attach.file('./network-schemes/part14_11_mpls_te_ab_atAR2_test1.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
        docker_compose_file='part14_11_atAR2_docker-compose.yaml'
        ip_iperf_server='192.168.73.1'
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
# Шаг1. Проверяем что RSVP LSP to_atAR2@atAR1_to_atAR2 построился кратчайшим путем без трафика проходящего через него
    conn.execute('terminal datadump')
    cmd=('show mpls rsvp lsp tunnel %s'%tun_name)

# В итеративном формате будем ждать пока поднимется RSVP LSP tunnel $tun_name
    i=0
    while i <= 10:
        conn.execute(cmd)
        resp=conn.response
        print('Итерация - %s %s\r'%(i, cmd))
        index_str=resp.find("State:")
        if index_str!=-1:
            i=10
        else:
            time.sleep(15) # Ждем пока RSVP LSP поднимутся
    
        i +=1


    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'
    allure.attach(resp, 'Шаг1. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга

    if hostname == DUT1['hostname']:
        tun_name=processed_result[0]['tun_name']
        assert_that(tun_name=='to_atAR2',"Шаг1. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result[0]['tun_id']
        assert_that(tun_id!='',"Шаг1. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_name=processed_result[0]['lsp_name']
        assert_that(lsp_name=='atAR1_to_atAR2',"Шаг1. Имя LSP в выводе команды не соответствует ожидаемому atAR1_to_atAR2, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_atAR2@atAR1_to_atAR2',"Шаг1. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR2@atAR1_to_atAR2, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id1=processed_result[0]['lsp_id']
        assert_that(lsp_id1!='',"Шаг1. ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_src=processed_result[0]['lsp_src']
        assert_that(lsp_src=='10.0.19.4',"Шаг1. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.4, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result[0]['lsp_dst']
        assert_that(lsp_dst=='10.0.19.2',"Шаг1. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.2, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result[0]['lsp_state']
        assert_that(lsp_state=='up',"Шаг1. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Tengigabitethernet0/0/18.200',"Шаг1. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/18.200, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.54.6/32' and hop0_outgoing_ERO=='192.168.54.5/32',"Шаг1. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.54.6/32,192.168.54.5/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
        hop1=processed_result[1]['hop_number']
        hop1_incoming_ERO=processed_result[1]['incoming_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.54.5/32',"Шаг1. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.54.5/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))


    if hostname == DUT2['hostname']:
        tun_name=processed_result[0]['tun_name']
        assert_that(tun_name=='to_atAR1',"Шаг1. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result[0]['tun_id']
        assert_that(tun_id!='',"Шаг1. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_name=processed_result[0]['lsp_name']
        assert_that(lsp_name=='atAR2_to_atAR1',"Шаг1. Имя LSP в выводе команды не соответствует ожидаемому atAR2_to_atAR1, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_atAR1@atAR2_to_atAR1',"Шаг1. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR1@atAR2_to_atAR1, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id1=processed_result[0]['lsp_id']
        assert_that(lsp_id1!='',"Шаг1. ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_src=processed_result[0]['lsp_src']
        assert_that(lsp_src=='10.0.19.2',"Шаг1. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.2, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result[0]['lsp_dst']
        assert_that(lsp_dst=='10.0.19.4',"Шаг1. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.4, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result[0]['lsp_state']
        assert_that(lsp_state=='up',"Шаг1. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Tengigabitethernet0/0/15.200',"Шаг1. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/15.200, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.54.5/32' and hop0_outgoing_ERO=='192.168.54.6/32',"Шаг1. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.54.5/32,192.168.54.6/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
        hop1=processed_result[1]['hop_number']
        hop1_incoming_ERO=processed_result[1]['incoming_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.54.6/32',"Шаг1. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.54.6/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))

# Шаг2. Запускаем iperf c полосой пропускания 6 Mbps и через 300 сек смотрим как перестроился RSVP LSP
    result_loss=0
    packet_send=0
    packet_recv=0
    with concurrent.futures.ThreadPoolExecutor() as executor:        
        future = executor.submit(start_docker_iperf3_server_client, ip_iperf_server, 300, '6M',  result_loss, packet_send, packet_recv,docker_compose_file)
        time.sleep(120)
        cmd1='show mpls rsvp lsp autobandwidth'
        conn.execute(cmd1)
        resp=conn.response
        allure.attach(resp, 'Шаг2.Вывод команды %s'%cmd1, attachment_type=allure.attachment_type.TEXT)
    process_list = future.result()

# Шаг2. Проверяем как пересторился $tun_name после генерации 6 Mbps трафика и истечения 300 секунд
    conn.execute(cmd)
    print('Шаг2. Проверяем как перестроился туннель %s\r'%tun_name)
    resp2=conn.response
    allure.attach(resp2, 'Шаг2.Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
#    print(resp)    
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm2 = textfsm.TextFSM(template)
    processed_result2 = fsm2.ParseTextToDicts(resp2)
#    print(processed_result2)   # Раскомментируй, если хочешь посмотреть результат парсинга



    if hostname == DUT1['hostname']:
        tun_name=processed_result2[0]['tun_name']
        assert_that(tun_name=='to_atAR2',"Шаг2. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result2[0]['tun_id']
        assert_that(tun_id!='',"Шаг2. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_name=processed_result2[0]['lsp_name']
        assert_that(lsp_name=='atAR1_to_atAR2',"Шаг2. Имя LSP в выводе команды не соответствует ожидаемому atAR1_to_atAR2, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result2[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_atAR2@atAR1_to_atAR2',"Шаг1. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR2@atAR1_to_atAR2, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id2=processed_result2[0]['lsp_id']
        assert_that(lsp_id2!=lsp_id1,"Шаг2. ID RSVP LSP в выводе команды равен ID на шаге 1, а должен измениться")
        lsp_src=processed_result2[0]['lsp_src']
        assert_that(lsp_src=='10.0.19.4',"Шаг2. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.4, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result2[0]['lsp_dst']
        assert_that(lsp_dst=='10.0.19.2',"Шаг2. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.2, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result2[0]['lsp_state']
        assert_that(lsp_state=='up',"Шаг2. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result2[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Tengigabitethernet0/0/17.364',"Шаг2. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/17.364, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result2[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result2[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.54.2/32' and hop0_outgoing_ERO=='192.168.54.1/32',"Шаг2. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.54.2/32,192.168.54.1/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))

        hop1=processed_result2[1]['hop_number']
        hop1_incoming_ERO=processed_result2[1]['incoming_ERO']
        hop1_outgoing_ERO=processed_result2[1]['outgoing_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.54.1/32' and hop1_outgoing_ERO=='192.168.54.50/32',"Шаг2. Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.54.1/32,192.168.54.50/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))

        hop2=processed_result2[2]['hop_number']
        hop2_incoming_ERO=processed_result2[2]['incoming_ERO']
        hop2_outgoing_ERO=processed_result2[2]['outgoing_ERO']
        assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.54.50/32' and hop2_outgoing_ERO=='192.168.54.49/32',"Шаг2. Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.54.50/32,192.168.54.49/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))


        hop3=processed_result2[3]['hop_number']
        hop3_incoming_ERO=processed_result2[3]['incoming_ERO']
        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.54.49/32',"Шаг2. Один или несколько параметров из hop3, hop3_incoming_ERO,  не равен ожидаемым значениям hop3, 192.168.54.49/32 вместо этого получены значения %s, %s"%(hop3,hop3_incoming_ERO))


    if hostname == DUT2['hostname']:
        tun_name=processed_result2[0]['tun_name']
        assert_that(tun_name=='to_atAR1',"Шаг2. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result2[0]['tun_id']
        assert_that(tun_id!='',"Шаг2. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_name=processed_result2[0]['lsp_name']
        assert_that(lsp_name=='atAR2_to_atAR1',"Шаг2. Имя LSP в выводе команды не соответствует ожидаемому atAR2_to_atAR1, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result2[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_atAR1@atAR2_to_atAR1',"Шаг2. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR1@atAR2_to_atAR1, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id2=processed_result2[0]['lsp_id']
        assert_that(lsp_id2!=lsp_id1,"Шаг2. ID RSVP LSP в выводе команды равен ID на шаге 1, а должен измениться")
        lsp_src=processed_result2[0]['lsp_src']
        assert_that(lsp_src=='10.0.19.2',"Шаг2. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.2, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result2[0]['lsp_dst']
        assert_that(lsp_dst=='10.0.19.4',"Шаг2. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.4, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result2[0]['lsp_state']
        assert_that(lsp_state=='up',"Шаг2. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result2[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Tengigabitethernet0/0/17.366',"Шаг2. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/17.366, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result2[0]['hop_number']
        hop0_incoming_ERO=processed_result2[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result2[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.54.49/32' and hop0_outgoing_ERO=='192.168.54.50/32',"Шаг2. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.54.49/32,192.168.54.50/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))

        hop1=processed_result2[1]['hop_number']
        hop1_incoming_ERO=processed_result2[1]['incoming_ERO']
        hop1_outgoing_ERO=processed_result2[1]['outgoing_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.54.50/32' and hop1_outgoing_ERO=='192.168.54.1/32',"Шаг2. Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.54.50/32,192.168.54.1/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))

        hop2=processed_result2[2]['hop_number']
        hop2_incoming_ERO=processed_result2[2]['incoming_ERO']
        hop2_outgoing_ERO=processed_result2[2]['outgoing_ERO']
        assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.54.1/32' and hop2_outgoing_ERO=='192.168.54.2/32',"Шаг2. Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.54.1/32,192.168.54.2/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))


        hop3=processed_result2[3]['hop_number']
        hop3_incoming_ERO=processed_result2[3]['incoming_ERO']
        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.54.2/32',"Шаг2. Один или несколько параметров из hop3, hop3_incoming_ERO,  не равен ожидаемым значениям hop3, 192.168.54.2/32 вместо этого получены значения %s, %s"%(hop3,hop3_incoming_ERO))


# Шаг3. А теперь ждем когда без трафика LSP вернётся на изначальный путь.
    time.sleep(610) # Приходится ждать 2 интервала по 300 секунд (300 секнд это минимальный интерал измерения)
    conn.execute(cmd)
    print('Шаг3. Проверяем как перестроился туннель %s\r'%tun_name)
    resp3=conn.response
    allure.attach(resp3, 'Шаг3.Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
#    print(resp3)    
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm3 = textfsm.TextFSM(template)
    processed_result3 = fsm3.ParseTextToDicts(resp3)

    if hostname == DUT1['hostname']:
        tun_name=processed_result3[0]['tun_name']
        assert_that(tun_name=='to_atAR2',"Шаг3. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result3[0]['tun_id']
        assert_that(tun_id!='',"Шаг3. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_name=processed_result3[0]['lsp_name']
        assert_that(lsp_name=='atAR1_to_atAR2',"Шаг3. Имя LSP в выводе команды не соответствует ожидаемому atAR1_to_atAR2, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result3[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_atAR2@atAR1_to_atAR2',"Шаг3. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR2@atAR1_to_atAR2, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id3=processed_result3[0]['lsp_id']
        assert_that(lsp_id3==lsp_id1,"Шаг3. ID RSVP LSP не равно значению которе было на шаге 1")
        lsp_src=processed_result3[0]['lsp_src']
        assert_that(lsp_src=='10.0.19.4',"Шаг3. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.4, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result3[0]['lsp_dst']
        assert_that(lsp_dst=='10.0.19.2',"Шаг3. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.2, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result3[0]['lsp_state']
        assert_that(lsp_state=='up',"Шаг3. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result3[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Tengigabitethernet0/0/18.200',"Шаг3. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/18.200, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result3[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result3[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.54.6/32' and hop0_outgoing_ERO=='192.168.54.5/32',"Шаг3. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.54.6/32,192.168.54.5/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
        hop1=processed_result3[1]['hop_number']
        hop1_incoming_ERO=processed_result3[1]['incoming_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.54.5/32',"Шаг3. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.54.5/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))


    if hostname == DUT2['hostname']:
        tun_name=processed_result3[0]['tun_name']
        assert_that(tun_name=='to_atAR1',"Шаг1. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result3[0]['tun_id']
        assert_that(tun_id!='',"Шаг1. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
        lsp_name=processed_result3[0]['lsp_name']
        assert_that(lsp_name=='atAR2_to_atAR1',"Шаг1. Имя LSP в выводе команды не соответствует ожидаемому atAR2_to_atAR1, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result3[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_atAR1@atAR2_to_atAR1',"Шаг1. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR1@atAR2_to_atAR1, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id3=processed_result3[0]['lsp_id']
        assert_that(lsp_id3==lsp_id1,"Шаг3. ID RSVP LSP не равно значению которе было на шаге 1")
        lsp_src=processed_result3[0]['lsp_src']
        assert_that(lsp_src=='10.0.19.2',"Шаг1. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.2, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result3[0]['lsp_dst']
        assert_that(lsp_dst=='10.0.19.4',"Шаг1. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.19.4, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result3[0]['lsp_state']
        assert_that(lsp_state=='up',"Шаг1. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result3[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Tengigabitethernet0/0/15.200',"Шаг1. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/15.200, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result3[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result3[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.54.5/32' and hop0_outgoing_ERO=='192.168.54.6/32',"Шаг1. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.54.5/32,192.168.54.6/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
        hop1=processed_result3[1]['hop_number']
        hop1_incoming_ERO=processed_result3[1]['incoming_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.54.6/32',"Шаг1. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.54.6/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))
