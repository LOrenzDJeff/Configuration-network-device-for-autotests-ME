from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.10:Функциональное тестирование Affinity/Admin Groups протокола RSVP-TE')
@allure.title('Проверка как построились  RSVP LSP туннели с учетом ограничениq Affinity/Admin Groups')
@pytest.mark.part14_10
@pytest.mark.affinity
@pytest.mark.dependency(depends=["load_config1410_dut1","load_config1410_dut2","load_config1410_dut3","load_config1410_dut6"],scope='session')
@pytest.mark.parametrize('ip, login, password, lsp_name', [(DUT3['host_ip'], DUT3['login'], DUT3['password'], 'to_vMX-1'),(DUT2['host_ip'], DUT2['login'], DUT2['password'], 'to_vMX'),(DUT1['host_ip'], DUT1['login'], DUT1['password'], 'to_vMX-2')])
def test_affinity_part14_10 (ip, login, password, lsp_name): 
    if ip == DUT3['host_ip']:
        allure.attach.file('./network-schemes/part14_10_show_mpls_rsvp_affinity_from_atDR1.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
#        allure.attach.file('./network-schemes/part14_10_show_mpls_rsvp_affinity-cmd_to_vMX-1.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)
    elif ip == DUT2['host_ip']:
        allure.attach.file('./network-schemes/part14_10_show_mpls_rsvp_affinity_from_atAR2.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
#        allure.attach.file('./network-schemes/part14_10_show_mpls_rsvp_affinity-cmd_to_atDR1.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)
    elif ip == DUT1['host_ip']:
        allure.attach.file('./network-schemes/part14_10_show_mpls_rsvp_affinity_from_atAR1.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
#        allure.attach.file('./network-schemes/part14_10_show_mpls_rsvp_affinity-cmd_to_vMX-2.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)

    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
# Маршрутизаторы ME по умолчанию считают доступной к резерву ВСЮ физическую полосу на интерфейсе (т.е. подход как у Джунипера, например у Циско и Хуавэй подход противоположный - по умолчанию доступный резерв - НОЛЬ)
# Учитывая вышеизложенный факт, туннель с требованием резерва полосы (если применить всю конфигурацию одним commit-ом) может подняться раньше чем в nbase придет информация о том
# что на интерфейсе полоса меньше физической и как следствие RSVP LSP построится через интерфейс на котором не хватет полосы
# Чтобы этого избежать сделаем shut/no shut для туннеля to_vMX-1
    conn.set_prompt('#')
    conn.execute ('config')
    conn.execute ('mpls rsvp tunnel  %s'%lsp_name)
    conn.execute ('shutdown')
    conn.execute ('commit')
    conn.execute ('no shutdown')
    conn.execute ('commit')
    time.sleep(20) # Подождем пока RSVP LSP туннеля построится
    conn.execute ('end')
    conn.execute('terminal datadump')
    cmd=('show mpls rsvp lsps tunnel %s'%lsp_name)
    conn.execute(cmd)
    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'
#    resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
#    allure.attach(resp_output[2], 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_name.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    result = fsm.ParseText(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()


    if ip == DUT3['host_ip']:

        tun_name=processed_result[0]['tun_name']
        assert_that(tun_name=='to_vMX-1',"Имя туннеля в выводе команды не соответствует ожидаемому to_vMX-1, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result[0]['tun_id']
        assert_that(tun_id!='',"ID туннеля в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%tun_id)
        lsp_name=processed_result[0]['lsp_name']
        assert_that(lsp_name=='notOrangeBlueVioletMustHave',"Имя LSP в выводе команды не соответствует ожидаемому notOrangeBlueVioletMustHave, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_vMX-1@notOrangeBlueVioletMustHave',"Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_vMX-1@notOrangeBlueVioletMustHave, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id=processed_result[0]['lsp_id']
        assert_that(lsp_id!='',"ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%lsp_id)
        lsp_src=processed_result[0]['lsp_src']
        assert_that(lsp_src=='1.0.0.1',"Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.1, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result[0]['lsp_dst']
        assert_that(lsp_dst=='1.0.0.4',"Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.4, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result[0]['lsp_state']
        assert_that(lsp_state=='up',"Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Bundle-ether2',"Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']        
        hop0_incoming_ERO=processed_result[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.5/32' and hop0_outgoing_ERO=='192.168.55.6/32',"Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.5/32,192.168.55.6/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
        hop1=processed_result[1]['hop_number']
        hop1_incoming_ERO=processed_result[1]['incoming_ERO']
        hop1_outgoing_ERO=processed_result[1]['outgoing_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.6/32' and hop1_outgoing_ERO=='192.168.55.13/32',"Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.6/32, 192.168.55.13/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))
        hop2=processed_result[2]['hop_number']
        hop2_incoming_ERO=processed_result[2]['incoming_ERO']
        hop2_outgoing_ERO=processed_result[2]['outgoing_ERO']
        assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.13/32' and hop2_outgoing_ERO=='192.168.55.14/32',"Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.13/32, 192.168.55.14/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))
#        hop3=processed_result[3]['hop_number']
#        hop3_incoming_ERO=processed_result[3]['incoming_ERO']
#        hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
#        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.22/32' and hop3_outgoing_ERO=='192.168.55.13/32',"Один или несколько параметров из hop3, hop3_incoming_ERO, hop3_outgoing_ERO не равен ожидаемым значениям hop3, 192.168.55.22/32, 192.168.55.13/32 вместо этого получены значения %s, %s, %s,"%(hop3,hop3_incoming_ERO,hop3_outgoing_ERO))
#        hop4=processed_result[4]['hop_number']
#        hop4_incoming_ERO=processed_result[4]['incoming_ERO']
#        hop4_outgoing_ERO=processed_result[4]['outgoing_ERO']
#        assert_that(hop4=='hop4' and hop4_incoming_ERO=='192.168.55.13/32' and hop4_outgoing_ERO=='192.168.55.14/32',"Один или несколько параметров из hop4, hop4_incoming_ERO, hop4_outgoing_ERO не равен ожидаемым значениям hop4,192.168.55.13/32,192.168.55.14/32 вместо этого получены значения %s, %s, %s,"%(hop4,hop4_incoming_ERO,hop4_outgoing_ERO))
        hop3=processed_result[3]['hop_number']
        hop3_incoming_ERO=processed_result[3]['incoming_ERO']
        hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.14/32' and hop3_outgoing_ERO=='',"Один или несколько параметров из hop3, hop3_incoming_ERO, hop3_outgoing_ERO не равен ожидаемым значениям hop3,192.168.55.14/32, вместо этого получены значения %s, %s, %s,"%(hop3,hop3_incoming_ERO,hop3_outgoing_ERO))
        
    elif ip == DUT2['host_ip']:
        tun_name=processed_result[0]['tun_name']
        assert_that(tun_name=='to_vMX',"Имя туннеля в выводе команды не соответствует ожидаемому to_vMX, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result[0]['tun_id']
        assert_that(tun_id!='',"ID туннеля в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%tun_id)
        lsp_name=processed_result[0]['lsp_name']
        assert_that(lsp_name=='notGreen',"Имя LSP в выводе команды не соответствует ожидаемому not_Green, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_vMX@notGreen',"Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_vMX@notGreen, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id=processed_result[0]['lsp_id']
        assert_that(lsp_id!='',"ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%lsp_id)
        lsp_src=processed_result[0]['lsp_src']
        assert_that(lsp_src=='1.0.0.2',"Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.2, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result[0]['lsp_dst']
        assert_that(lsp_dst=='1.0.0.4',"Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.4, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result[0]['lsp_state']
        assert_that(lsp_state=='up',"Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Bundle-ether1',"Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether1, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.6/32' and hop0_outgoing_ERO=='192.168.55.5/32',"Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.6/32,192.168.55.5/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))        
        hop1=processed_result[1]['hop_number']
        hop1_incoming_ERO=processed_result[1]['incoming_ERO']
        hop1_outgoing_ERO=processed_result[1]['outgoing_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.5/32' and hop1_outgoing_ERO=='192.168.55.17/32',"Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.5/32, 192.168.55.17/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))
        hop2=processed_result[2]['hop_number']
        hop2_incoming_ERO=processed_result[2]['incoming_ERO']
        hop2_outgoing_ERO=processed_result[2]['outgoing_ERO']
        assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.17/32' and hop2_outgoing_ERO=='192.168.55.18/32',"Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.17/32, 192.168.55.18/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))
        hop3=processed_result[3]['hop_number']
#        hop3_incoming_ERO=processed_result[3]['incoming_ERO']
#        hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
#        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.9/32' and hop3_outgoing_ERO=='192.168.55.1/32',"Один или несколько параметров из hop3, hop3_incoming_ERO, hop3_outgoing_ERO не равен ожидаемым значениям hop3, 192.168.55.9/32, 192.168.55.1/32 вместо этого получены значения %s, %s, %s,"%(hop3,hop3_incoming_ERO,hop3_outgoing_ERO))        
#        hop4=processed_result[4]['hop_number']
#        hop4_incoming_ERO=processed_result[4]['incoming_ERO']
#        hop4_outgoing_ERO=processed_result[4]['outgoing_ERO']
#        assert_that(hop4=='hop4' and hop4_incoming_ERO=='192.168.55.1/32' and hop4_outgoing_ERO=='192.168.55.2/32',"Один или несколько параметров из hop4, hop4_incoming_ERO, hop4_outgoing_ERO не равен ожидаемым значениям hop4,192.168.55.1/32,192.168.55.2/32 вместо этого получены значения %s, %s, %s,"%(hop4,hop4_incoming_ERO,hop4_outgoing_ERO))
        hop3=processed_result[3]['hop_number']
        hop3_incoming_ERO=processed_result[3]['incoming_ERO']
        hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.18/32' and hop3_outgoing_ERO=='',"Один или несколько параметров из hop3, hop3_incoming_ERO, hop3_outgoing_ERO не равен ожидаемым значениям hop3,192.168.55.18/32, вместо этого получены значения %s, %s, %s,"%(hop3,hop3_incoming_ERO,hop3_outgoing_ERO))


    elif ip == DUT1['host_ip']:
        tun_name=processed_result[0]['tun_name']
        assert_that(tun_name=='to_vMX-2',"Имя туннеля в выводе команды не соответствует ожидаемому to_vMX-2, вместо этого значение равно %s"%tun_name)
        tun_id=processed_result[0]['tun_id']
        assert_that(tun_id!='',"ID туннеля в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%tun_id)
        lsp_name=processed_result[0]['lsp_name']
        assert_that(lsp_name=='notGreen',"Имя LSP в выводе команды не соответствует ожидаемому notGreen, вместо этого значение равно %s"%lsp_name)
        lsp_signal_name=processed_result[0]['lsp_signal_name']
        assert_that(lsp_signal_name=='to_vMX-2@notGreen',"Сигнальное имя LSP в выводе команды не соответствует ожидаемому to_vMX-2@notGreen, вместо этого значение равно %s"%lsp_signal_name)
        lsp_id=processed_result[0]['lsp_id']
        assert_that(lsp_id!='',"ID RSVP LSP в выводе команды не соответствует ожидаемому в шаблоне, вместо этого значение равно %s"%lsp_id)
        lsp_src=processed_result[0]['lsp_src']
        assert_that(lsp_src=='1.0.0.3',"Source IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.3, вместо этого значение равно %s"%lsp_src)
        lsp_dst=processed_result[0]['lsp_dst']
        assert_that(lsp_dst=='1.0.0.4',"Destination IP для RSVP LSP в выводе команды не соответствует ожидаемому 1.0.0.4, вместо этого значение равно %s"%lsp_dst)
        lsp_state=processed_result[0]['lsp_state']
        assert_that(lsp_state=='up',"Статус RSVP LSP в выводе команды не соответствует ожидаемому up, вместо этого значение равно %s"%lsp_state)
        lsp_signal_int=processed_result[0]['lsp_signal_int']
        assert_that(lsp_signal_int=='Bundle-ether2',"Сигнальный интерфейс для RSVP LSP в выводе команды не соответствует ожидаемому Bundle-ether2, вместо этого значение равно %s"%lsp_signal_int)
        hop0=processed_result[0]['hop_number']
        hop0_incoming_ERO=processed_result[0]['incoming_ERO']
        hop0_outgoing_ERO=processed_result[0]['outgoing_ERO']
        assert_that(hop0=='hop0' and hop0_incoming_ERO=='192.168.55.21/32' and hop0_outgoing_ERO=='192.168.55.22/32',"Один или несколько параметров из hop0, hop0_incoming_ERO, hop0_outgoing_ERO не равен ожидаемым значениям hop0, 192.168.55.21/32,192.168.55.22/32 вместо этого получены значения %s, %s, %s,"%(hop0,hop0_incoming_ERO,hop0_outgoing_ERO))
        hop1=processed_result[1]['hop_number']
        hop1_incoming_ERO=processed_result[1]['incoming_ERO']
        hop1_outgoing_ERO=processed_result[1]['outgoing_ERO']
        assert_that(hop1=='hop1' and hop1_incoming_ERO=='192.168.55.22/32' and hop1_outgoing_ERO=='192.168.55.6/32',"Один или несколько параметров из hop1, hop1_incoming_ERO, hop1_outgoing_ERO не равен ожидаемым значениям hop1, 192.168.55.22/32, 192.168.55.6/32 вместо этого получены значения %s, %s, %s,"%(hop1,hop1_incoming_ERO,hop1_outgoing_ERO))
        hop2=processed_result[2]['hop_number']
        hop2_incoming_ERO=processed_result[2]['incoming_ERO']
        hop2_outgoing_ERO=processed_result[2]['outgoing_ERO']
        assert_that(hop2=='hop2' and hop2_incoming_ERO=='192.168.55.6/32' and hop2_outgoing_ERO=='192.168.55.5/32',"Один или несколько параметров из hop2, hop2_incoming_ERO, hop2_outgoing_ERO не равен ожидаемым значениям hop2, 192.168.55.6/32, 192.168.55.5/32 вместо этого получены значения %s, %s, %s,"%(hop2,hop2_incoming_ERO,hop2_outgoing_ERO))
        hop3=processed_result[3]['hop_number']
        hop3_incoming_ERO=processed_result[3]['incoming_ERO']
        hop3_outgoing_ERO=processed_result[3]['outgoing_ERO']
        assert_that(hop3=='hop3' and hop3_incoming_ERO=='192.168.55.5/32' and hop3_outgoing_ERO=='192.168.55.17/32',"Один или несколько параметров из hop3, hop3_incoming_ERO, hop3_outgoing_ERO не равен ожидаемым значениям hop3, 192.168.55.5/32,192.168.55.17/32 вместо этого получены значения %s, %s, %s,"%(hop3,hop3_incoming_ERO,hop3_outgoing_ERO))

