from conftest import *

@pytest.mark.part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.008:Проверка системных Proxy ARP')
@allure.title('В данном тесте будем проверять функционал ARP')
@pytest.mark.show_arp_int_part2
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
									       
def test_arp_part2(DUT):
    allure.attach.file('./network-schemes/part1_ping_neighbors.png','Схема теста:', attachment_type=allure.attachment_type.PNG)
    if DUT.hostname == DUT1.hostname:
        allure.attach.file('./tests_descriptions/part002/test0016_procedure_script1.txt','Процедура теста', attachment_type=allure.attachment_type.TEXT)
    if DUT.hostname == DUT2.hostname:
        allure.attach.file('./tests_descriptions/part002/test0016_procedure_script2.txt','Процедура теста', attachment_type=allure.attachment_type.TEXT)  
    if DUT.hostname == DUT3.hostname:
        allure.attach.file('./tests_descriptions/part002/test0016_procedure_script3.txt','Процедура теста', attachment_type=allure.attachment_type.TEXT)
    
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    
    template2 = open('./templates/parse_show_arp.txt')
    cmd = 'show arp interfaces '+ DUT.neighor1['int_name']
    conn.execute(cmd)
    resp2 = conn.response
    fsm2 = textfsm.TextFSM(template2)
    result2 = fsm2.ParseTextToDicts(resp2)
    
    template1 = open('./templates/parse_show_arp.txt')
    cmd1 = 'show arp interfaces '+ DUT.neighor2['int_name']
    conn.execute(cmd1)
    resp1 = conn.response
    fsm1 = textfsm.TextFSM(template1)
    result1= fsm1.ParseTextToDicts(resp1)
    
    template3 = open('./templates/parse_show_arp.txt')
    cmd2 = 'show arp interfaces '+ DUT.neighor3['int_name']
    conn.execute(cmd2)
    resp3 = conn.response
    fsm3= textfsm.TextFSM(template3)
    result3 = fsm3.ParseTextToDicts(resp3)
    
    # Проверяем заполнилась ли arp таблица
    # Проверяем заполнилась ли arp таблица
    loc_index = 0
    if DUT.hostname == DUT1.hostname:
        located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.2', loc_index)
        if located_index1 == 999:
            conn.execute('ping 192.168.1.2')
            conn.execute(cmd)
            resp2 = conn.response
            fsm2 = textfsm.TextFSM(template2)
            result2 = fsm2.ParseTextToDicts(resp2)
            located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.2', loc_index)
            assert_that(located_index1 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.2" % cmd)
        located_index = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.1', loc_index)
        assert_that(located_index != 999, "В выводе команды %s не обнаружен адрес 192.168.1.1" % cmd)
        allure.attach(resp2, 'Вывод команды ' + cmd, attachment_type=allure.attachment_type.TEXT)

        located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.22', loc_index)
        if located_index3 == 999:
            conn.execute('ping 192.168.1.22')
            conn.execute(cmd1)
            resp1 = conn.response
            fsm1 = textfsm.TextFSM(template1)
            result1 = fsm1.ParseTextToDicts(resp1)
            located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.22', loc_index)
            assert_that(located_index3 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.22" % cmd1)
        located_index2 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.21', loc_index)
        assert_that(located_index2 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.21" % cmd1)
        allure.attach(resp1, 'Вывод команды ' + cmd1, attachment_type=allure.attachment_type.TEXT)

        located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.10', loc_index)
        if located_index5 == 999:
            conn.execute('ping 192.168.1.10')
            conn.execute(cmd2)
            resp3 = conn.response
            fsm3 = textfsm.TextFSM(template3)
            result3 = fsm3.ParseTextToDicts(resp3)
            located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.10', loc_index)
            assert_that(located_index5 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.10" % cmd2)
        located_index4 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.9', loc_index)
        assert_that(located_index4 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.9" % cmd2)
        allure.attach(resp3, 'Вывод команды ' + cmd2, attachment_type=allure.attachment_type.TEXT)

    if DUT.hostname == DUT2.hostname:
        located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.5', loc_index)
        if located_index1 == 999:
            conn.execute('ping 192.168.1.5')
            conn.execute(cmd)
            resp2 = conn.response
            fsm2 = textfsm.TextFSM(template2)
            result2 = fsm2.ParseTextToDicts(resp2)
            located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.5', loc_index)
            assert_that(located_index1 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.5" % cmd)
        located_index = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.6', loc_index)
        assert_that(located_index != 999, "В выводе команды %s не обнаружен адрес 192.168.1.6" % cmd)
        allure.attach(resp2, 'Вывод команды ' + cmd, attachment_type=allure.attachment_type.TEXT)

        located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.21', loc_index)
        if located_index3 == 999:
            conn.execute('ping 192.168.1.21')
            conn.execute(cmd1)
            resp1 = conn.response
            fsm1 = textfsm.TextFSM(template1)
            result1 = fsm1.ParseTextToDicts(resp1)
            located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.21', loc_index)
            assert_that(located_index3 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.21" % cmd1)
        located_index2 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.22', loc_index)
        assert_that(located_index2 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.22" % cmd1)
        allure.attach(resp1, 'Вывод команды ' + cmd1, attachment_type=allure.attachment_type.TEXT)

        located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.14', loc_index)
        if located_index5 == 999:
            conn.execute('ping 192.168.1.14')
            conn.execute(cmd2)
            resp3 = conn.response
            fsm3 = textfsm.TextFSM(template3)
            result3 = fsm3.ParseTextToDicts(resp3)
            located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.14', loc_index)
            assert_that(located_index5 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.14" % cmd2)
        located_index4 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.13', loc_index)
        assert_that(located_index4 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.13" % cmd2)
        allure.attach(resp3, 'Вывод команды ' + cmd2, attachment_type=allure.attachment_type.TEXT)

    if DUT.hostname == DUT3.hostname:
        located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.1', loc_index)
        if located_index1 == 999:
            conn.execute('ping 192.168.1.1')
            conn.execute(cmd)
            resp2 = conn.response
            fsm2 = textfsm.TextFSM(template2)
            result2 = fsm2.ParseTextToDicts(resp2)
            located_index1 = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.1', loc_index)
            assert_that(located_index1 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.1" % cmd)
        located_index = locate_index_in_ListOfDict(result2, 'IP', '192.168.1.2', loc_index)
        assert_that(located_index != 999, "В выводе команды %s не обнаружен адрес 192.168.1.2" % cmd)
        allure.attach(resp2, 'Вывод команды ' + cmd, attachment_type=allure.attachment_type.TEXT)

        located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.6', loc_index)
        if located_index3 == 999:
            conn.execute('ping 192.168.1.6')
            conn.execute(cmd1)
            resp1 = conn.response
            fsm1 = textfsm.TextFSM(template1)
            result1 = fsm1.ParseTextToDicts(resp1)
            located_index3 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.6', loc_index)
            assert_that(located_index3 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.6" % cmd1)
        located_index2 = locate_index_in_ListOfDict(result1, 'IP', '192.168.1.5', loc_index)
        assert_that(located_index2 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.5" % cmd1)
        allure.attach(resp1, 'Вывод команды ' + cmd1, attachment_type=allure.attachment_type.TEXT)

        located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.18', loc_index)
        if located_index5 == 999:
            conn.execute('ping 192.168.1.18')
            conn.execute(cmd2)
            resp3 = conn.response
            fsm3 = textfsm.TextFSM(template3)
            result3 = fsm3.ParseTextToDicts(resp3)
            located_index5 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.18', loc_index)
            assert_that(located_index5 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.18" % cmd2)
        located_index4 = locate_index_in_ListOfDict(result3, 'IP', '192.168.1.17', loc_index)
        assert_that(located_index4 != 999, "В выводе команды %s не обнаружен адрес 192.168.1.17" % cmd2)
        allure.attach(resp3, 'Вывод команды ' + cmd2, attachment_type=allure.attachment_type.TEXT)

    if (DUT.neighor1["int_name"] == DUT1.neighor1['int_name'] and DUT.host_ip ==  DUT1.host_ip):
        IP = result2[located_index]['IP']
        assert_that(f"{IP}/30" == DUT1.neighor1['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.1, а равен - %s" % IP)
        age = result2[located_index]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result2[located_index]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:96, а равен - %s" % mac)
        state = result2[located_index]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result2[located_index]['Int']
        assert_that(Int == DUT1.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu1, а равен - %s" % Int)
        IP = result2[located_index1]['IP']
        assert_that(f"{IP}/30" == DUT3.neighor1['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.2, а равен - %s" % IP)
        age = result2[located_index1]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result2[located_index1]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 68:13:e2:d8:16:ba, а равен - %s" % mac)
        state = result2[located_index1]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result2[located_index1]['Int']
        assert_that(Int == DUT3.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu1, а равен - %s" % Int)

    elif (DUT.neighor2["int_name"] == DUT1.neighor2['int_name'] and DUT.host_ip ==  DUT1.host_ip):
        IP = result1[located_index2]['IP']
        assert_that(f"{IP}/30" == DUT1.neighor2['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.21, а равен - %s" % IP)
        age = result1[located_index2]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result1[located_index2]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:97, а равен - %s" % mac)
        state = result1[located_index2]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result1[located_index2]['Int']
        assert_that(Int == DUT1.neighor2['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu2, а равен - %s" % Int)
        IP = result1[located_index3]['IP']
        assert_that(f"{IP}/30" == DUT2.neighor2['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.22, а равен - %s" % IP)
        age = result1[located_index3]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result1[located_index3]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 'e0:d9:e3:df:6e:b3', а равен - %s" % mac)
        state = result1[located_index3]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result1[located_index3]['Int']
        assert_that(Int == DUT2.neighor2['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu2, а равен - %s" % Int)

    elif (DUT.neighor3["int_name"] == DUT1.neighor3['int_name'] and DUT.host_ip ==  DUT1.host_ip):
        IP = result3[located_index4]['IP']
        assert_that(f"{IP}/30" == DUT1.neighor3['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.9, а равен - %s" % IP)
        age = result3[located_index4]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result3[located_index4]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:8b, а равен - %s" % mac)
        state = result3[located_index4]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result3[located_index4]['Int']
        assert_that(Int == DUT1.neighor3['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению te0/0/11.352, а равен - %s" % Int)
        IP = result3[located_index5]['IP']
        assert_that(f"{IP}/30" == DUT4['vlan2']['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.10, а равен - %s" % IP)
        age = result3[located_index5]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result3[located_index5]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 50:00:00:13:00:02, а равен - %s" % mac)
        state = result3[located_index5]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result3[located_index5]['Int']
        assert_that(Int == f"{DUT4['int']}.{DUT4['vlan2']['id']}",
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению te0/0/11.352, а равен - %s" % Int)


    elif (DUT.neighor1["int_name"] == DUT2.neighor1['int_name'] and DUT.host_ip ==  DUT2.host_ip):
        IP = result2[located_index1]['IP']
        assert_that(f"{IP}/30" == DUT3.neighor2['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.5, а равен - %s" % IP)
        age = result2[located_index1]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result2[located_index1]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 68:13:e2:d8:16:bb, а равен - %s" % mac)
        state = result2[located_index1]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result2[located_index1]['Int']
        assert_that(Int == DUT2.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu1, а равен - %s" % Int)

    elif (DUT.neighor2["int_name"] == DUT2.neighor2['int_name'] and DUT.host_ip ==  DUT2.host_ip):
        IP = result1[located_index3]['IP']
        assert_that(f"{IP}/30" == DUT2.neighor2['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.21, а равен - %s" % IP)
        age = result1[located_index3]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result1[located_index3]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:97, а равен - %s" % mac)
        state = result1[located_index3]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result1[located_index3]['Int']
        assert_that(Int == DUT2.neighor2['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu2, а равен - %s" % Int)
        IP = result1[located_index2]['IP']
        assert_that(f"{IP}/30" == DUT1.neighor2['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.22, а равен - %s" % IP)
        age = result1[located_index2]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result1[located_index2]['mac']
        assert_that(mac == '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:6e:b3, а равен - %s" % mac)
        state = result1[located_index2]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result1[located_index2]['Int']
        assert_that(Int == DUT1.neighor2['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu2, а равен - %s" % Int)

    elif (DUT.neighor3["int_name"] == DUT2.neighor3['int_name'] and DUT.host_ip ==  DUT2.host_ip):
        IP = result3[located_index4]['IP']
        assert_that(f"{IP}/30" == DUT2.neighor3['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.13, а равен - %s" % IP)
        age = result3[located_index4]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result3[located_index4]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:6e:8b, а равен - %s" % mac)
        state = result3[located_index4]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result3[located_index4]['Int']
        assert_that(Int == DUT2.neighor3['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению te0/0/11.351, а равен - %s" % Int)
        IP = result3[located_index5]['IP']
        assert_that(DUT.host_ip == DUT4['vlan3']['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.14, а равен - %s" % IP)
        age = result3[located_index5]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result3[located_index5]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 50:00:00:13:00:02, а равен - %s" % mac)
        state = result3[located_index5]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result3[located_index5]['Int']
        assert_that(Int == f"{DUT4['int']}.{DUT4['vlan2']['id']}",
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению te0/0/11.351, а равен - %s" % Int)


    elif (DUT.neighor1["int_name"] == DUT3.neighor1['int_name'] and DUT.host_ip ==  DUT3.host_ip):
        IP = result2[located_index1]['IP']
        assert_that(f"{IP}/30" == DUT1.neighor1['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.1, а равен - %s" % IP)
        age = result2[located_index1]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result2[located_index1]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:96, а равен - %s" % mac)
        state = result2[located_index1]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result2[located_index1]['Int']
        assert_that(Int == DUT3.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu1, а равен - %s" % Int)
        IP = result2[located_index]['IP']
        assert_that(f"{IP}/30" == DUT3.neighor1['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.2, а равен - %s" % IP)
        age = result2[located_index]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result2[located_index]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 68:13:e2:d8:16:ba, а равен - %s" % mac)
        state = result2[located_index]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result2[located_index]['Int']
        assert_that(Int == DUT1.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor1["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu1, а равен - %s" % Int)

    elif (DUT.neighor2["int_name"] == DUT3.neighor2['int_name'] and DUT.host_ip ==  DUT3.host_ip):
        IP = result1[located_index2]['IP']
        assert_that(f"{IP}/30" == DUT3.neighor2['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.21, а равен - %s" % IP)
        age = result1[located_index2]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result1[located_index2]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:97, а равен - %s" % mac)
        state = result1[located_index2]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result1[located_index2]['Int']
        assert_that(Int == DUT3.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu2, а равен - %s" % Int)
        IP = result1[located_index3]['IP']
        assert_that(f"{IP}/30" == DUT2.neighor1['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.22, а равен - %s" % IP)
        age = result1[located_index3]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result1[located_index3]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 'e0:d9:e3:df:6e:b3', а равен - %s" % mac)
        state = result1[located_index3]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result1[located_index3]['Int']
        assert_that(Int == DUT2.neighor1['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor2["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению bu2, а равен - %s" % Int)

    elif (DUT.neighor3["int_name"] == DUT3.neighor3['int_name'] and DUT.host_ip ==  DUT3.host_ip):
        IP = result3[located_index4]['IP']
        assert_that(f"{IP}/30" == DUT3.neighor3['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.9, а равен - %s" % IP)
        age = result3[located_index4]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result3[located_index4]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению e0:d9:e3:df:35:8b, а равен - %s" % mac)
        state = result3[located_index4]['state']
        assert_that(state == 'Interface',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Interface, а равен - %s" % state)
        Int = result3[located_index4]['Int']
        assert_that(Int == DUT3.neighor3['int_name'],
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению te0/0/11.352, а равен - %s" % Int)
        IP = result3[located_index5]['IP']
        assert_that(DUT.host_ip == DUT4['vlan1']['ip'],
                    'Параметр IP в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 192.168.1.10, а равен - %s" % IP)
        age = result3[located_index5]['age']
        assert_that(age != ' ', 'Параметр Age в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " пуст")
        mac = result3[located_index5]['mac']
        assert_that(mac != '',
                    'Параметр Hardware address в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению 50:00:00:13:00:02, а равен - %s" % mac)
        state = result3[located_index5]['state']
        assert_that(state == 'Dynamic',
                    'Параметр State в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению Dynamic, а равен - %s" % state)
        Int = result3[located_index5]['Int']
        assert_that(Int == f"{DUT4['int']}.{DUT4['vlan1']['id']}",
                    'Параметр Interface в выводе команды для интерфейса ' + DUT.neighor3["int_name"] + ' ' + DUT.hostname + " не соответствует ожидаемому значению te0/0/11.352, а равен - %s" % Int)
