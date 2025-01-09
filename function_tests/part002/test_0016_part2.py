from conftest import *

@pytest.mark.part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.008:Проверка системных Proxy ARP')
@allure.title('В данном тесте будем проверять функционал ARP')
@pytest.mark.show_arp_int_part2
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param("DUT1"), 
 			 pytest.param("DUT2"), 
 			 pytest.param("DUT3")
			]
			)
									       
def test_arp_part2(DUT):
    allure.attach.file('./network-schemes/part1_ping_neighbors.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
    with open('config_OOP.json', 'r', encoding='utf-8') as file:
        check = json.load(file)
    router = setting_ME(DUT)
    if router.hostname == check['DUT1']['hostname']:
        allure.attach.file('./tests_descriptions/part002/test0016_procedure_script1.txt','Процедура теста', attachment_type=allure.attachment_type.TEXT)
    if router.hostname == check['DUT2']['hostname']:
        allure.attach.file('./tests_descriptions/part002/test0016_procedure_script2.txt','Процедура теста', attachment_type=allure.attachment_type.TEXT)  
    if router.hostname == check['DUT3']['hostname']:
        allure.attach.file('./tests_descriptions/part002/test0016_procedure_script3.txt','Процедура теста', attachment_type=allure.attachment_type.TEXT)
    
    resp = ''
    conn = Telnet()
    acc = Account(router.login, router.password)
    conn.connect(router.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    
    template2 = open('./templates/parse_show_arp.txt')
    cmd = 'show arp interfaces '+ router.neighor1['int_name']
    conn.execute(cmd)
    resp2 = conn.response
    fsm2 = textfsm.TextFSM(template2)
    result2 = fsm2.ParseTextToDicts(resp2)
    
    template1 = open('./templates/parse_show_arp.txt')
    cmd1 = 'show arp interfaces '+ router.neighor2['int_name']
    conn.execute(cmd1)
    resp1 = conn.response
    fsm1 = textfsm.TextFSM(template1)
    result1= fsm1.ParseTextToDicts(resp1)
    
    template3 = open('./templates/parse_show_arp.txt')
    cmd2 = 'show arp interfaces '+ router.neighor3['int_name']
    conn.execute(cmd2)
    resp3 = conn.response
    fsm3= textfsm.TextFSM(template3)
    result3 = fsm3.ParseTextToDicts(resp3)
    
    # Проверяем заполнилась ли arp таблица
    loc_index=0
    if router.hostname == check['DUT1']['hostname']:
        located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.2', loc_index)
        if located_index1==999:
            conn.execute('ping 192.168.55.2')
            conn.execute(cmd)
            resp2 = conn.response
            fsm2 = textfsm.TextFSM(template2)
            result2 = fsm2.ParseTextToDicts(resp2)
            located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.2', loc_index)
            assert_that(located_index1!=999, "В выводе команды %s не обнаружен адрес 192.168.55.2" % cmd)
        located_index = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.1', loc_index)
        assert_that(located_index!=999, "В выводе команды %s не обнаружен адрес 192.168.55.1" % cmd)
        allure.attach(resp2, 'Вывод команды '+ cmd, attachment_type=allure.attachment_type.TEXT)
               
        located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.22', loc_index)
        if located_index3==999:
            conn.execute('ping 192.168.55.22')
            conn.execute(cmd1)
            resp1 = conn.response
            fsm1 = textfsm.TextFSM(template1)
            result1= fsm1.ParseTextToDicts(resp1)
            located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.22', loc_index)
            assert_that(located_index3!=999, "В выводе команды %s не обнаружен адрес 192.168.55.22" % cmd1)	
        located_index2 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.21', loc_index)
        assert_that(located_index2!=999, "В выводе команды %s не обнаружен адрес 192.168.55.21" % cmd1) 
        allure.attach(resp1, 'Вывод команды '+ cmd1, attachment_type=allure.attachment_type.TEXT)
                
        located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.10', loc_index)
        if located_index5==999:
            conn.execute('ping 192.168.55.10')
            conn.execute(cmd2)
            resp3 = conn.response
            fsm3= textfsm.TextFSM(template3)
            result3 = fsm3.ParseTextToDicts(resp3)
            located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.10', loc_index)
            assert_that(located_index5!=999, "В выводе команды %s не обнаружен адрес 192.168.55.10" % cmd2)	 
        located_index4 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.9', loc_index)
        assert_that(located_index4!=999, "В выводе команды %s не обнаружен адрес 192.168.55.9" % cmd2)
        allure.attach(resp3, 'Вывод команды ' + cmd2, attachment_type=allure.attachment_type.TEXT)
        
    
    
    if router.hostname == check['DUT2']['hostname']:
        located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.5', loc_index)
        if located_index1==999:
            conn.execute('ping 192.168.55.5')
            conn.execute(cmd)
            resp2 = conn.response
            fsm2 = textfsm.TextFSM(template2)
            result2 = fsm2.ParseTextToDicts(resp2)            
            located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.5', loc_index)
            assert_that(located_index1!=999, "В выводе команды %s не обнаружен адрес 192.168.55.5" % cmd)	
        located_index = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.6', loc_index)
        assert_that(located_index!=999, "В выводе команды %s не обнаружен адрес 192.168.55.6" % cmd)
        allure.attach(resp2, 'Вывод команды '+ cmd, attachment_type=allure.attachment_type.TEXT)
             
        located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.21', loc_index)
        if located_index3==999:
            conn.execute('ping 192.168.55.21')
            conn.execute(cmd1)
            resp1 = conn.response
            fsm1 = textfsm.TextFSM(template1)
            result1= fsm1.ParseTextToDicts(resp1)            
            located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.21', loc_index)
            assert_that(located_index3!=999, "В выводе команды %s не обнаружен адрес 192.168.55.21" % cmd1)	
        located_index2 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.22', loc_index)
        assert_that(located_index2!=999, "В выводе команды %s не обнаружен адрес 192.168.55.22" % cmd1)   
        allure.attach(resp1, 'Вывод команды '+ cmd1, attachment_type=allure.attachment_type.TEXT)
              
        located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.14', loc_index)
        if located_index5==999:
            conn.execute('ping 192.168.55.14')
            conn.execute(cmd2)
            resp3 = conn.response
            fsm3= textfsm.TextFSM(template3)
            result3 = fsm3.ParseTextToDicts(resp3)
            located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.14', loc_index)
            assert_that(located_index5!=999, "В выводе команды %s не обнаружен адрес 192.168.55.14" % cmd2)	
        located_index4 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.13', loc_index)
        assert_that(located_index4!=999, "В выводе команды %s не обнаружен адрес 192.168.55.13" % cmd2)  
        allure.attach(resp3, 'Вывод команды ' + cmd2, attachment_type=allure.attachment_type.TEXT)
        
        
    if router.hostname == check['DUT3']['hostname']:
        located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.1', loc_index)
        if located_index1==999:
            conn.execute('ping 192.168.55.1')
            conn.execute(cmd)
            resp2 = conn.response
            fsm2 = textfsm.TextFSM(template2)
            result2 = fsm2.ParseTextToDicts(resp2) 
            located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.1', loc_index)
            assert_that(located_index1!=999, "В выводе команды %s не обнаружен адрес 192.168.55.1" % cmd)
        located_index = locate_index_in_ListOfDict(result2, 'IP', '192.168.55.2', loc_index)
        assert_that(located_index!=999, "В выводе команды %s не обнаружен адрес 192.168.55.2" % cmd)
        allure.attach(resp2, 'Вывод команды '+ cmd, attachment_type=allure.attachment_type.TEXT)
               
        located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.6', loc_index)
        if located_index3==999:
            conn.execute('ping 192.168.55.6')
            conn.execute(cmd1)
            resp1 = conn.response
            fsm1 = textfsm.TextFSM(template1)
            result1= fsm1.ParseTextToDicts(resp1)    
            located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.6', loc_index)
            assert_that(located_index3!=999, "В выводе команды %s не обнаружен адрес 192.168.55.6" % cmd1)	
        located_index2 = locate_index_in_ListOfDict(result1, 'IP', '192.168.55.5', loc_index)
        assert_that(located_index2!=999, "В выводе команды %s не обнаружен адрес 192.168.55.5" % cmd1) 
        allure.attach(resp1, 'Вывод команды '+ cmd1, attachment_type=allure.attachment_type.TEXT)
               
        located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.18', loc_index)
        if located_index5==999:
            conn.execute('ping 192.168.55.18')
            conn.execute(cmd2)
            resp3 = conn.response
            fsm3= textfsm.TextFSM(template3)
            result3 = fsm3.ParseTextToDicts(resp3)
            located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.18', loc_index)
            assert_that(located_index5!=999, "В выводе команды %s не обнаружен адрес 192.168.55.18" % cmd2)	
        located_index4 = locate_index_in_ListOfDict(result3, 'IP', '192.168.55.17', loc_index)
        assert_that(located_index4!=999, "В выводе команды %s не обнаружен адрес 192.168.55.17" % cmd2)      
        allure.attach(resp3, 'Вывод команды ' + cmd2, attachment_type=allure.attachment_type.TEXT)	
        
        
    if (router.neighor1['int_name'] == check['DUT1']['int']['to_phys1']['int_name'] and router.host_ip== check['DUT1']['host_ip']):
        IP = result2[located_index]['IP']
        assert_that(IP =='192.168.55.1','Параметр IP в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.1, а равен - %s"%IP)
        age = result2[located_index]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" пуст")
        mac = result2[located_index]['mac']
        assert_that(mac=='e4:5a:d4:de:c8:a2','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e4:5a:d4:de:c8:a2, а равен - %s"%mac)
        state = result2[located_index]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result2[located_index]['Int']
        assert_that(Int=='bu1','Параметр Interface в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu1, а равен - %s"%Int)
        IP = result2[located_index1]['IP']
        assert_that(IP =='192.168.55.2','Параметр IP в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.2, а равен - %s"%IP)
        age = result2[located_index1]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" пуст")
        mac = result2[located_index1]['mac']
        assert_that(mac=='a8:f9:4b:8b:94:02','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению a8:f9:4b:8b:94:02, а равен - %s"%mac)
        state = result2[located_index1]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result2[located_index1]['Int']
        assert_that(Int=='bu1','Параметр Interface в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu1, а равен - %s"%Int)
    
    elif (router.neighor2['int_name'] == check['DUT1']['int']['to_phys2']['int_name']  and router.host_ip== check['DUT1']['host_ip']):
        IP = result1[located_index2]['IP']
        assert_that(IP =='192.168.55.21','Параметр IP в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.21, а равен - %s"%IP)
        age = result1[located_index2]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" пуст")
        mac = result1[located_index2]['mac']
        assert_that(mac=='e4:5a:d4:de:c8:a3','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e4:5a:d4:de:c8:a3, а равен - %s"%mac)
        state = result1[located_index2]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result1[located_index2]['Int']
        assert_that(Int=='bu2','Параметр Interface в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu2, а равен - %s"%Int)
        IP = result1[located_index3]['IP']
        assert_that(IP =='192.168.55.22','Параметр IP в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.22, а равен - %s"%IP)
        age = result1[located_index3]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" пуст")
        mac = result1[located_index3]['mac']
        assert_that(mac=='e0:d9:e3:ff:48:b3','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 'e0:d9:e3:ff:48:b3', а равен - %s"%mac)
        state = result1[located_index3]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result1[located_index3]['Int']
        assert_that(Int=='bu2','Параметр Interface в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu2, а равен - %s"%Int)
    
    elif (router.neighor3['int_name'] == check['DUT1']['int']['to_virt']['int_name']  and router.host_ip== check['DUT1']['host_ip']):
        IP = result3[located_index4]['IP']
        assert_that(IP =='192.168.55.9','Параметр IP в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.9, а равен - %s"%IP)
        age = result3[located_index4]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" пуст")
        mac = result3[located_index4]['mac']
        assert_that(mac=='e4:5a:d4:de:c8:8b','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e4:5a:d4:de:c8:8b, а равен - %s"%mac)
        state = result3[located_index4]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result3[located_index4]['Int']
        assert_that(Int=='te0/0/11.352','Параметр Interface в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению te0/0/11.352, а равен - %s"%Int)
        IP = result3[located_index5]['IP']
        assert_that(IP =='192.168.55.10','Параметр IP в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.10, а равен - %s"%IP)
        age = result3[located_index5]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" пуст")
        mac = result3[located_index5]['mac']
        assert_that(mac=='50:00:00:02:00:02','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 50:00:00:02:00:02, а равен - %s"%mac)
        state = result3[located_index5]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result3[located_index5]['Int']
        assert_that(Int=='te0/0/11.352','Параметр Interface в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению te0/0/11.352, а равен - %s"%Int)
   
   
    elif (router.neighor1['int_name'] == check['DUT2']['int']['to_phys1']['int_name']  and router.host_ip== check['DUT2']['host_ip']):
        IP = result2[located_index1]['IP']
        assert_that(IP =='192.168.55.5','Параметр IP в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.5, а равен - %s"%IP)
        age = result2[located_index1]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" пуст")
        mac = result2[located_index1]['mac']
        assert_that(mac=='a8:f9:4b:8b:94:03','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению a8:f9:4b:8b:94:03, а равен - %s"%mac)
        state = result2[located_index1]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result2[located_index1]['Int']
        assert_that(Int=='bu1','Параметр Interface в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu1, а равен - %s"%Int)
        IP = result2[located_index]['IP']
        assert_that(IP =='192.168.55.6','Параметр IP в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.6, а равен - %s"%IP)
        age = result2[located_index]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" пуст")
        mac = result2[located_index]['mac']
        assert_that(mac=='e0:d9:e3:ff:48:b2','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e0:d9:e3:ff:48:b2, а равен - %s"%mac)
        state = result2[located_index]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result2[located_index]['Int']
        assert_that(Int=='bu1','Параметр Interface в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu1, а равен - %s"%Int)
    
    elif (router.neighor2['int_name'] == check['DUT2']['int']['to_phys2']['int_name']  and router.host_ip== check['DUT2']['host_ip']):
        IP = result1[located_index3]['IP']
        assert_that(IP =='192.168.55.21','Параметр IP в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.21, а равен - %s"%IP)
        age = result1[located_index3]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" пуст")
        mac = result1[located_index3]['mac']
        assert_that(mac=='e0:d9:e3:ff:48:b2','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e0:d9:e3:ff:48:b2, а равен - %s"%mac)
        state = result1[located_index3]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result1[located_index3]['Int']
        assert_that(Int=='bu2','Параметр Interface в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu2, а равен - %s"%Int)
        IP = result1[located_index2]['IP']
        assert_that(IP =='192.168.55.22','Параметр IP в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.22, а равен - %s"%IP)
        age = result1[located_index2]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" пуст")
        mac = result1[located_index2]['mac']
        assert_that(mac=='e0:d9:e3:ff:48:b3','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e0:d9:e3:ff:48:b3, а равен - %s"%mac)
        state = result1[located_index2]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result1[located_index2]['Int']
        assert_that(Int=='bu2','Параметр Interface в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu2, а равен - %s"%Int)
    
    elif (router.neighor3['int_name'] == check['DUT2']['int']['to_virt']['int_name']  and router.host_ip== check['DUT2']['host_ip']):
        IP = result3[located_index4]['IP']
        assert_that(IP =='192.168.55.13','Параметр IP в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.13, а равен - %s"%IP)
        age = result3[located_index4]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" пуст")
        mac = result3[located_index4]['mac']
        assert_that(mac=='e0:d9:e3:ff:48:8b','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e0:d9:e3:ff:48:8b, а равен - %s"%mac)
        state = result3[located_index4]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result3[located_index4]['Int']
        assert_that(Int=='te0/0/11.351','Параметр Interface в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению te0/0/11.351, а равен - %s"%Int)
        IP = result3[located_index5]['IP']
        assert_that(IP =='192.168.55.14','Параметр IP в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.14, а равен - %s"%IP)
        age = result3[located_index5]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" пуст")
        mac = result3[located_index5]['mac']
        assert_that(mac=='50:00:00:02:00:02','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 50:00:00:02:00:02, а равен - %s"%mac)
        state = result3[located_index5]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result3[located_index5]['Int']
        assert_that(Int=='te0/0/11.351','Параметр Interface в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению te0/0/11.351, а равен - %s"%Int)    
    
    
    elif (router.neighor1['int_name'] == check['DUT3']['int']['to_phys1']['int_name'] and router.host_ip== check['DUT3']['host_ip']):
        IP = result2[located_index1]['IP']
        assert_that(IP =='192.168.55.1','Параметр IP в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.1, а равен - %s"%IP)
        age = result2[located_index1]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" пуст")
        mac = result2[located_index1]['mac']
        assert_that(mac=='e4:5a:d4:de:c8:a2','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e4:5a:d4:de:c8:a2, а равен - %s"%mac)
        state = result2[located_index1]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result2[located_index1]['Int']
        assert_that(Int=='bu1','Параметр Interface в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu1, а равен - %s"%Int)
        IP = result2[located_index]['IP']
        assert_that(IP =='192.168.55.2','Параметр IP в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.2, а равен - %s"%IP)
        age = result2[located_index]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" пуст")
        mac = result2[located_index]['mac']
        assert_that(mac=='a8:f9:4b:8b:94:02','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению a8:f9:4b:8b:94:02, а равен - %s"%mac)
        state = result2[located_index]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result2[located_index]['Int']
        assert_that(Int=='bu1','Параметр Interface в выводе команды для интерфейса '+  router.neighor1['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu1, а равен - %s"%Int)
    
    elif (router.neighor2['int_name'] == check['DUT3']['int']['to_phys2']['int_name'] and router.host_ip== check['DUT3']['host_ip']):
        IP = result1[located_index2]['IP']
        assert_that(IP =='192.168.55.5','Параметр IP в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.5, а равен - %s"%IP)
        age = result1[located_index2]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" пуст")
        mac = result1[located_index2]['mac']
        assert_that(mac=='a8:f9:4b:8b:94:03','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению a8:f9:4b:8b:94:03, а равен - %s"%mac)
        state = result1[located_index2]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result1[located_index2]['Int']
        assert_that(Int=='bu2','Параметр Interface в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu2, а равен - %s"%Int)
        IP = result1[located_index3]['IP']
        assert_that(IP =='192.168.55.6','Параметр IP в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.6, а равен - %s"%IP)
        age = result1[located_index3]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" пуст")
        mac = result1[located_index3]['mac']
        assert_that(mac=='e0:d9:e3:ff:48:b2','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению e0:d9:e3:ff:48:b2, а равен - %s"%mac)
        state = result1[located_index3]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result1[located_index3]['Int']
        assert_that(Int=='bu2','Параметр Interface в выводе команды для интерфейса '+  router.neighor2['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению bu2, а равен - %s"%Int)
    
    elif (router.neighor1['int_name'] == check['DUT3']['int']['to_virt']['int_name'] and router.host_ip== check['DUT3']['host_ip']):
        IP = result3[located_index4]['IP']
        assert_that(IP =='192.168.55.17','Параметр IP в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.17, а равен - %s"%IP)
        age = result3[located_index4]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" пуст")
        mac = result3[located_index4]['mac']
        assert_that(mac=='a8:f9:4b:8b:92:99','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению a8:f9:4b:8b:92:99, а равен - %s"%mac)
        state = result3[located_index4]['state']
        assert_that(state=='Interface','Параметр State в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Interface, а равен - %s"%state)
        Int = result3[located_index4]['Int']
        assert_that(Int=='te0/1/5.350','Параметр Interface в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению te0/1/5.350, а равен - %s"%Int)
        IP = result3[located_index5]['IP']
        assert_that(IP =='192.168.55.18','Параметр IP в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 192.168.55.18, а равен - %s"%IP)
        age = result3[located_index5]['age']
        assert_that(age !=' ','Параметр Age в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" пуст")
        mac = result3[located_index5]['mac']
        assert_that(mac=='50:00:00:02:00:02','Параметр Hardware address в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению 50:00:00:02:00:02, а равен - %s"%mac)
        state = result3[located_index5]['state']
        assert_that(state=='Dynamic','Параметр State в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению Dynamic, а равен - %s"%state)
        Int = result3[located_index5]['Int']
        assert_that(Int=='te0/1/5.350','Параметр Interface в выводе команды для интерфейса '+  router.neighor3['int_name'] + ' ' +router.hostname +" не соответсвует ожидаемому значению te0/1/5.350, а равен - %s"%Int)  
