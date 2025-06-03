from conftest import *

#debug_cmd_list=['debug pp-mgr cmd','debug pp-mgr general','debug pp-mgr mpls','debug pp-mgr int','debug pp-mgr hw-api']

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.4:Функциональное тестирование L2VPN over RSVP-TE')
@allure.title('Проверка вывода команды show l2vpn mac-table bridge-domain BD-TEST')
@pytest.mark.part14_4
@pytest.mark.mac_table_bd_rsvp
@pytest.mark.dependency(depends=["load_config144_dut1","load_config144_dut2","load_config144_dut3","load_config144_dut4"],scope='session')
#@pytest.mark.parametrize('ip, hostname, login, password, debug_cmd_list', [(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'], debug_cmd_list), (DUT3['host_ip'],DUT3['hostname'], DUT3['login'], DUT3['password'], debug_cmd_list)])
@pytest.mark.parametrize('ip, login, password', [(DUT2['host_ip'], DUT2['login'], DUT2['password']), (DUT3['host_ip'], DUT3['login'], DUT3['password'])])
def test_show_l2vpn_mac_table_bd_part14_4 (ip, login, password): 
#def test_show_l2vpn_mac_table_bd_part14_4 (me_open_debug_collect_logs, ip, hostname, login, password, debug_cmd_list): 
    allure.attach.file('./network-schemes/part14_4_show_l2vpn_mac_bd.png','Схема теста:', attachment_type=allure.attachment_type.PNG)

# Подключимся к atAR1 (он же CE1) и сгенерируем трафик чтобы MAC адреса в бридж домене изучились
    conn1 = Telnet()
    acc1 = Account(DUT1['login'] , DUT1['password'])
    conn1.connect(DUT1['host_ip'])
    conn1.login(acc1)
    conn1.execute('terminal datadump')
    cmd1=('ping 172.16.70.2 vrf CE1 count 20') # Увеличим кол-во пакетов до 20 чтобы MAC-ки успели изучиться
    conn1.execute(cmd1)
    conn1.send('quit\r')
    conn1.close()
# Конец генерации трафика

    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('terminal datadump')
    cmd=('show l2vpn mac-table bridge-domain BD-TEST')
    conn.execute(cmd) # первый раз выполняем пинг чтобы успели изучиться MAC адреса и не было потери первого пакета 
    conn.execute(cmd)
    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show l2vpn mac-table bridge-domain BD-TEST'
#    resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_show_l2vpn_mac_table_bd.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()
    # Попробуем найти MAC по значению в словаре который сформировался после парсинга    
    loc_index=0
    located_index1=locate_index_in_ListOfDict(processed_result,'CE_MAC','e0:d9:e3:df:35:96', loc_index)
    assert_that(located_index1!=999,"MAC адрес e0:d9:e3:df:35:96 не обнаружен в результатх парсинга")
    located_index2=locate_index_in_ListOfDict(processed_result,'CE_MAC','e0:d9:e3:df:35:97', loc_index)
    assert_that(located_index1!=999,"MAC адрес e0:d9:e3:df:35:97 не обнаружен в результатх парсинга")    

    Top=processed_result[0]['Top']
    MAC_CE1=processed_result[located_index1]['CE_MAC']
    MAC_CE1_type=processed_result[located_index1]['MAC_type']
    MAC_CE1_int_learn=processed_result[located_index1]['learned_int']
    MAC_CE1_location=processed_result[located_index1]['LC_loc']
    MAC_CE1_bd_name=processed_result[located_index1]['BD_name']

    MAC_CE2=processed_result[located_index2]['CE_MAC']
    MAC_CE2_type=processed_result[located_index2]['MAC_type']
    MAC_CE2_int_learn=processed_result[located_index2]['learned_int']
    MAC_CE2_location=processed_result[located_index2]['LC_loc']
    MAC_CE2_bd_name=processed_result[located_index2]['BD_name']
    assert_that(Top !='','Табличный заголовок в выводе команды не соответвует шаблону')
    assert_that(MAC_CE1=='e0:d9:e3:df:35:96',"Ожидаемый MAC e0:d9:e3:df:35:96 не изучен в домене BD-TESTS")
    assert_that(MAC_CE2=='e0:d9:e3:df:35:97',"Ожидаемый MAC e0:d9:e3:df:35:97 не изучен в домене BD-TESTS")
    assert_that(MAC_CE1_type=='Dynamic'," Тип адреса e0:d9:e3:df:35:96 не соответвует ожидаемому значению Dynamic, а равен %s"%MAC_CE1_type)
    assert_that(MAC_CE2_type=='Dynamic'," Тип адреса e0:d9:e3:df:35:97 не соответвует ожидаемому значению Dynamic, а равен %s"%MAC_CE2_type)
    assert_that(MAC_CE1_bd_name=='BD-TEST',"Имя домена в котором изучен e0:d9:e3:df:35:96 не соответвует ожидаемому значению BD-TEST, а равен %s"%MAC_CE1_bd_name)
    assert_that(MAC_CE2_bd_name=='BD-TEST',"Имя домена в котором изучен e0:d9:e3:df:35:97 не соответвует ожидаемому значению BD-TEST, а равен %s"%MAC_CE2_bd_name)

    if ip==DUT2['host_ip']:
    	assert_that(MAC_CE1_int_learn=='pw 1.0.0.1 123',"MAC адрес e0:d9:e3:df:35:96 изучен не на ожидаемом интерфейсе pw 1.0.0.1, а на %s"%MAC_CE1_int_learn)
    	assert_that(MAC_CE2_int_learn=='bu2.400',"MAC адрес e0:d9:e3:df:35:97 изучен не на ожидаемом интерфейсе bu2.400, а на %s"%MAC_CE2_int_learn)
    	assert_that(MAC_CE1_location=='0/0',"Параметр LC/Location для e0:d9:e3:df:35:96 не равен ожидаемому 0/0, а ревен %s"%MAC_CE1_location)
    	assert_that(MAC_CE2_location=='0/0',"Параметр LC/Location для e0:d9:e3:df:35:97 не равен ожидаемому 0/0, а ревен %s"%MAC_CE2_location)

    elif ip==DUT3['host_ip']:
        assert_that(MAC_CE1_int_learn=='bu1.300',"MAC адрес e0:d9:e3:df:35:96 изучен не на ожидаемом интерфейсе bu1.300, а на %s"%MAC_CE1_int_learn)
        assert_that(MAC_CE2_int_learn=='pw 1.0.0.2 123',"MAC адрес e0:d9:e3:df:35:97 изучен не на ожидаемом интерфейсе pw 1.0.0.2 123, а на %s"%MAC_CE2_int_learn)
        assert_that(MAC_CE1_location=='0/1',"Параметр LC/Location для e0:d9:e3:df:35:96 не равен ожидаемому 0/1, а ревен %s"%MAC_CE1_location)
        assert_that(MAC_CE2_location=='0/1',"Параметр LC/Location для e0:d9:e3:df:35:97 не равен ожидаемому 0/1, а ревен %s"%MAC_CE2_location)
