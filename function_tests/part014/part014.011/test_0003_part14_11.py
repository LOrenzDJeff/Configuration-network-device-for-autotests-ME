from conftest import *

#debug_cmd_list=['debug pp-mgr cmd','debug pp-mgr general','debug pp-mgr arp','debug pp-mgr bfd','debug pp-mgr egress']

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.11:Функциональное тестирование MPLS TE AutoBandwidth')
@allure.title('Проверка перестроения RSVP LSP при изменении объема передаваемого через него трафика')
@pytest.mark.part14_11
@pytest.mark.mpls_te_autobandwidth_test1
@pytest.mark.dependency(depends=["load_config1411_dut1","load_config1411_dut2","load_config1411_dut3"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password, tun_name', [(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'],'to_atAR2'),(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'],'to_atAR1')])
#@pytest.mark.parametrize('ip , hostname , login, password, tun_name', [(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'],'to_atAR2')])
def test_mpls_te_autobandwidth_test1_part14_11 (ip, hostname, login, password, tun_name): 
    if hostname==DUT1['hostname']:
    	allure.attach.file('./network-schemes/part14_11_mpls_te_ab_atAR1_test1.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
    	docker_compose_file='part14_11_atAR1_docker-compose.yaml'
    	ip_iperf_client='192.168.73.3'
    	ip_iperf_server='192.168.74.3'
    if hostname==DUT2['hostname']:
    	allure.attach.file('./network-schemes/part14_11_mpls_te_ab_atAR2_test1.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
    	docker_compose_file='part14_11_atAR2_docker-compose.yaml'
    	ip_iperf_client='192.168.74.3'
    	ip_iperf_server='192.168.73.3'
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    # Определим ожидаемое время переключения RSVP LSP в данном тесте
    blue_red_switch_time=350 # Время генерации трафика в течение которого должно быть переключение с синего на красный путь, иначе тест будет считаться не успешным на шаге 2
    red_blue_switch_time=610 # Время в течение которого RSVP LSP (без трафика) должен вернуться с красного на синий путь, иначе тест будет считаться не успешным на шаге 3
# Перед началом теста необходимо пересигнализировать RSVP LSP чтобы туннель поднялся с уже применёнными настройками egress-general-label на соседе.
# Если этого не сделать RSVP LSP туннель может быть например поднят в тесте  другого раздела где настроек отключающих PHP нет. Из-за наличия метки 3 
# на стороне Ingress LSR статистика по трафику собираться не будет и тест не выполнися успешно
    conn.execute('configure') 
    conn.execute('mpls rsvp tunnel %s'%tun_name)
    conn.execute('shutdown')
    conn.execute('commit')
    conn.execute('no shutdown')
    conn.execute('commit')
    conn.execute('end')        
# Шаг1. Проверяем что RSVP LSP  построился кратчайшим путем без трафика проходящего через него
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
	    assert_that(lsp_src=='1.0.0.3',"Шаг1. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_src)
	    lsp_dst=processed_result[0]['lsp_dst']
	    assert_that(lsp_dst=='1.0.0.2',"Шаг1. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_dst)
	    lsp_state=processed_result[0]['lsp_state']
	    assert_that(lsp_state=='up',"Шаг1. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    lsp_signal_int=processed_result[0]['lsp_signal_int']
	    assert_that(lsp_signal_int=='Bundle-ether2',"Шаг1. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)
	    hop0=processed_result[0]['hop_number']
	    hop0_incoming_ERO=processed_result[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.21/32' and hop0_outgoing_ERO=='192.168.55.22/32',"Шаг1. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.21/32,192.168.55.22/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    hop1=processed_result[1]['hop_number']
	    hop1_incoming_ERO=processed_result[1]['incoming_ERO']
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.22/32',"Шаг1. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.55.22/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))


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
	    assert_that(lsp_src=='1.0.0.2',"Шаг1. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_src)
	    lsp_dst=processed_result[0]['lsp_dst']
	    assert_that(lsp_dst=='1.0.0.3',"Шаг1. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_dst)
	    lsp_state=processed_result[0]['lsp_state']
	    assert_that(lsp_state=='up',"Шаг1. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    lsp_signal_int=processed_result[0]['lsp_signal_int']
	    assert_that(lsp_signal_int=='Bundle-ether2',"Шаг1. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)
	    hop0=processed_result[0]['hop_number']
	    hop0_incoming_ERO=processed_result[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.22/32' and hop0_outgoing_ERO=='192.168.55.21/32',"Шаг1. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.22/32,192.168.55.21/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    hop1=processed_result[1]['hop_number']
	    hop1_incoming_ERO=processed_result[1]['incoming_ERO']
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.21/32',"Шаг1. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.55.21/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))

# Шаг2. Запускаем iperf c полосой пропускания 60 Mbps и через 300 сек смотрим как перестроился RSVP LSP


    result_loss=0
    packet_send=0
    packet_recv=0
    q = queue.Queue()  # Через эту очередь будем возвращать из процедуры результаты генерации iperf-ом
    start_traffic_gen=time.time() # Фиксируем время начала генерации трафика
    x=thread_with_trace(target=start_docker_iperf3_server_client_queue,args=(ip_iperf_server,blue_red_switch_time , '60M' , result_loss , packet_send,packet_recv, docker_compose_file, q))

    x.start() # Запускаем iperf клиент и сервер в докер-контейнерах

###############################################################################################        
# Проверим что есть пинг до iperf-сервера, иначе смысла нет ждать когда законфится тест
    conn.execute('ping %s vrf VRF40'%ip_iperf_server)
    resp=conn.response
    template = open('./templates/parse_ping_from_me.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
    print("Результат пинга сервера %s: %s\r"%(ip_iperf_server,processed_result))
    ping_success_rate=processed_result[0]['success_rate']
#Если  ping_success_rate == 0.0, то аварийно завершаем тест
#    assert_that(ping_success_rate!='0.0',"Шаг2. iperf-сервер %s с %s не доступен. Тест аварийно завершаем"%(ip_iperf_server,hostname))       
    conn.execute('clear arp vrf VRF40 address %s'%ip_iperf_client) # Без этой фигни связи нет....Чистим arp-кэш т.к. MAC адрес может измениться у docker контейнера при запуске от теста к тесту и это приведёт к проблемам со связностью между клиентом и сервером

# Проверим что есть пинг до iperf-клиента, иначе смысла нет ждать когда законфится тест
    conn.execute('ping %s vrf VRF40'%ip_iperf_client)
    resp=conn.response
    template = open('./templates/parse_ping_from_me.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
    print("Результат пинга клиента %s: %s\r"%(ip_iperf_client,processed_result))
    ping_success_rate=processed_result[0]['success_rate']
#Если  ping_success_rate == 0.0, то аварийно завершаем тест
#    assert_that(ping_success_rate!='0.0',"Шаг2. iperf-клиент %s с %s не доступен. Тест аварийно завершаем"%(ip_iperf_client,hostname))

# #################################################################################################        

    time.sleep(90)        
    cmd1='show mpls rsvp lsp autobandwidth'
    conn.execute(cmd1)
    resp=conn.response
    allure.attach(resp, 'Шаг2.Вывод команды %s'%cmd1, attachment_type=allure.attachment_type.TEXT)


    while x.is_alive():        
        curr_seconds=time.time()
        duration_time=curr_seconds-start_traffic_gen
#        print("duration time is - %d"%duration_time)
        time.sleep(2)
        if duration_time>blue_red_switch_time:
            x.kill()
            subprocess.check_call(f'docker-compose -f tools/docker/iperf/%s down -t 1'%docker_compose_file,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
#            result, _ = services.communicate()

            print("Timeout - %d sec"%blue_red_switch_time)    
#    print("Статус потока Х - %s"%x.is_alive())            
    x.join() # Подождем пока генерация трафика не закончится, иначе могут начаться другие тесты а этот по сути ещё не окончился....

    stop_traffic_gen=time.time()  # Фиксируем время прекращения генерации трафика
    stop_traffic_time_struct=time.localtime(stop_traffic_gen)

    print('Шаг2. Генерация трафика остановлена в %s. Длительность - %d cекунд\r'%(time.strftime('%H:%M:%S',stop_traffic_time_struct),stop_traffic_gen-start_traffic_gen))


# Шаг2. Проверяем как перестроился $tun_name после генерации 6 Mbps трафика и истечения blue_red_switch_time секунд
    conn.execute(cmd)

    check_time_step2=time.time()  # Фиксируем время проверки на шаге2: C Синего на Красный путь
    check_time_step2_struct=time.localtime(check_time_step2)

    print('Шаг2. %s Проверяем как перестроился туннель %s\r'%(time.strftime('%H:%M:%S',check_time_step2_struct),tun_name))



    resp2=conn.response
    allure.attach(resp2, 'Шаг2.Вывод команды %s после генерации трафика в течение %d секунд'%(cmd,blue_red_switch_time), attachment_type=allure.attachment_type.TEXT)
#    print(resp2)    
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
	    lsp_src=processed_result2[0]['lsp_src']
	    assert_that(lsp_src=='1.0.0.3',"Шаг2. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 10.0.0.3, вместо этого значение равно %s"%lsp_src)
	    lsp_dst=processed_result2[0]['lsp_dst']
	    assert_that(lsp_dst=='1.0.0.2',"Шаг2. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_dst)
	    lsp_state=processed_result2[0]['lsp_state']
	    assert_that(lsp_state=='up',"Шаг2. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    lsp_signal_int=processed_result2[0]['lsp_signal_int']
	    assert_that(lsp_signal_int=='Bundle-ether1',"Шаг2. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether1, вместо этого значение равно %s"%lsp_signal_int)
	    hop0=processed_result2[0]['hop_number']
	    hop0_incoming_ERO=processed_result2[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result2[0]['outgoing_ERO']
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.1/32' and hop0_outgoing_ERO=='192.168.55.2/32',"Шаг2. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.1/32,192.168.55.2/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))

	    hop1=processed_result2[1]['hop_number']
	    hop1_incoming_ERO=processed_result2[1]['incoming_ERO']
	    hop1_outgoing_ERO=processed_result2[1]['outgoing_ERO']
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.2/32' and hop1_outgoing_ERO=='192.168.55.5/32',"Шаг2. Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.2/32,192.168.55.5/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))

	    hop2=processed_result2[2]['hop_number']
	    hop2_incoming_ERO=processed_result2[2]['incoming_ERO']
	    hop2_outgoing_ERO=processed_result2[2]['outgoing_ERO']
	    assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.5/32' and hop2_outgoing_ERO=='192.168.55.6/32',"Шаг2. Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.5/32,192.168.55.6/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))


	    hop3=processed_result2[3]['hop_number']
	    hop3_incoming_ERO=processed_result2[3]['incoming_ERO']
	    assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.6/32',"Шаг2. Один или несколько параметров из hop3, hop3_incoming_ERO,  не равен ожидаемым значениям hop3, 192.168.55.6/32 вместо этого получены значения %s, %s"%(hop3,hop3_incoming_ERO))


    if hostname == DUT2['hostname']:
	    tun_name=processed_result2[0]['tun_name']
	    assert_that(tun_name=='to_atAR1',"Шаг2. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
	    tun_id=processed_result2[0]['tun_id']
	    assert_that(tun_id!='',"Шаг2. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
	    lsp_name=processed_result2[0]['lsp_name']
	    assert_that(lsp_name=='atAR2_to_atAR1',"Шаг2. Имя LSP в выводе команды не соответствует ожидаемому atAR2_to_atAR1, вместо этого значение равно %s"%lsp_name)
	    lsp_signal_name=processed_result2[0]['lsp_signal_name']
	    assert_that(lsp_signal_name=='to_atAR1@atAR2_to_atAR1',"Шаг2. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR1@atAR2_to_atAR1, вместо этого значение равно %s"%lsp_signal_name)
	    lsp_src=processed_result2[0]['lsp_src']
	    assert_that(lsp_src=='1.0.0.2',"Шаг2. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_src)
	    lsp_dst=processed_result2[0]['lsp_dst']
	    assert_that(lsp_dst=='1.0.0.3',"Шаг2. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_dst)
	    lsp_state=processed_result2[0]['lsp_state']
	    assert_that(lsp_state=='up',"Шаг2. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    lsp_signal_int=processed_result2[0]['lsp_signal_int']
	    assert_that(lsp_signal_int=='Bundle-ether1',"Шаг2. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether1, вместо этого значение равно %s"%lsp_signal_int)
	    hop0=processed_result2[0]['hop_number']
	    hop0_incoming_ERO=processed_result2[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result2[0]['outgoing_ERO']
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.6/32' and hop0_outgoing_ERO=='192.168.55.5/32',"Шаг2. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.6/32,192.168.55.5/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))

	    hop1=processed_result2[1]['hop_number']
	    hop1_incoming_ERO=processed_result2[1]['incoming_ERO']
	    hop1_outgoing_ERO=processed_result2[1]['outgoing_ERO']
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.5/32' and hop1_outgoing_ERO=='192.168.55.2/32',"Шаг2. Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.5/32,192.168.55.2/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))

	    hop2=processed_result2[2]['hop_number']
	    hop2_incoming_ERO=processed_result2[2]['incoming_ERO']
	    hop2_outgoing_ERO=processed_result2[2]['outgoing_ERO']
	    assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.2/32' and hop2_outgoing_ERO=='192.168.55.1/32',"Шаг2. Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.2/32,192.168.55.1/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))


	    hop3=processed_result2[3]['hop_number']
	    hop3_incoming_ERO=processed_result2[3]['incoming_ERO']
	    assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.1/32',"Шаг2. Один или несколько параметров из hop3, hop3_incoming_ERO,  не равен ожидаемым значениям hop3, 192.168.55.1/32 вместо этого получены значения %s, %s"%(hop3,hop3_incoming_ERO))

    lsp_id2=processed_result2[0]['lsp_id']
#    assert_that(lsp_id2!=lsp_id1,"Шаг2. ID RSVP LSP в выводе команды равен ID на шаге 1, а должен измениться") #


# Шаг3. А теперь ждем когда без трафика LSP вернётся на изначальный путь.


    time.sleep(red_blue_switch_time) # Приходится ждать 2 интервала по 300 секунд (300 секнд это минимальный интерал изменения полосы - adjacent timer)
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
	    lsp_src=processed_result3[0]['lsp_src']
	    assert_that(lsp_src=='1.0.0.3',"Шаг3. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_src)
	    lsp_dst=processed_result3[0]['lsp_dst']
	    assert_that(lsp_dst=='1.0.0.2',"Шаг3. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_dst)
	    lsp_state=processed_result3[0]['lsp_state']
	    assert_that(lsp_state=='up',"Шаг3. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    lsp_signal_int=processed_result3[0]['lsp_signal_int']
	    assert_that(lsp_signal_int=='Bundle-ether2',"Шаг3. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)
	    hop0=processed_result3[0]['hop_number']
	    hop0_incoming_ERO=processed_result3[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result3[0]['outgoing_ERO']
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.21/32' and hop0_outgoing_ERO=='192.168.55.22/32',"Шаг3. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.21/32,192.168.55.22/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    hop1=processed_result3[1]['hop_number']
	    hop1_incoming_ERO=processed_result3[1]['incoming_ERO']
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.22/32',"Шаг3. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.55.22/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))


    if hostname == DUT2['hostname']:
	    tun_name=processed_result3[0]['tun_name']
	    assert_that(tun_name=='to_atAR1',"Шаг3. Имя туннеля в выводе команды не соответствует ожидаемому to_atAR2, вместо этого значение равно %s"%tun_name)
	    tun_id=processed_result3[0]['tun_id']
	    assert_that(tun_id!='',"Шаг3. ID туннеля в выводе команды не соответствует ожидаемому в шаблоне")
	    lsp_name=processed_result3[0]['lsp_name']
	    assert_that(lsp_name=='atAR2_to_atAR1',"Шаг3. Имя LSP в выводе команды не соответствует ожидаемому atAR2_to_atAR1, вместо этого значение равно %s"%lsp_name)
	    lsp_signal_name=processed_result3[0]['lsp_signal_name']
	    assert_that(lsp_signal_name=='to_atAR1@atAR2_to_atAR1',"Шаг3. Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atAR1@atAR2_to_atAR1, вместо этого значение равно %s"%lsp_signal_name)
	    lsp_src=processed_result3[0]['lsp_src']
	    assert_that(lsp_src=='1.0.0.2',"Шаг3. Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_src)
	    lsp_dst=processed_result3[0]['lsp_dst']
	    assert_that(lsp_dst=='1.0.0.3',"Шаг3. Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_dst)
	    lsp_state=processed_result3[0]['lsp_state']
	    assert_that(lsp_state=='up',"Шаг3. Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    lsp_signal_int=processed_result3[0]['lsp_signal_int']
	    assert_that(lsp_signal_int=='Bundle-ether2',"Шаг3. Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)
	    hop0=processed_result3[0]['hop_number']
	    hop0_incoming_ERO=processed_result3[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result3[0]['outgoing_ERO']
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.22/32' and hop0_outgoing_ERO=='192.168.55.21/32',"Шаг3. Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.22/32,192.168.55.21/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    hop1=processed_result3[1]['hop_number']
	    hop1_incoming_ERO=processed_result3[1]['incoming_ERO']
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.21/32',"Шаг3. Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.55.21/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))
    lsp_id3=processed_result3[0]['lsp_id']
#    assert_that(lsp_id3==lsp_id1,"Шаг3. ID RSVP LSP не равно значению которе было на шаге 1")

