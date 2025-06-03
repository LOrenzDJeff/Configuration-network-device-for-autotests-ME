from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.1: Функциональное тестирование show-команд протокола RSVP-TE')
@allure.title('Проверка вывода команды show mpls rsvp tunnels-lsp')
@pytest.mark.part14_1
@pytest.mark.show_rsvp_lsp
@pytest.mark.parametrize('ip, login, password', [(DUT3['host_ip'], DUT3['login'], DUT3['password']),(DUT2['host_ip'], DUT2['login'], DUT2['password']),(DUT1['host_ip'], DUT1['login'], DUT1['password'])])
def test_show_rsvp_tunnel_lsp_part14_1 (ip, login, password):
    allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    if ip == DUT3['host_ip']:
        conn.set_prompt('atDR1#')
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel-lsp_atDR1.png','Вывод команды', attachment_type=allure.attachment_type.PNG)         
    elif ip == DUT2['host_ip']:
        conn.set_prompt('atAR2#')
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel-lsp_atAR2.png','Вывод команды', attachment_type=allure.attachment_type.PNG)        
    elif ip == DUT1['host_ip']:
        conn.set_prompt('atAR1#')
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel-lsp_atAR1.png','Вывод команды', attachment_type=allure.attachment_type.PNG)
    conn.execute('terminal datadump')
    cmd=('show mpls rsvp lsps')
    conn.execute(cmd)
    resp=conn.response
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'    
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_show_mpls_rsvp_lsp.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)    
#    result = fsm.ParseText(resp)
    conn.send('quit\r')
    conn.close()
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
# Попробуем найти LSP по имени в словаре который сформировался после парсинга    
    loc_index=0
    if ip==DUT3['host_ip']:
        located_index1=locate_index_in_ListOfDict(processed_result,'lsp_name','to_vMX-1@atDR1_to_vMX-lsp1', loc_index)
        located_index2=locate_index_in_ListOfDict(processed_result,'lsp_name','to_atDR1@atAR2_to_atDR1-lsp1', loc_index)
        assert_that(located_index1!=999,"LSP с именем to_vMX-1@atDR1_to_vMX-lsp1 не обнаружен в выводе команды")
        assert_that(located_index2!=999,"LSP с именем to_atDR1@atAR2_to_atDR1-lsp1 не обнаружен в выводе команды")    
    if ip==DUT2['host_ip']:
        located_index1=locate_index_in_ListOfDict(processed_result,'lsp_name','to_atDR1@atAR2_to_atDR1-lsp1', loc_index)
        located_index2=locate_index_in_ListOfDict(processed_result,'lsp_name','to_atAR2@atAR1_to_atAR2-lsp1', loc_index)
        assert_that(located_index1!=999,"LSP с именем to_atDR1@atAR2_to_atDR1-lsp1 не обнаружен в выводе команды")
        assert_that(located_index2!=999,"LSP с именем to_atAR2@atAR1_to_atAR2-lsp1 не обнаружен в выводе команды")    

    if ip==DUT1['host_ip']:
        located_index1=locate_index_in_ListOfDict(processed_result,'lsp_name','to_vMX-1@atDR1_to_vMX-lsp1', loc_index)
        located_index2=locate_index_in_ListOfDict(processed_result,'lsp_name','to_atDR1@atAR2_to_atDR1-lsp1', loc_index)
        assert_that(located_index1!=999,"LSP с именем to_vMX-1@atDR1_to_vMX-lsp1 не обнаружен в выводе команды")
        assert_that(located_index2!=999,"LSP с именем to_atDR1@atAR2_to_atDR1-lsp1 не обнаружен в выводе команды")    




