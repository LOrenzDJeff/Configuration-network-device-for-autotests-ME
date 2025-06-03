from conftest import *
@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.5:Функциональное тестирование RSVP-TE E2E protection show-комманды')
@allure.title('Проверка вывода команды show mpls rsvp tunnels-lsp tunnel tunnel_name при включенном E2E protection')
@pytest.mark.part14_5
@pytest.mark.show_mpls_rsvp_lsps_tunnel_e2e
@pytest.mark.dependency(depends=["load_config145_dut1","load_config145_dut2","load_config145_dut3","load_config145_dut6"],scope='session')
@pytest.mark.parametrize('ip, login, password, tunnel_name', [(DUT3['host_ip'], DUT3['login'], DUT3['password'], 'to_atAR2')])
def test_show_mpls_rsvp_tunnels_lsp_tunnel_e2e_part14_5 (ip, login, password, tunnel_name): 
    allure.attach.file('./network-schemes/part14_5_show_mpls_rsvp_tunnels_lsp_e2e.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
    allure.attach.file('./network-schemes/part14_5_show_mpls_rsvp_tunnels_lsp_e2e_cmd.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('terminal datadump')
    cmd=('show mpls rsvp lsps tunnel %s'%tunnel_name)
    conn.execute(cmd)
    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels-lsp tunnel tunnel_name'
    resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp tunnel tunnel_name' c шаблоном в файле parse_show_mpls_rsvp_tunnels-lsp_tunnel_to_name_e2e.txt 
    template = open('./templates/parse_show_mpls_rsvp_lsps_tunnel_to_name_e2e.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    result = fsm.ParseText(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()

# Вывод команды 'show mpls rsvp lsps tunnel имя_туннеля' может на первое место выставить main LSP, а может backup LSP
# Поэтому делаем так:

    lsp1_signal_name=processed_result[0]['lsp_signal_name']
    if lsp1_signal_name=='to_atAR2@backup':
        lsp1_id=processed_result[0]['lsp_id']
        lsp1_src=processed_result[0]['lsp_src']
        lsp1_dst=processed_result[0]['lsp_dst']
        lsp1_state=processed_result[1]['lsp_state']
        lsp1_res_status=processed_result[1]['lsp_res_status']
        lsp1_protect_role=processed_result[1]['lsp_protect_role']
        lsp1_signal_int=processed_result[1]['lsp_signal_int']
        lsp1_ero_hop0=processed_result[2]['hop_number']
        lsp1_incoming_ero_hop0=processed_result[2]['incoming_ERO']
        lsp1_outgoing_ero_hop0=processed_result[2]['outgoing_ERO']
        lsp1_ero_hop1=processed_result[3]['hop_number']
        lsp1_incoming_ero_hop1=processed_result[3]['incoming_ERO']
        lsp1_outgoing_ero_hop1=processed_result[3]['outgoing_ERO']
        lsp1_ero_hop2=processed_result[4]['hop_number']
        lsp1_incoming_ero_hop2=processed_result[4]['incoming_ERO']
        lsp1_outgoing_ero_hop2=processed_result[4]['outgoing_ERO']
        lsp1_ero_hop3=processed_result[5]['hop_number']
        lsp1_incoming_ero_hop3=processed_result[5]['incoming_ERO']
        lsp1_outgoing_ero_hop3=processed_result[5]['outgoing_ERO']

        lsp1_rro_hop0=processed_result[6]['hop_number']
        lsp1_incoming_rro_hop0=processed_result[6]['incoming_RRO']
        lsp1_outgoing_rro_hop0=processed_result[6]['outgoing_RRO']
        lsp1_rro_hop1=processed_result[7]['hop_number']
        lsp1_incoming_rro_hop1=processed_result[7]['incoming_RRO']
        lsp1_outgoing_rro_hop1=processed_result[7]['outgoing_RRO']
        lsp1_rro_hop2=processed_result[8]['hop_number']
        lsp1_incoming_rro_hop2=processed_result[8]['incoming_RRO']
        lsp1_outgoing_rro_hop2=processed_result[8]['outgoing_RRO']
        lsp1_rro_hop3=processed_result[9]['hop_number']
        lsp1_incoming_rro_hop3=processed_result[9]['incoming_RRO']
        lsp1_outgoing_rro_hop3=processed_result[9]['outgoing_RRO']
        
        lsp2_signal_name=processed_result[10]['lsp_signal_name']
        lsp2_id=processed_result[10]['lsp_id']
        lsp2_src=processed_result[10]['lsp_src']
        lsp2_dst=processed_result[10]['lsp_dst']
        lsp2_state=processed_result[11]['lsp_state']
        lsp2_res_status=processed_result[11]['lsp_res_status']
        lsp2_protect_role=processed_result[11]['lsp_protect_role']
        lsp2_signal_int=processed_result[11]['lsp_signal_int']
        lsp2_ero_hop0=processed_result[12]['hop_number']
        lsp2_incoming_ero_hop0=processed_result[12]['incoming_ERO']
        lsp2_outgoing_ero_hop0=processed_result[12]['outgoing_ERO']
        lsp2_ero_hop1=processed_result[13]['hop_number']
        lsp2_incoming_ero_hop1=processed_result[13]['incoming_ERO']
        lsp2_outgoing_ero_hop1=processed_result[13]['outgoing_ERO']
        lsp2_rro_hop0=processed_result[14]['hop_number']
        lsp2_incoming_rro_hop0=processed_result[14]['incoming_RRO']
        lsp2_outgoing_rro_hop0=processed_result[14]['outgoing_RRO']
        lsp2_rro_hop1=processed_result[15]['hop_number']
        lsp2_incoming_rro_hop1=processed_result[15]['incoming_RRO']
        lsp2_outgoing_rro_hop1=processed_result[15]['outgoing_RRO']

        assert_that(lsp1_id!='',"Параметр LSP ID у RSVP LSP %s не равен значению опреденному в шаблоне, вместо этого он равен %s"%(lsp1_signal_name,lsp1_id))
        assert_that(lsp1_src=='1.0.0.1',"Параметр Source у RSVP LSP %s не равен ожидаемому значению 1.0.0.1, вместо этого он равен %s"%(lsp1_signal_name,lsp1_src))
        assert_that(lsp1_dst=='1.0.0.2',"Параметр Destination у RSVP LSP %s не равен ожидаемому значению 1.0.0.2, вместо этого он равен %s"%(lsp1_signal_name,lsp1_dst))
        assert_that(lsp1_state=='up',"Параметр State у RSVP LSP %s не равен ожидаемому значению UP, вместо этого он равен %s"%(lsp1_signal_name,lsp1_state))
        assert_that(lsp1_res_status=='standby',"Параметр Resource status у RSVP LSP %s не равен ожидаемому значению standby, вместо этого он равен %s"%(lsp1_signal_name,lsp1_res_status))
        assert_that(lsp1_protect_role=='protecting',"Параметр Protection role у RSVP LSP %s не равен ожидаемому значению protecting, вместо этого он равен %s"%(lsp1_signal_name,lsp1_protect_role))
        assert_that(lsp1_signal_int=='Bundle-ether1',"Параметр Signaling interface у RSVP LSP %s не равен ожидаемому значению Bundle-ether1, вместо этого он равен %s"%(lsp1_signal_name,lsp1_signal_int))
        assert_that(lsp1_ero_hop0=='hop0' and lsp1_incoming_ero_hop0=='192.168.55.2/32' and lsp1_outgoing_ero_hop0=='192.168.55.1/32',"Параметры hop0, incoming_ERO_hop0, outgoing_ERO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.2/32, 192.168.55.1/32, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_ero_hop0,lsp1_incoming_ero_hop0,lsp1_outgoing_ero_hop0))
        assert_that(lsp1_ero_hop1=='hop1' and lsp1_incoming_ero_hop1=='192.168.55.1/32' and lsp1_outgoing_ero_hop1=='192.168.55.21/32',"Параметры hop1, incoming_ERO_hop1, outgoing_ERO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, 192.168.55.1/32, 192.168.55.21/32, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_ero_hop1,lsp1_incoming_ero_hop1,lsp1_outgoing_ero_hop1))
        assert_that(lsp1_ero_hop2=='hop2' and lsp1_incoming_ero_hop2=='192.168.55.21/32' and lsp1_outgoing_ero_hop2=='192.168.55.22/32',"Параметры hop2, incoming_ERO_hop2, outgoing_ERO_hop2 у RSVP LSP %s не равны ожидаемым значениям hop2, 192.168.55.21/32, 192.168.55.22/32, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_ero_hop2,lsp1_incoming_ero_hop2,lsp1_outgoing_ero_hop2))
        assert_that(lsp1_ero_hop3=='hop3' and lsp1_incoming_ero_hop3=='192.168.55.22/32' and lsp1_outgoing_ero_hop3=='',"Параметры hop3, incoming_ERO_hop3, outgoing_ERO_hop3 у RSVP LSP %s не равны ожидаемым значениям hop3, 192.168.55.22/32, '', вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_ero_hop3,lsp1_incoming_ero_hop3,lsp1_outgoing_ero_hop3))

        assert_that(lsp1_rro_hop0=='hop0' and lsp1_incoming_rro_hop0=='192.168.55.1' and lsp1_outgoing_rro_hop0=='192.168.55.1',"Параметры hop0, incoming_RRO_hop0, outgoing_RRO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.1, 192.168.55.1, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_rro_hop0,lsp1_incoming_rro_hop0,lsp1_outgoing_rro_hop0))
        assert_that(lsp1_rro_hop1=='hop1' and lsp1_incoming_rro_hop1!='' and lsp1_outgoing_rro_hop1!='',"Параметры hop1, incoming_RRO_hop1, outgoing_RRO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, Label N, Label N, определенным в шаблоне, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_rro_hop1,lsp1_incoming_rro_hop1,lsp1_outgoing_rro_hop1))
        assert_that(lsp1_rro_hop2=='hop2' and lsp1_incoming_rro_hop2=='192.168.55.22' and lsp1_outgoing_rro_hop2=='192.168.55.22',"Параметры hop2, incoming_RRO_hop2, outgoing_RRO_hop2 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.22, 192.168.55.22, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_rro_hop2,lsp1_incoming_rro_hop2,lsp1_outgoing_rro_hop2))
        assert_that(lsp1_rro_hop3=='hop3' and lsp1_incoming_rro_hop3!='' and lsp1_outgoing_rro_hop3!='',"Параметры hop3, incoming_RRO_hop3, outgoing_RRO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop3, Label N, Label N, определенным в шаблоне, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_rro_hop3,lsp1_incoming_rro_hop3,lsp1_outgoing_rro_hop3))

        assert_that(lsp2_id!='',"Параметр LSP ID у RSVP LSP %s не равен значению опреденному в шаблоне, вместо этого он равен %s"%(lsp2_signal_name,lsp2_id))
        assert_that(lsp2_src=='1.0.0.1',"Параметр Source у RSVP LSP %s не равен ожидаемому значению 1.0.0.1, вместо этого он равен %s"%(lsp2_signal_name,lsp2_src))
        assert_that(lsp2_dst=='1.0.0.2',"Параметр Destination у RSVP LSP %s не равен ожидаемому значению 1.0.0.2, вместо этого он равен %s"%(lsp2_signal_name,lsp2_dst))
        assert_that(lsp2_state=='up',"Параметр State у RSVP LSP %s не равен ожидаемому значению UP, вместо этого он равен %s"%(lsp2_signal_name,lsp2_state))
        assert_that(lsp2_res_status=='active',"Параметр Resource status у RSVP LSP %s не равен ожидаемому значению active, вместо этого он равен %s"%(lsp2_signal_name,lsp2_res_status))
        assert_that(lsp2_protect_role=='working',"Параметр Protection role у RSVP LSP %s не равен ожидаемому значению working, вместо этого он равен %s"%(lsp2_signal_name,lsp2_protect_role))
        assert_that(lsp2_signal_int=='Bundle-ether2',"Параметр Signaling interface у RSVP LSP %s не равен ожидаемому значению Bundle-ether2, вместо этого он равен %s"%(lsp2_signal_name,lsp2_signal_int))
        assert_that(lsp2_ero_hop0=='hop0' and lsp2_incoming_ero_hop0=='192.168.55.5/32' and lsp2_outgoing_ero_hop0=='192.168.55.6/32',"Параметры hop0, incoming_ERO_hop0, outgoing_ERO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.5/32, 192.168.55.6/32, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_ero_hop0,lsp2_incoming_ero_hop0,lsp2_outgoing_ero_hop0))
        assert_that(lsp2_ero_hop1=='hop1' and lsp2_incoming_ero_hop1=='192.168.55.6/32' and lsp2_outgoing_ero_hop1=='',"Параметры hop1, incoming_ERO_hop1, outgoing_ERO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, 192.168.55.6/32, '', вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_ero_hop1,lsp2_incoming_ero_hop1,lsp2_outgoing_ero_hop1))

        assert_that(lsp2_rro_hop0=='hop0' and lsp2_incoming_rro_hop0=='192.168.55.6' and lsp2_outgoing_rro_hop0=='192.168.55.6',"Параметры hop0, incoming_RRO_hop0, outgoing_RRO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.6, 192.168.55.6, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_rro_hop0,lsp2_incoming_rro_hop0,lsp2_outgoing_rro_hop0))
        assert_that(lsp2_rro_hop1=='hop1' and lsp2_incoming_rro_hop1!='' and lsp2_outgoing_rro_hop1!='',"Параметры hop1, incoming_RRO_hop1, outgoing_RRO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, Label N, Label N, определенным в шаблоне, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_rro_hop1,lsp2_incoming_rro_hop1,lsp2_outgoing_rro_hop1))
    elif lsp1_signal_name=='to_atAR2@main':
        lsp1_signal_name=processed_result[10]['lsp_signal_name']
        lsp1_id=processed_result[0]['lsp_id']
        lsp1_src=processed_result[0]['lsp_src']
        lsp1_dst=processed_result[0]['lsp_dst']
        lsp1_state=processed_result[1]['lsp_state']
        lsp1_res_status=processed_result[1]['lsp_res_status']
        lsp1_protect_role=processed_result[1]['lsp_protect_role']
        lsp1_signal_int=processed_result[1]['lsp_signal_int']
        lsp1_ero_hop0=processed_result[2]['hop_number']
        lsp1_incoming_ero_hop0=processed_result[2]['incoming_ERO']
        lsp1_outgoing_ero_hop0=processed_result[2]['outgoing_ERO']
        lsp1_ero_hop1=processed_result[3]['hop_number']
        lsp1_incoming_ero_hop1=processed_result[3]['incoming_ERO']
        lsp1_outgoing_ero_hop1=processed_result[3]['outgoing_ERO']
        lsp1_rro_hop0=processed_result[4]['hop_number']
        lsp1_incoming_rro_hop0=processed_result[4]['incoming_RRO']
        lsp1_outgoing_rro_hop0=processed_result[4]['outgoing_RRO']
        lsp1_rro_hop1=processed_result[5]['hop_number']
        lsp1_incoming_rro_hop1=processed_result[5]['incoming_RRO']
        lsp1_outgoing_rro_hop1=processed_result[5]['outgoing_RRO']

        assert_that(lsp1_id!='',"Параметр LSP ID у RSVP LSP %s не равен значению опреденному в шаблоне, вместо этого он равен %s"%(lsp1_signal_name,lsp1_id))
        assert_that(lsp1_src=='1.0.0.1',"Параметр Source у RSVP LSP %s не равен ожидаемому значению 1.0.0.1, вместо этого он равен %s"%(lsp1_signal_name,lsp1_src))
        assert_that(lsp1_dst=='1.0.0.2',"Параметр Destination у RSVP LSP %s не равен ожидаемому значению 1.0.0.2, вместо этого он равен %s"%(lsp1_signal_name,lsp1_dst))
        assert_that(lsp1_state=='up',"Параметр State у RSVP LSP %s не равен ожидаемому значению UP, вместо этого он равен %s"%(lsp1_signal_name,lsp1_state))
        assert_that(lsp1_res_status=='active',"Параметр Resource status у RSVP LSP %s не равен ожидаемому значению active, вместо этого он равен %s"%(lsp1_signal_name,lsp1_res_status))
        assert_that(lsp1_protect_role=='working',"Параметр Protection role у RSVP LSP %s не равен ожидаемому значению working, вместо этого он равен %s"%(lsp1_signal_name,lsp1_protect_role))
        assert_that(lsp1_signal_int=='Bundle-ether2',"Параметр Signaling interface у RSVP LSP %s не равен ожидаемому значению Bundle-ether2, вместо этого он равен %s"%(lsp1_signal_name,lsp1_signal_int))
        assert_that(lsp1_ero_hop0=='hop0' and lsp1_incoming_ero_hop0=='192.168.55.5/32' and lsp1_outgoing_ero_hop0=='192.168.55.6/32',"Параметры hop0, incoming_ERO_hop0, outgoing_ERO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.5/32, 192.168.55.6/32, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_ero_hop0,lsp1_incoming_ero_hop0,lsp1_outgoing_ero_hop0))
        assert_that(lsp1_ero_hop1=='hop1' and lsp1_incoming_ero_hop1=='192.168.55.6/32' and lsp1_outgoing_ero_hop1=='',"Параметры hop1, incoming_ERO_hop1, outgoing_ERO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, 192.168.55.6/32, '', вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_ero_hop1,lsp1_incoming_ero_hop1,lsp1_outgoing_ero_hop1))

        assert_that(lsp1_rro_hop0=='hop0' and lsp1_incoming_rro_hop0=='192.168.55.6' and lsp1_outgoing_rro_hop0=='192.168.55.6',"Параметры hop0, incoming_RRO_hop0, outgoing_RRO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.6, 192.168.55.6, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_rro_hop0,lsp1_incoming_rro_hop0,lsp1_outgoing_rro_hop0))
        assert_that(lsp1_rro_hop1=='hop1' and lsp1_incoming_rro_hop1!='' and lsp1_outgoing_rro_hop1!='',"Параметры hop1, incoming_RRO_hop1, outgoing_RRO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, Label N, Label N, определенным в шаблоне, вместо этого они равны %s %s %s"%(lsp1_signal_name,lsp1_rro_hop1,lsp1_incoming_rro_hop1,lsp1_outgoing_rro_hop1))

        lsp2_signal_name=processed_result[6]['lsp_signal_name']
        lsp2_id=processed_result[6]['lsp_id']
        lsp2_src=processed_result[6]['lsp_src']
        lsp2_dst=processed_result[6]['lsp_dst']
        lsp2_state=processed_result[7]['lsp_state']
        lsp2_res_status=processed_result[7]['lsp_res_status']
        lsp2_protect_role=processed_result[7]['lsp_protect_role']
        lsp2_signal_int=processed_result[7]['lsp_signal_int']
        lsp2_ero_hop0=processed_result[8]['hop_number']
        lsp2_incoming_ero_hop0=processed_result[8]['incoming_ERO']
        lsp2_outgoing_ero_hop0=processed_result[8]['outgoing_ERO']
        lsp2_ero_hop1=processed_result[9]['hop_number']
        lsp2_incoming_ero_hop1=processed_result[9]['incoming_ERO']
        lsp2_outgoing_ero_hop1=processed_result[9]['outgoing_ERO']
        lsp2_ero_hop2=processed_result[10]['hop_number']
        lsp2_incoming_ero_hop2=processed_result[10]['incoming_ERO']
        lsp2_outgoing_ero_hop2=processed_result[10]['outgoing_ERO']
        lsp2_ero_hop3=processed_result[11]['hop_number']
        lsp2_incoming_ero_hop3=processed_result[11]['incoming_ERO']
        lsp2_outgoing_ero_hop3=processed_result[11]['outgoing_ERO']

        lsp2_rro_hop0=processed_result[12]['hop_number']
        lsp2_incoming_rro_hop0=processed_result[12]['incoming_RRO']
        lsp2_outgoing_rro_hop0=processed_result[12]['outgoing_RRO']
        lsp2_rro_hop1=processed_result[13]['hop_number']
        lsp2_incoming_rro_hop1=processed_result[13]['incoming_RRO']
        lsp2_outgoing_rro_hop1=processed_result[13]['outgoing_RRO']
        lsp2_rro_hop2=processed_result[14]['hop_number']
        lsp2_incoming_rro_hop2=processed_result[14]['incoming_RRO']
        lsp2_outgoing_rro_hop2=processed_result[14]['outgoing_RRO']
        lsp2_rro_hop3=processed_result[15]['hop_number']
        lsp2_incoming_rro_hop3=processed_result[15]['incoming_RRO']
        lsp2_outgoing_rro_hop3=processed_result[15]['outgoing_RRO']

        assert_that(lsp2_id!='',"Параметр LSP ID у RSVP LSP %s не равен значению опреденному в шаблоне, вместо этого он равен %s"%(lsp2_signal_name,lsp2_id))
        assert_that(lsp2_src=='1.0.0.1',"Параметр Source у RSVP LSP %s не равен ожидаемому значению 1.0.0.1, вместо этого он равен %s"%(lsp2_signal_name,lsp2_src))
        assert_that(lsp2_dst=='1.0.0.2',"Параметр Destination у RSVP LSP %s не равен ожидаемому значению 1.0.0.2, вместо этого он равен %s"%(lsp2_signal_name,lsp2_dst))
        assert_that(lsp2_state=='up',"Параметр State у RSVP LSP %s не равен ожидаемому значению UP, вместо этого он равен %s"%(lsp2_signal_name,lsp2_state))
        assert_that(lsp2_res_status=='standby',"Параметр Resource status у RSVP LSP %s не равен ожидаемому значению standby, вместо этого он равен %s"%(lsp2_signal_name,lsp2_res_status))
        assert_that(lsp2_protect_role=='protecting',"Параметр Protection role у RSVP LSP %s не равен ожидаемому значению protecting, вместо этого он равен %s"%(lsp2_signal_name,lsp2_protect_role))
        assert_that(lsp2_signal_int=='Bundle-ether1',"Параметр Signaling interface у RSVP LSP %s не равен ожидаемому значению Bundle-ether1, вместо этого он равен %s"%(lsp2_signal_name,lsp2_signal_int))
        assert_that(lsp2_ero_hop0=='hop0' and lsp2_incoming_ero_hop0=='192.168.55.2/32' and lsp2_outgoing_ero_hop0=='192.168.55.1/32',"Параметры hop0, incoming_ERO_hop0, outgoing_ERO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.2/32, 192.168.55.1/32, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_ero_hop0,lsp2_incoming_ero_hop0,lsp2_outgoing_ero_hop0))
        assert_that(lsp2_ero_hop1=='hop1' and lsp2_incoming_ero_hop1=='192.168.55.1/32' and lsp2_outgoing_ero_hop1=='192.168.55.21/32',"Параметры hop1, incoming_ERO_hop1, outgoing_ERO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, 192.168.55.1/32, 192.168.55.21/32, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_ero_hop1,lsp2_incoming_ero_hop1,lsp2_outgoing_ero_hop1))
        assert_that(lsp2_ero_hop2=='hop2' and lsp2_incoming_ero_hop2=='192.168.55.21/32' and lsp2_outgoing_ero_hop2=='192.168.55.22/32',"Параметры hop2, incoming_ERO_hop2, outgoing_ERO_hop2 у RSVP LSP %s не равны ожидаемым значениям hop2, 192.168.55.21/32, 192.168.55.22/32, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_ero_hop2,lsp2_incoming_ero_hop2,lsp2_outgoing_ero_hop2))
        assert_that(lsp2_ero_hop3=='hop3' and lsp2_incoming_ero_hop3=='192.168.55.22/32' and lsp2_outgoing_ero_hop3=='',"Параметры hop3, incoming_ERO_hop3, outgoing_ERO_hop3 у RSVP LSP %s не равны ожидаемым значениям hop3, 192.168.55.22/32, '', вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_ero_hop3,lsp2_incoming_ero_hop3,lsp2_outgoing_ero_hop3))

        assert_that(lsp2_rro_hop0=='hop0' and lsp2_incoming_rro_hop0=='192.168.55.1' and lsp2_outgoing_rro_hop0=='192.168.55.1',"Параметры hop0, incoming_RRO_hop0, outgoing_RRO_hop0 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.1, 192.168.55.1, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_rro_hop0,lsp2_incoming_rro_hop0,lsp2_outgoing_rro_hop0))
        assert_that(lsp2_rro_hop1=='hop1' and lsp2_incoming_rro_hop1!='' and lsp2_outgoing_rro_hop1!='',"Параметры hop1, incoming_RRO_hop1, outgoing_RRO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop1, Label N, Label N, определенным в шаблоне, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_rro_hop1,lsp2_incoming_rro_hop1,lsp2_outgoing_rro_hop1))
        assert_that(lsp2_rro_hop2=='hop2' and lsp2_incoming_rro_hop2=='192.168.55.22' and lsp2_outgoing_rro_hop2=='192.168.55.22',"Параметры hop2, incoming_RRO_hop2, outgoing_RRO_hop2 у RSVP LSP %s не равны ожидаемым значениям hop0, 192.168.55.22, 192.168.55.22, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_rro_hop2,lsp2_incoming_rro_hop2,lsp2_outgoing_rro_hop2))
        assert_that(lsp2_rro_hop3=='hop3' and lsp2_incoming_rro_hop3!='' and lsp2_outgoing_rro_hop3!='',"Параметры hop3, incoming_RRO_hop3, outgoing_RRO_hop1 у RSVP LSP %s не равны ожидаемым значениям hop3, Label N, Label N, определенным в шаблоне, вместо этого они равны %s %s %s"%(lsp2_signal_name,lsp2_rro_hop3,lsp2_incoming_rro_hop3,lsp2_outgoing_rro_hop3))

    else :
        assert_that(False, "Имя первого RSVP LSP в выводе команды не соответствует ожидаемым значениям")


