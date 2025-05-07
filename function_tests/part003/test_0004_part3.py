from conftest import *

@allure.feature('03:Функциональное тестирование протокола LLDP')
@allure.story('3.2:Проверка LLDP')
@allure.title('В данном тесте будем  проверять вывод комнады show lldp neighbors')
@pytest.mark.part3
@pytest.mark.show_lldp_neighbors
@pytest.mark.dependency(depends=["load_config003_dut1","load_config003_dut2","load_config003_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
						   
def test_show_lldp_neighbors_part3 (DUT): 
    allure.attach.file('./network-schemes/part3_show_lldp_neighbor.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
# В данном тесте будем проверять вывод команды 'show lldp neighbors'      
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login , DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute("terminal datadump")
    conn.set_prompt('#')
    cmd = ('show lldp neighbors')     
    conn.execute(cmd) 
    resp = conn.response
    allure.attach(resp, 'Вывод команды show lldp neighbors', attachment_type=allure.attachment_type.TEXT)        
#    print('show users  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show lldp neighbors'
# C помощью магии модуля textFSM сравниваем вывод команды 'show users' c шаблоном в файле parse_show_lldp_neighbor.txt 
    template = open('./templates/parse_show_lldp_neighbor.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseTextToDicts(resp)
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    assert_that(len(result) > 0, f'Пустой вывод команды {cmd}')
    Top = result[0]['Top']
    assert_that(Top != '', "Заголовок в выводе команды %s не соответствует шаблону" % cmd)
    
    loc_index = 0
    if DUT.hostname == DUT1.hostname:
        located_index = locate_index_in_ListOfDict(result, 'local_port', DUT1.neighor2["interface"][0], loc_index)
        assert_that(located_index!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/1")
        located_index1 = locate_index_in_ListOfDict(result, 'local_port', DUT1.neighor2["interface"][1], loc_index)
        assert_that(located_index1!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/2")  
        located_index2 = locate_index_in_ListOfDict(result, 'local_port', DUT1.neighor1["interface"][0], loc_index)
        assert_that(located_index2!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/3")  
        located_index3 = locate_index_in_ListOfDict(result, 'local_port', DUT1.neighor1["interface"][1], loc_index)
        assert_that(located_index3!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/4")  
        
    if DUT.hostname == DUT2.hostname:
        located_index = locate_index_in_ListOfDict(result, 'local_port', DUT2.neighor1["interface"][0], loc_index)
        assert_that(located_index!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/3")
        located_index1 = locate_index_in_ListOfDict(result, 'local_port', DUT2.neighor1["interface"][1], loc_index)
        assert_that(located_index1!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/4")  
        located_index2 = locate_index_in_ListOfDict(result, 'local_port', DUT2.neighor2["interface"][0], loc_index)
        assert_that(located_index2!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/7")  
        located_index3 = locate_index_in_ListOfDict(result, 'local_port', DUT2.neighor2["interface"][1], loc_index)
        assert_that(located_index3!=999, f"В выводе команды {cmd} не обнаружен Local port te0/0/8")  
        
    if DUT.hostname == DUT3.hostname:
        located_index = locate_index_in_ListOfDict(result, 'local_port', DUT3.neighor1["interface"][0], loc_index)
        assert_that(located_index!=999, f"В выводе команды {cmd} не обнаружен Local port te0/1/13")
        located_index1 = locate_index_in_ListOfDict(result, 'local_port', DUT3.neighor1["interface"][1], loc_index)
        assert_that(located_index1!=999, f"В выводе команды {cmd} не обнаружен Local port te0/1/14")  
        located_index2 = locate_index_in_ListOfDict(result, 'local_port', DUT3.neighor2["interface"][0], loc_index)
        assert_that(located_index2!=999, f"В выводе команды {cmd} не обнаружен Local port te0/8/3")  
        located_index3 = locate_index_in_ListOfDict(result, 'local_port', DUT3.neighor2["interface"][1], loc_index)
        assert_that(located_index3!=999, f"В выводе команды {cmd} не обнаружен Local port te0/8/4")  
        
        
    local_port = result[located_index]['local_port']
    device_id = result[located_index]['device_id']
    port_id = result[located_index]['port_id']
    capabilities = result[located_index]['capabilities']
    agent = result[located_index]['agent']
    system_name = result[located_index]['system_name']
    
    local_port1 = result[located_index1]['local_port']
    device_id1 = result[located_index1]['device_id']
    port_id1 = result[located_index1]['port_id']
    capabilities1 = result[located_index1]['capabilities']
    agent1 = result[located_index1]['agent']
    system_name1 = result[located_index1]['system_name']
    
    local_port2 = result[located_index2]['local_port']
    device_id2 = result[located_index2]['device_id']
    port_id2 = result[located_index2]['port_id']
    capabilities2 = result[located_index2]['capabilities']
    agent2 = result[located_index2]['agent']
    system_name2 = result[located_index2]['system_name']
    
    local_port3 = result[located_index3]['local_port']
    device_id3 = result[located_index3]['device_id']
    port_id3 = result[located_index3]['port_id']
    capabilities3 = result[located_index3]['capabilities']
    agent3 = result[located_index3]['agent']
    system_name3 = result[located_index3]['system_name']
    
    if DUT.hostname == DUT1.hostname:
        assert_that(device_id != '', "Значение Device id для Local port %s равно не ожидаемому e0:d9:e3:ff:48:80, а %s" % (local_port, device_id))
        assert_that(port_id == DUT2.neighor2["interface"][0], "Значение Port id для Local port %s равно не ожидаемому te0/0/7, а %s" % (local_port, port_id))
        assert_that(capabilities == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port, capabilities))
        assert_that(agent == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port, agent))
        assert_that(system_name == DUT2.hostname, "Значение System name для Local port %s равно не ожидаемому atAR2, а %s" % (local_port, system_name))
        
        assert_that(device_id1 != '', "Значение Device id для Local port %s равно не ожидаемому e0:d9:e3:ff:48:80, а %s" % (local_port1, device_id1))
        assert_that(port_id1 == DUT2.neighor2["interface"][1], "Значение Port id для Local port %s равно не ожидаемому te0/0/8, а %s" % (local_port1, port_id1))
        assert_that(capabilities1 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port1, capabilities1))
        assert_that(agent1 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port1, agent1))
        assert_that(system_name1 == DUT2.hostname, "Значение System name для Local port %s равно не ожидаемому atAR2, а %s" % (local_port1, system_name1))
        
        assert_that(device_id2 != '', "Значение Device id для Local port %s равно не ожидаемому a8:f9:4b:8b:92:80, а %s" % (local_port2, device_id2))
        assert_that(port_id2 == DUT3.neighor1["interface"][0], "Значение Port id для Local port %s равно не ожидаемому te0/1/13, а %s" % (local_port2, port_id2))
        assert_that(capabilities2 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port2, capabilities2))
        assert_that(agent2 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port2, agent2))
        assert_that(system_name2 == DUT3.hostname, "Значение System name для Local port %s равно не ожидаемому atDR1, а %s" % (local_port2, system_name2))   
        
        assert_that(device_id3 != '', "Значение Device id для Local port %s равно не ожидаемому a8:f9:4b:8b:92:80, а %s" % (local_port3, device_id3))
        assert_that(port_id3 == DUT3.neighor1["interface"][1], "Значение Port id для Local port %s равно не ожидаемому te0/1/14, а %s" % (local_port3, port_id3))
        assert_that(capabilities3 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port3, capabilities3))
        assert_that(agent3 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port3, agent3))
        assert_that(system_name3 == DUT3.hostname, "Значение System name для Local port %s равно не ожидаемому atDR1, а %s" % (local_port3, system_name3))   
        

    if DUT.hostname == DUT2.hostname:
        assert_that(device_id != '', "Значение Device id для Local port %s равно не ожидаемому a8:f9:4b:8b:92:80, а %s" % (local_port, device_id))
        assert_that(port_id == DUT3.neighor2["interface"][0], "Значение Port id для Local port %s равно не ожидаемому te0/8/3, а %s" % (local_port, port_id))
        assert_that(capabilities == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port, capabilities))
        assert_that(agent == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port, agent))
        assert_that(system_name == DUT3.hostname, "Значение System name для Local port %s равно не ожидаемому atDR1, а %s" % (local_port, system_name))
        
        assert_that(device_id1 != '', "Значение Device id для Local port %s равно не ожидаемому a8:f9:4b:8b:92:80, а %s" % (local_port1, device_id1))
        assert_that(port_id1 == DUT3.neighor2["interface"][1], "Значение Port id для Local port %s равно не ожидаемому te0/8/4, а %s" % (local_port1, port_id1))
        assert_that(capabilities1 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port1, capabilities1))
        assert_that(agent1 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port1, agent1))
        assert_that(system_name1 == DUT3.hostname, "Значение System name для Local port %s равно не ожидаемому atDR1, а %s" % (local_port1, system_name1))       
        
        assert_that(device_id2 != '', "Значение Device id для Local port %s равно не ожидаемому e4:5a:d4:de:c8:80, а %s" % (local_port2, device_id2))
        assert_that(port_id2 == DUT1.neighor2["interface"][0], "Значение Port id для Local port %s равно не ожидаемому te0/0/1, а %s" % (local_port2, port_id2))
        assert_that(capabilities2 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port2, capabilities2))
        assert_that(agent2 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port2, agent2))
        assert_that(system_name2 == DUT1.hostname, "Значение System name для Local port %s равно не ожидаемому atAR1, а %s" % (local_port2, system_name2))   
        
        assert_that(device_id3 != '', "Значение Device id для Local port %s равно не ожидаемому e4:5a:d4:de:c8:80, а %s" % (local_port3, device_id3))
        assert_that(port_id3 == DUT1.neighor2["interface"][1], "Значение Port id для Local port %s равно не ожидаемому te0/0/2, а %s" % (local_port3, port_id3))
        assert_that(capabilities3 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port3, capabilities3))
        assert_that(agent3 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port3, agent3))
        assert_that(system_name3 == DUT1.hostname, "Значение System name для Local port %s равно не ожидаемому atAR1, а %s" % (local_port3, system_name3))   
        
    if DUT.hostname == DUT3.hostname:
        assert_that(device_id != '', "Значение Device id для Local port %s равно не ожидаемому e4:5a:d4:de:c8:80, а %s" % (local_port, device_id))
        assert_that(port_id == DUT1.neighor1["interface"][0], "Значение Port id для Local port %s равно не ожидаемому te0/0/3, а %s" % (local_port, port_id))
        assert_that(capabilities == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port, capabilities))
        assert_that(agent == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port, agent))
        assert_that(system_name == DUT1.hostname, "Значение System name для Local port %s равно не ожидаемому atAR1, а %s" % (local_port, system_name))
        
        assert_that(device_id1 != '', "Значение Device id для Local port %s равно не ожидаемому e4:5a:d4:de:c8:80, а %s" % (local_port1, device_id1))
        assert_that(port_id1 == DUT1.neighor1["interface"][1], "Значение Port id для Local port %s равно не ожидаемому te0/0/4, а %s" % (local_port1, port_id1))
        assert_that(capabilities1 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port1, capabilities1))
        assert_that(agent1 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port1, agent1))
        assert_that(system_name1 == DUT1.hostname, "Значение System name для Local port %s равно не ожидаемому atAR1, а %s" % (local_port1, system_name1))       
        
        assert_that(device_id2 != '', "Значение Device id для Local port %s равно не ожидаемому e0:d9:e3:ff:48:80, а %s" % (local_port2, device_id2))
        assert_that(port_id2 == DUT2.neighor1["interface"][0], "Значение Port id для Local port %s равно не ожидаемому te0/0/3, а %s" % (local_port2, port_id2))
        assert_that(capabilities2 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port2, capabilities2))
        assert_that(agent2 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port2, agent2))
        assert_that(system_name2 == DUT2.hostname, "Значение System name для Local port %s равно не ожидаемому atAR2, а %s" % (local_port2, system_name2))   
        
        assert_that(device_id3 != '', "Значение Device id для Local port %s равно не ожидаемому e0:d9:e3:ff:48:80, а %s" % (local_port3, device_id3))
        assert_that(port_id3 == DUT2.neighor1["interface"][1], "Значение Port id для Local port %s равно не ожидаемому te0/0/4, а %s" % (local_port3, port_id3))
        assert_that(capabilities3 == 'B R', "Значение Capabilities для Local port %s равно не ожидаемому B R, а %s" % (local_port3, capabilities3))
        assert_that(agent3 == 'N', "Значение Agent для Local port %s равно не ожидаемому N, а %s" % (local_port3, agent3))
        assert_that(system_name3 == DUT2.hostname, "Значение System name для Local port %s равно не ожидаемому atAR2, а %s" % (local_port3, system_name3)) 