#    Top=processed_result[0]['Top']
    lsp1_name=processed_result[located_index1]['lsp_name']
    lsp1_id=processed_result[located_index1]['lsp_id']
    lsp1_source=processed_result[located_index1]['lsp_source']
    lsp1_destination=processed_result[located_index1]['lsp_destination']
    lsp1_labels=processed_result[located_index1]['labels']
    lsp1_type=processed_result[located_index1]['lsp_type']
    lsp1_state=processed_result[located_index1]['lsp_state']

    lsp2_name=processed_result[located_index2]['lsp_name']
    lsp2_id=processed_result[located_index2]['lsp_id']
    lsp2_source=processed_result[located_index2]['lsp_source']
    lsp2_destination=processed_result[located_index2]['lsp_destination']
    lsp2_labels=processed_result[located_index2]['labels']
    lsp2_type=processed_result[located_index2]['lsp_type']
    lsp2_state=processed_result[located_index2]['lsp_state']
    

    if ip==DUT3['host_ip']:
        assert_that(lsp1_name=='to_vMX-1@atDR1_to_vMX-lsp1',"Имя RSVP LSP1 %s не соответствует ожидаемому значению to_vMX-1@atDR1_to_vMX-ls"%lsp1_name)
        assert_that(lsp1_id!='',"Значение LSP1 ID %s не соответствует шаблону"%lsp1_id)
        assert_that(lsp1_source=='1.0.0.1',"Значение LSP1 source %s не соответствует значению 1.0.0.1"%lsp1_source)
        assert_that(lsp1_destination=='1.0.0.4',"Значение LSP1 destination %s не соответствует значению 1.0.0.4"%lsp1_destination)
        assert_that(lsp1_labels!='',"Значение MPLS меток  %s для MPLS RSVP LSP1 не соответствует шаблону"%lsp1_labels)
        assert_that(lsp1_type!='',"Значение типа RSVP LSP1 %s не соответствует шаблону"%lsp1_type)
        
        assert_that(lsp2_name=='to_atDR1@atAR2_to_atDR1-lsp1',"Имя RSVP LSP2 %s не соответствует ожидаемому значению to_atDR1@atAR2_to_atDR1-"%lsp2_name)
        assert_that(lsp2_id!='',"Значение LSP2 ID %s не соответствует шаблону"%lsp2_id)
        assert_that(lsp2_source=='1.0.0.2',"Значение LSP2 source %s не соответствует значению 1.0.0.2"%lsp2_source)
        assert_that(lsp2_destination=='1.0.0.1',"Значение LSP2 destination %s не соответствует значению 1.0.0.1"%lsp2_destination)
        assert_that(lsp2_labels!='',"Значение MPLS меток %s для MPLS RSVP LSP2 не соответствует шаблону"%lsp2_labels)
        assert_that(lsp2_type!='',"Значение типа RSVP LSP2 %s не соответствует шаблону"%lsp2_type)

    elif ip==DUT2['host_ip']:
        assert_that(lsp1_name=='to_atDR1@atAR2_to_atDR1-lsp1',"Имя RSVP LSP1 %s не соответствует ожидаемому значению to_atDR1@atAR2_to_atDR1-lsp1"%lsp1_name)
        assert_that(lsp1_id!='',"Значение LSP1 ID %s не соответствует шаблону"%lsp1_id)
        assert_that(lsp1_source=='1.0.0.2',"Значение LSP1 source %s не соответствует значению 1.0.0.2"%lsp1_source)
        assert_that(lsp1_destination=='1.0.0.1',"Значение LSP1 destination %s не соответствует значению 1.0.0.1"%lsp1_destination)
        assert_that(lsp1_labels!='',"Значение MPLS меток  %s для MPLS RSVP LSP1 не соответствует шаблону"%lsp1_labels)
        assert_that(lsp1_type!='',"Значение типа RSVP LSP1 %s не соответствует шаблону"%lsp1_type)

        assert_that(lsp2_name=='to_atAR2@atAR1_to_atAR2-lsp1',"Имя RSVP LSP2 %s не соответствует ожидаемому значению to_atAR2@atAR1_to_atAR2-lsp1"%lsp2_name)
        assert_that(lsp2_id!='',"Значение LSP2 ID %s не соответствует шаблону"%lsp2_id)
        assert_that(lsp2_source=='1.0.0.3',"Значение LSP2 source %s не соответствует значению 1.0.0.3"%lsp2_source)
        assert_that(lsp2_destination=='1.0.0.2',"Значение LSP2 destination %s не соответствует значению 1.0.0.2"%lsp2_destination)
        assert_that(lsp2_labels!='',"Значение MPLS меток %s для MPLS RSVP LSP2 не соответствует шаблону"%lsp2_labels)
        assert_that(lsp2_type!='',"Значение типа RSVP LSP2 %s не соответствует шаблону"%lsp2_type)
    elif ip==DUT1['host_ip']:
        assert_that(lsp1_name=='to_vMX-1@atDR1_to_vMX-lsp1',"Имя RSVP LSP1 %s не соответствует ожидаемому значению to_vMX-1@atDR1_to_vMX-ls"%lsp1_name)
        assert_that(lsp1_id!='',"Значение LSP1 ID %s не соответствует шаблону"%lsp1_id)
        assert_that(lsp1_source=='1.0.0.1',"Значение LSP1 source %s не соответствует значению 1.0.0.1"%lsp1_source)
        assert_that(lsp1_destination=='1.0.0.4',"Значение LSP1 destination %s не соответствует значению 1.0.0.4"%lsp1_destination)
        assert_that(lsp1_labels!='',"Значение MPLS меток  %s для MPLS RSVP LSP1 не соответствует шаблону"%lsp1_labels)
        assert_that(lsp1_type!='',"Значение типа RSVP LSP1 %s не соответствует шаблону"%lsp1_type)

        assert_that(lsp2_name=='to_atDR1@atAR2_to_atDR1-lsp1',"Имя RSVP LSP2 %s не соответствует ожидаемому значению to_atDR1@atAR2_to_atDR1-"%lsp2_name)
        assert_that(lsp2_id!='',"Значение LSP2 ID %s не соответствует шаблону"%lsp2_id)
        assert_that(lsp2_source=='1.0.0.2',"Значение LSP2 source %s не соответствует значению 1.0.0.2"%lsp2_source)
        assert_that(lsp2_destination=='1.0.0.1',"Значение LSP2 destination %s не соответствует значению 1.0.0.1"%lsp2_destination)
        assert_that(lsp2_labels!='',"Значение MPLS меток %s для MPLS RSVP LSP2 не соответствует шаблону"%lsp2_labels)
        assert_that(lsp2_type!='',"Значение типа RSVP LSP2 %s не соответствует шаблону"%lsp2_type)


    assert_that(lsp1_state=='up',"Статус RSVP LSP1 %s не соответствует ожидаемому значениею up"%lsp1_state)
    assert_that(lsp2_state=='up',"Статус RSVP LSP2 %s не соответствует ожидаемому значению up"%lsp2_state)

