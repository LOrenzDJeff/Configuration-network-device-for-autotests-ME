from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.3:Функциональное тестирование bandwidth reservation протокола RSVP-TE')
@allure.title('Проверка как построился RSVP LSP туннеля to_vMX-1 при изменении max-resv-band на транзитном LSR')
@pytest.mark.part14_3
@pytest.mark.change_max_resv_band_transit_lsr
@pytest.mark.parametrize('ip, login, password, tun_name', [(DUT3['host_ip'], DUT3['login'], DUT3['password'], 'to_vMX-1'),(DUT1['host_ip'], DUT1['login'], DUT1['password'], 'to_vMX-2'),(DUT2['host_ip'], DUT2['login'], DUT2['password'], 'to_atDR1')])
def test_change_max_resv_band_transit_part14_3 (ip, login, password, tun_name): 
    if ip == DUT3['host_ip']:
        allure.attach.file('./network-schemes/part14_3_change_max_resv_band_atDR1.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
    elif ip == DUT2['host_ip']:
        allure.attach.file('./network-schemes/part14_3_change_max_resv_band_atAR2.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
    elif ip == DUT1['host_ip']:
        allure.attach.file('./network-schemes/part14_3_change_max_resv_band_atAR1.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    if ip == DUT3['host_ip'] or ip ==DUT1['host_ip']:   	
# Подключаемся к atAR1 для того чтобы изменить max-resv-band на транзитных интерфейсах  Te0/0/11.352 и BU2
	    conn2 = Telnet()
	    acc2 = Account(DUT1['login'], DUT1['password'])
	    conn2.connect(DUT1['host_ip'])
	    conn2.login(acc2)
	    conn2.execute('terminal datadump')
	    conn2.execute('configure')
	    conn2.execute('mpls rsvp')
	    conn2.execute('interface te0/0/11.352') # Будем увеличивать max-resv-band
	    conn2.execute('maximum-reservable-bandwidth 10000000')
	    conn2.execute('interface bu2') # Будем уменьшать max-resv-band
	    conn2.execute('maximum-reservable-bandwidth 100000')
	#    conn2.set_prompt('Commit successfully completed')
	    conn2.execute('commit')
	#    conn2.set_prompt('#')
	    conn2.execute('end')
	    time.sleep(15) # Без этой паузы tun_name не перестраивается даже после ручного запуска процедуры M-B-B
    elif ip == DUT2['host_ip']:
	    conn2 = Telnet()
	    acc2 = Account(DUT2['login'], DUT2['password'])
	    conn2.connect(DUT2['host_ip'])
	    conn2.login(acc2)
	    conn2.execute('terminal datadump')
	    conn2.execute('configure')
	    conn2.execute('mpls rsvp')
	    conn2.execute('interface bu2') # Будем увеличивать max-resv-band
	    conn2.execute('maximum-reservable-bandwidth 3000000')
	#    conn2.set_prompt('Commit successfully completed')
	    conn2.execute('commit')
	#    conn2.set_prompt('#')
	    conn2.execute('end')


# Теперь проверяем как перестроился RSVP LSP у туннеля tun_name
    conn.execute('terminal datadump')
    cmd=('mpls rsvp make-before-break %s'%tun_name)  # На момент написания этого теста автоматический Make-Before-Breake еще не реализован поэтому запускаем его вручную 
    conn.execute(cmd)
    time.sleep(10) 
    cmd=('show mpls rsvp lsps tunnel %s'%tun_name)
    conn.execute(cmd)
    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    result = fsm.ParseText(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()
    conn2.send('quit\r')
    conn2.close()    
    tun_name=processed_result[0]['tun_name']
    tun_id=processed_result[0]['tun_id']
    lsp_name=processed_result[0]['lsp_name']
    lsp_signal_name=processed_result[0]['lsp_signal_name']
    lsp_id=processed_result[0]['lsp_id']
    lsp_src=processed_result[0]['lsp_src']
    lsp_dst=processed_result[0]['lsp_dst']
    lsp_state=processed_result[0]['lsp_state']
    lsp_signal_int=processed_result[0]['lsp_signal_int']


    if ip == DUT3['host_ip']:
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
#	    hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']


	    assert_that(tun_name=='to_vMX-1',"Имя туннеля в выводе команды не соответствует ожидаемому to_vMX-1, вместо этого значение равно %s"%tun_name)
	    assert_that(tun_id!='',"ID туннеля в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%tun_id)
	    assert_that(lsp_name=='from_atDR1_to_vMX-1',"Имя LSP в выводе команды не соответствует ожидаемому from_atDR1_to_vMX-1, вместо этого значение равно %s"%lsp_name)
	    assert_that(lsp_signal_name=='to_vMX-1@from_atDR1_to_vMX-1',"Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_vMX-1@from_atDR1_to_vMX-1, вместо этого значение равно %s"%lsp_signal_name)
	    assert_that(lsp_id!='',"ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%lsp_id)
	    assert_that(lsp_src=='1.0.0.1',"Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.1, вместо этого значение равно %s"%lsp_src)
	    assert_that(lsp_dst=='1.0.0.4',"Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.4, вместо этого значение равно %s"%lsp_dst)
	    assert_that(lsp_state=='up',"Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    assert_that(lsp_signal_int=='Bundle-ether1',"Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether1, вместо этого значение равно %s"%lsp_signal_int)
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.2/32' and hop0_outgoing_ERO=='192.168.55.1/32',"Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.2/32,192.168.55.1/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.1/32' and hop1_outgoing_ERO=='192.168.55.9/32',"Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.1/32, 192.168.55.9/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))
	    assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.9/32' and hop2_outgoing_ERO=='192.168.55.10/32',"Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.9/32, 192.168.55.10/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))
	    assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.10/32',"Один или несколько параметров из hop3, hop3_incoming_ERO не равен ожидаемым значениям hop3, 192.168.55.10/32 вместо этого получены значения %s, %s"%(hop3,hop3_incoming_ERO))
    elif ip == DUT2['host_ip']:
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

	    assert_that(tun_name=='to_atDR1',"Имя туннеля в выводе команды не соответствует ожидаемому to_atDR1, вместо этого значение равно %s"%tun_name)
	    assert_that(tun_id!='',"ID туннеля в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%tun_id)
	    assert_that(lsp_name=='atAR2_to_atDR1-lsp1',"Имя LSP в выводе команды не соответствует ожидаемому atAR2_to_atDR1-lsp1, вместо этого значение равно %s"%lsp_name)
	    assert_that(lsp_signal_name=='to_atDR1@atAR2_to_atDR1-lsp1',"Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_atDR1@atAR2_to_atDR1-lsp1, вместо этого значение равно %s"%lsp_signal_name)
	    assert_that(lsp_id!='',"ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%lsp_id)
	    assert_that(lsp_src=='1.0.0.2',"Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_src)
	    assert_that(lsp_dst=='1.0.0.1',"Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.1, вместо этого значение равно %s"%lsp_dst)
	    assert_that(lsp_state=='up',"Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    assert_that(lsp_signal_int=='Bundle-ether2',"Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)

	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.22/32' and hop0_outgoing_ERO=='192.168.55.21/32',"Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.22/32,192.168.55.21/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.21/32' and hop1_outgoing_ERO=='192.168.55.1/32',"Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.21/32, 192.168.55.1/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))
	    assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.1/32' and hop2_outgoing_ERO=='192.168.55.2/32',"Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.1/32, 192.168.55.2/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))
	    assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.2/32' ,"Один или несколько параметров из hop3, hop3_incoming_ERO не равен ожидаемым значениям hop3, 192.168.55.2/32 вместо этого получены значения %s, %s"%(hop3,hop3_incoming_ERO))
	    


    elif ip == DUT1['host_ip']:
	    hop0=processed_result[0]['hop_number']
	    hop0_incoming_ERO=processed_result[0]['incoming_ERO']
	    hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
	    hop1=processed_result[1]['hop_number']
	    hop1_incoming_ERO=processed_result[1]['incoming_ERO']

	    assert_that(tun_name=='to_vMX-2',"Имя туннеля в выводе команды не соответствует ожидаемому to_vMX-2, вместо этого значение равно %s"%tun_name)
	    assert_that(tun_id!='',"ID туннеля в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%tun_id)
	    assert_that(lsp_name=='atAR1_to_vMX-2-lsp',"Имя LSP в выводе команды не соответствует ожидаемому atAR1_to_vMX-2-lsp, вместо этого значение равно %s"%lsp_name)
	    assert_that(lsp_signal_name=='to_vMX-2@atAR1_to_vMX-2-lsp',"Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_vMX-2@atAR1_to_vMX-2-lsp, вместо этого значение равно %s"%lsp_signal_name)
	    assert_that(lsp_id!='',"ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%lsp_id)
	    assert_that(lsp_src=='1.0.0.3',"Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_src)
	    assert_that(lsp_dst=='1.0.0.4',"Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.4, вместо этого значение равно %s"%lsp_dst)
	    assert_that(lsp_state=='up',"Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
	    assert_that(lsp_signal_int=='Tengigabitethernet0/0/11.352',"Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Tengigabitethernet0/0/11.352, вместо этого значение равно %s"%lsp_signal_int)
	    assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.9/32' and hop0_outgoing_ERO=='192.168.55.10/32',"Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.9/32,192.168.55.10/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
	    assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.10/32',"Один или несколько параметров из hop1, hop1_incoming_ERO,  не равен ожидаемым значениям hop1, 192.168.55.10/32 вместо этого получены значения %s, %s"%(hop1,hop1_incoming_ERO))
