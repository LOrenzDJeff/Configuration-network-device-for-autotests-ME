from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.1: Функциональное тестирование show-команд протокола RSVP-TE')
@allure.title('Проверка вывода команды show mpls rsvp tunnels имя_туннеля')
@pytest.mark.part14_1
@pytest.mark.show_rsvp_tunnel_name
@pytest.mark.parametrize('ip, login, password, tun_name', [(DUT3['host_ip'], DUT3['login'], DUT3['password'],'to_vMX-1'),(DUT2['host_ip'], DUT2['login'], DUT2['password'],'to_atDR1'),(DUT1['host_ip'], DUT1['login'], DUT1['password'],'to_atAR2') ])
def test_show_rsvp_tunnel_name_part14_1 (ip, login, password, tun_name):
    allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
#    allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_name.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG) 
    if ip==DUT1['host_ip']:
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_name_atAR1.png','Вывод команды', attachment_type=allure.attachment_type.PNG) 
    if ip==DUT2['host_ip']:
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_name_atAR2.png','Вывод команды', attachment_type=allure.attachment_type.PNG) 
    if ip==DUT3['host_ip']:
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_name_atDR1.png','Вывод команды', attachment_type=allure.attachment_type.PNG) 
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    cmd=('show mpls rsvp tunnels %s'%tun_name)
    conn.set_error_prompt(['Unknown command'])  # Меняем Error Prompt т.к. в выводе команды show mpls rsvp tunnels имя_туннеля могут быть строки начинающиеся на Error
    conn.execute(cmd)
    resp=conn.response
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'
    resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show route' c шаблоном в файле parse_show_mpls_rsvp_tunnel_name.txt 
    template = open('./templates/parse_show_mpls_rsvp_tunnel_name.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    result = fsm.ParseText(resp)
    conn.send('quit\r')
    conn.close()
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
#    tun_descr=processed_result[0]['tun_descr']
    tun_name=processed_result[0]['tun_name']
    tun_dst=processed_result[0]['tun_dst']    
#    tun_ingress_id=processed_result[0]['tun_ingress_id']
    tun_admin_status=processed_result[0]['tun_admin_status']
    tun_oper_status=processed_result[0]['tun_oper_status']
    tun_id=processed_result[0]['tun_id']
    

    if ip==DUT3['host_ip']:
        tun_descr=processed_result[0]['tun_descr']     
        assert_that(tun_descr=='from_atDR1_to_vMX',"Description ТЕ туннеля %s не соответствует значению from_atDR1_to_vMX"%tun_descr)
        tun_ingress_id=processed_result[0]['tun_ingress_id']        
        assert_that(tun_ingress_id=='1.0.0.1',"Ingress LSR ID ТЕ туннеля %s не соответствует значению 1.0.0.1"%tun_ingress_id)
        tun_egress_id=processed_result[0]['tun_egress_id']
        assert_that(tun_egress_id=='1.0.0.4',"Egress LSR ID ТЕ туннеля %s не соответствует значению 1.0.0.4"%tun_egress_id)
        tun_bandwidth=processed_result[0]['tun_bandwidth']
        assert_that(tun_bandwidth=='0',"Bandwidth  ТЕ туннеля %s не соответствует значению 0, а равно %s"%(tun_name,tun_bandwidth))
        tun_bandwidth_backup=processed_result[0]['tun_bandwidth_backup']
        assert_that(tun_bandwidth_backup=='0',"Bandwidth backup ТЕ туннеля %s не соответствует значению 0, а равно %s"%(tun_name,tun_bandwidth_backup))
        tun_protect_type=processed_result[0]['tun_protect_type']
        assert_that(tun_protect_type=='none',"Protection type ТЕ туннеля %s не соответствует значению none, а равно %s"%(tun_name,tun_protect_type))
        tun_band_protect_desire=processed_result[0]['tun_band_protect_desire']
        assert_that(tun_band_protect_desire=='disabled',"Флаг Bandwidth protection desire ТЕ туннеля %s не соответствует значению disabled, а равно %s"%(tun_name,tun_band_protect_desire))
        tun_node_protect=processed_result[0]['tun_node_protect']
        assert_that(tun_node_protect=='disabled',"Флаг Node protection  ТЕ туннеля %s не соответствует значению disabled, а равно %s"%(tun_name,tun_node_protect))
        tun_routing=processed_result[0]['tun_routing']
        assert_that(tun_routing=='no',"Флаг Routing adjacency ТЕ туннеля %s не соответствует значению no, а равно %s"%(tun_name,tun_routing))
        tun_forwarding=processed_result[0]['tun_forwarding']
        assert_that(tun_forwarding=='no',"Флаг Forwarding adjacency ТЕ туннеля %s не соответствует значению no, а равно %s"%(tun_name,tun_forwarding))
        tun_bidirect=processed_result[0]['tun_bidirect']
        assert_that(tun_bidirect=='not bidirectional',"Флаг bidirectional ТЕ туннеля %s не соответствует значению not bidirectional, а равно %s"%(tun_name,tun_bidirect))
        tun_prio_setup=processed_result[0]['tun_prio_setup']       
        assert_that(tun_prio_setup=='7',"Setup priority у LSP ТЕ туннеля %s не соответствует значению 7, а равно %s"%(tun_name,tun_prio_setup))
        tun_prio_hold=processed_result[0]['tun_prio_hold']
        assert_that(tun_prio_hold=='7',"Hold priority у LSP ТЕ туннеля %s не соответствует значению 7, а равно %s"%(tun_name,tun_prio_setup))
        tun_lsp_name=processed_result[0]['tun_lsp_name']
        assert_that(tun_lsp_name=='atDR1_to_vMX-lsp1',"Имя LSP ТЕ туннеля %s не соответствует значению atDR1_to_vMX-lsp1, а равно %s"%(tun_name,tun_lsp_name))
        tun_lsp_state=processed_result[0]['tun_lsp_state']
        assert_that(tun_lsp_state=='up',"Операционный статус LSP ТЕ туннеля %s не соответствует значению up, а равно %s"%(tun_name,tun_lsp_state))
        tun_lsp_id=processed_result[0]['tun_lsp_id']
        assert_that(tun_lsp_id!='',"LSP id ТЕ туннеля %s не соответствует шаблону"%tun_name)
        tun_lsp_computation=processed_result[0]['tun_lsp_computation']
        assert_that(tun_lsp_computation!='',"Способ вычисления пути для LSP ТЕ туннеля %s не соответствует одному из значений шаблона"%tun_name)
        tun_lsp_explicit_name=processed_result[0]['tun_lsp_explicit_name']
        assert_that(tun_lsp_explicit_name=='over_atAR1',"Имя explicit path, используемое для вычисления пути LSP ТЕ туннеля %s не соответствует значению over_atAR1, а равно %s"%(tun_name,tun_lsp_explicit_name))
    if ip==DUT1['host_ip']:
        tun_descr=processed_result[0]['tun_descr']
        assert_that(tun_descr=='from_atAR1_to_atAR2',"Description ТЕ туннеля %s не соответствует значению from_atAR1_to_atAR2, а равно %s"%(tun_name,tun_descr))
        tun_ingress_id=processed_result[0]['tun_ingress_id']
        assert_that(tun_ingress_id=='1.0.0.3',"Ingress LSR ID ТЕ туннеля %s не соответствует значению 1.0.0.3, а равно %s"%(tun_name,tun_ingress_id))
        tun_egress_id=processed_result[0]['tun_egress_id']
        assert_that(tun_egress_id=='1.0.0.2',"Egress LSR ID ТЕ туннеля %s не соответствует значению 1.0.0.2, а равно %s"%(tun_name,tun_egress_id))
        tun_bandwidth=processed_result[0]['tun_bandwidth']
        assert_that(tun_bandwidth=='0',"Bandwidth  ТЕ туннеля %s не соответствует значению 0, а равно %s"%(tun_name,tun_bandwidth))
        tun_bandwidth_backup=processed_result[0]['tun_bandwidth_backup']
        assert_that(tun_bandwidth_backup=='0',"Bandwidth backup ТЕ туннеля %s не соответствует значению 0, а равно %s"%(tun_name,tun_bandwidth_backup))
        tun_protect_type=processed_result[0]['tun_protect_type']
        assert_that(tun_protect_type=='none',"Protection type ТЕ туннеля %s не соответствует значению none, а равно %s"%(tun_name,tun_protect_type))
        tun_band_protect_desire=processed_result[0]['tun_band_protect_desire']
        assert_that(tun_band_protect_desire=='disabled',"Флаг Bandwidth protection desire ТЕ туннеля %s не соответствует значению disabled, а равно %s"%(tun_name,tun_band_protect_desire))
        tun_node_protect=processed_result[0]['tun_node_protect']
        assert_that(tun_node_protect=='disabled',"Флаг Node protection  ТЕ туннеля %s не соответствует значению disabled, а равно %s"%(tun_name,tun_node_protect))
        tun_routing=processed_result[0]['tun_routing']
        assert_that(tun_routing=='no',"Флаг Routing adjacency ТЕ туннеля %s не соответствует значению no, а равно %s"%(tun_name,tun_routing))
        tun_forwarding=processed_result[0]['tun_forwarding']
        assert_that(tun_forwarding=='no',"Флаг Forwarding adjacency ТЕ туннеля %s не соответствует значению no, а равно %s"%(tun_name,tun_forwarding))
        tun_bidirect=processed_result[0]['tun_bidirect']
        assert_that(tun_bidirect=='not bidirectional',"Флаг bidirectional ТЕ туннеля %s не соответствует значению not bidirectional, а равно %s"%(tun_name,tun_bidirect))
        tun_prio_setup=processed_result[0]['tun_prio_setup']
        assert_that(tun_prio_setup=='6',"Setup priority у LSP ТЕ туннеля %s не соответствует значению 6, а равно %s"%(tun_name,tun_prio_setup))
        tun_prio_hold=processed_result[0]['tun_prio_hold']
        assert_that(tun_prio_hold=='3',"Hold priority у LSP ТЕ туннеля %s не соответствует значению 3, а равно %s"%(tun_name,tun_prio_setup))
        tun_lsp_name=processed_result[0]['tun_lsp_name']
        assert_that(tun_lsp_name=='atAR1_to_atAR2-lsp1',"Имя LSP ТЕ туннеля %s не соответствует значению atDR1_to_vMX-lsp1, а равно %s"%(tun_name,tun_lsp_name))
        tun_lsp_state=processed_result[0]['tun_lsp_state']
        assert_that(tun_lsp_state=='up',"Операционный статус LSP ТЕ туннеля %s не соответствует значению up, а равно %s"%(tun_name,tun_lsp_state))
        tun_lsp_id=processed_result[0]['tun_lsp_id']
        assert_that(tun_lsp_id!='',"LSP id ТЕ туннеля %s не соответствует шаблону"%tun_name)
        tun_lsp_computation=processed_result[0]['tun_lsp_computation']
        assert_that(tun_lsp_computation!='',"Способ вычисления пути для LSP ТЕ туннеля %s не соответствует одному из значений шаблона"%tun_name)
        tun_lsp_explicit_name=processed_result[0]['tun_lsp_explicit_name']
        assert_that(tun_lsp_explicit_name=='directly_toatAR2',"Имя explicit path, используемое для вычисления пути LSP ТЕ туннеля %s не соответствует значению directly_toatAR2, а равно %s"%(tun_name,tun_lsp_explicit_name))
    if ip==DUT2['host_ip']:
        tun_descr=processed_result[0]['tun_descr']
        assert_that(tun_descr=='from_atAR2_to_atDR1',"Description ТЕ туннеля %s не соответствует значению from_atAR2_to_atDR1, а равно %s"%(tun_name,tun_descr))
        tun_ingress_id=processed_result[0]['tun_ingress_id']
        assert_that(tun_ingress_id=='1.0.0.2',"Ingress LSR ID ТЕ туннеля %s не соответствует значению 1.0.0.2, а равно %s"%(tun_name,tun_ingress_id))
        tun_egress_id=processed_result[0]['tun_egress_id']
        assert_that(tun_egress_id=='1.0.0.1',"Egress LSR ID ТЕ туннеля %s не соответствует значению 1.0.0.1, а равно %s"%(tun_name,tun_egress_id))
        tun_bandwidth=processed_result[0]['tun_bandwidth']
        assert_that(tun_bandwidth=='8',"Bandwidth  ТЕ туннеля %s не соответствует значению 8 Mbps, а равно %s"%(tun_name,tun_bandwidth))
        tun_bandwidth_backup=processed_result[0]['tun_bandwidth_backup']
        assert_that(tun_bandwidth_backup=='0',"Bandwidth backup ТЕ туннеля %s не соответствует значению 0, а равно %s"%(tun_name,tun_bandwidth_backup))
        tun_protect_type=processed_result[0]['tun_protect_type']
        assert_that(tun_protect_type=='none',"Protection type ТЕ туннеля %s не соответствует значению none, а равно %s"%(tun_name,tun_protect_type))
        tun_band_protect_desire=processed_result[0]['tun_band_protect_desire']
        assert_that(tun_band_protect_desire=='disabled',"Флаг Bandwidth protection desire ТЕ туннеля %s не соответствует значению disabled, а равно %s"%(tun_name,tun_band_protect_desire))
        tun_node_protect=processed_result[0]['tun_node_protect']
        assert_that(tun_node_protect=='disabled',"Флаг Node protection  ТЕ туннеля %s не соответствует значению disabled, а равно %s"%(tun_name,tun_node_protect))
        tun_routing=processed_result[0]['tun_routing']
        assert_that(tun_routing=='yes',"Флаг Routing adjacency ТЕ туннеля %s не соответствует значению yes, а равно %s"%(tun_name,tun_routing))
        tun_forwarding=processed_result[0]['tun_forwarding']
        assert_that(tun_forwarding=='yes',"Флаг Forwarding adjacency ТЕ туннеля %s не соответствует значению yes, а равно %s"%(tun_name,tun_forwarding))
        tun_bidirect=processed_result[0]['tun_bidirect']
        assert_that(tun_bidirect=='not bidirectional',"Флаг bidirectional ТЕ туннеля %s не соответствует значению not bidirectional, а равно %s"%(tun_name,tun_bidirect))
        tun_prio_setup=processed_result[0]['tun_prio_setup']
        assert_that(tun_prio_setup=='1',"Setup priority у LSP ТЕ туннеля %s не соответствует значению 1, а равно %s"%(tun_name,tun_prio_setup))
        tun_prio_hold=processed_result[0]['tun_prio_hold']
        assert_that(tun_prio_hold=='0',"Hold priority у LSP ТЕ туннеля %s не соответствует значению 0, а равно %s"%(tun_name,tun_prio_setup))
        tun_lsp_name=processed_result[0]['tun_lsp_name']
        assert_that(tun_lsp_name=='atAR2_to_atDR1-lsp1',"Имя LSP ТЕ туннеля %s не соответствует значению atAR2_to_atDR1-lsp1, а равно %s"%(tun_name,tun_lsp_name))
        tun_lsp_state=processed_result[0]['tun_lsp_state']
        assert_that(tun_lsp_state=='up',"Операционный статус LSP ТЕ туннеля %s не соответствует значению up, а равно %s"%(tun_name,tun_lsp_state))
        tun_lsp_id=processed_result[0]['tun_lsp_id']
        assert_that(tun_lsp_id!='',"LSP id ТЕ туннеля %s не соответствует шаблону"%tun_name)
        tun_lsp_computation=processed_result[0]['tun_lsp_computation']
        assert_that(tun_lsp_computation!='',"Способ вычисления пути для LSP ТЕ туннеля %s не соответствует одному из значений шаблона"%tun_name)
        tun_lsp_explicit_name=processed_result[0]['tun_lsp_explicit_name']
        assert_that(tun_lsp_explicit_name=='over_atAR1',"Имя explicit path, используемое для вычисления пути LSP ТЕ туннеля %s не соответствует значению over_atAR1, а равно %s"%(tun_name,tun_lsp_explicit_name))

