from conftest import *

@allure.feature('03:Функциональное тестирование протокола LLDP')
@allure.story('3.2:Проверка LLDP')
@allure.title('В данном тесте будем  проверять вывод комнады show lldp neighbors detail')
@pytest.mark.part3
@pytest.mark.show_lldp_neighbors_detail
@pytest.mark.dependency(depends=["load_config003_dut1","load_config003_dut2","load_config003_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_lldp_neighbors_detail_part3(DUT): 
	allure.attach.file('./network-schemes/part3_show_lldp_neighbor_detail.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
# В данном тесте будем проверять вывод команды 'show lldp neighbor'	 
	resp = ''
	conn = Telnet()
	acc = Account(DUT.login , DUT.password)
	conn.connect(DUT.host_ip)
	conn.login(acc)
	conn.set_prompt('#')
	conn.execute("terminal datadump")
	conn.set_prompt('#')
	cmd = ('show lldp neighbors detail')
	conn.execute('terminal datadump')
	conn.execute(cmd) 
	resp = conn.response
	allure.attach(resp, f'Вывод команды {cmd}', attachment_type=allure.attachment_type.TEXT)
#	print('show lldp neighbors detail  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show lldp neighbor detail'
# C помощью магии модуля textFSM сравниваем вывод команды 'show users' c шаблоном в файле parse_show_users.txt 
	template = open('./templates/parse_show_lldp_neighbor_detail.txt')
	fsm = textfsm.TextFSM(template)
	result = fsm.ParseTextToDicts(resp)
	assert_that(len(result) > 0, 'Пустой вывод команды show lldp neighbors detail')
#	print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга

	loc_index = 0
	if DUT.hostname == DUT1.hostname:
		located_index = locate_index_in_ListOfDict(result, 'portN', DUT1.neighor2["full_interface"][0], loc_index)
		assert_that(located_index!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/1")
		located_index1 = locate_index_in_ListOfDict(result, 'portN', DUT1.neighor2["full_interface"][1], loc_index)
		assert_that(located_index1!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/2")  
		located_index2 = locate_index_in_ListOfDict(result, 'portN', DUT1.neighor1["full_interface"][0], loc_index)
		assert_that(located_index2!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/3")  
		located_index3 = locate_index_in_ListOfDict(result, 'portN', DUT1.neighor1["full_interface"][1], loc_index)
		assert_that(located_index3!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/4")  
		
	if DUT.hostname == DUT2.hostname:
		located_index = locate_index_in_ListOfDict(result, 'portN', DUT2.neighor1["full_interface"][0], loc_index)
		assert_that(located_index!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/3")
		located_index1 = locate_index_in_ListOfDict(result, 'portN', DUT2.neighor1["full_interface"][1], loc_index)
		assert_that(located_index1!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/4")  
		located_index2 = locate_index_in_ListOfDict(result, 'portN', DUT2.neighor2["full_interface"][0], loc_index)
		assert_that(located_index2!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/7")  
		located_index3 = locate_index_in_ListOfDict(result, 'portN', DUT2.neighor2["full_interface"][1], loc_index)
		assert_that(located_index3!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/0/8")  
		
	if DUT.hostname == DUT3.hostname:
		located_index = locate_index_in_ListOfDict(result, 'portN', DUT3.neighor1["full_interface"][0], loc_index)
		assert_that(located_index!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/1/13")
		located_index1 = locate_index_in_ListOfDict(result, 'portN', DUT3.neighor1["full_interface"][1], loc_index)
		assert_that(located_index1!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/1/14")  
		located_index2 = locate_index_in_ListOfDict(result, 'portN', DUT3.neighor2["full_interface"][0], loc_index)
		assert_that(located_index2!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/8/3")  
		located_index3 = locate_index_in_ListOfDict(result, 'portN', DUT3.neighor2["full_interface"][1], loc_index)
		assert_that(located_index3!=999, f"В выводе команды {cmd} не обнаружен Local Interface: Tengigabitethernet0/8/4")  
		
	port1 = result[located_index]['portN']
	p1_chassis = result[located_index]['p_chassis']
	p1_port_id = result[located_index]['p_port_id']
	p1_neib_mac = result[located_index]['p_neib_mac']
	p1_sysname = result[located_index]['p_sys_name']
	p1_sysdescr = result[located_index]['p_sys_descr']
	p1_syscap = result[located_index]['p_syscap']
	p1_encap = result[located_index]['p_encap']
	p1_manage_ip = result[located_index]['p_manage_ip']
	
	port2 = result[located_index1]['portN']
	p2_chassis = result[located_index1]['p_chassis']
	p2_port_id = result[located_index1]['p_port_id']
	p2_neib_mac = result[located_index1]['p_neib_mac']
	p2_sysname = result[located_index1]['p_sys_name']
	p2_sysdescr = result[located_index1]['p_sys_descr']
	p2_syscap = result[located_index1]['p_syscap']
	p2_encap = result[located_index1]['p_encap']
	p2_manage_ip = result[located_index1]['p_manage_ip']
	
	port3 = result[located_index2]['portN']
	p3_chassis = result[located_index2]['p_chassis']
	p3_port_id = result[located_index2]['p_port_id']
	p3_neib_mac = result[located_index2]['p_neib_mac']
	p3_sysname = result[located_index2]['p_sys_name']
	p3_sysdescr = result[located_index2]['p_sys_descr']
	p3_syscap = result[located_index2]['p_syscap']
	p3_encap = result[located_index2]['p_encap']
	p3_manage_ip = result[located_index2]['p_manage_ip']
	
	port4 = result[located_index3]['portN']
	p4_chassis = result[located_index3]['p_chassis']
	p4_port_id = result[located_index3]['p_port_id']
	p4_neib_mac = result[located_index3]['p_neib_mac']
	p4_sysname = result[located_index3]['p_sys_name']
	p4_sysdescr = result[located_index3]['p_sys_descr']
	p4_syscap = result[located_index3]['p_syscap']
	p4_encap = result[located_index3]['p_encap']
	p4_manage_ip = result[located_index3]['p_manage_ip']

	conn.send('quit\r')
	conn.close()
	
	if DUT.hostname == DUT1.hostname:
		assert_that(p1_chassis !='', f"Chassis ID соседа обнаруженного на порту {port1} равен не ожидаемому e0:d9:e3:ff:48:80, а {p1_chassis}")
		assert_that(p1_port_id == DUT2.neighor2["interface"][0], f"Port id соседа обнаруженного на порту {port1} равен не ожидаемому te0/0/7, а {p1_port_id}")
		assert_that(p1_neib_mac != '', f"MAC адрес соседа обнаруженного на порту {port1} равен не ожидаемому e0:d9:e3:ff:48:87, а {p1_neib_mac}")
		assert_that(p1_sysname == DUT2.hostname, f"System Name соседа обнаруженного на порту {port1} равен не ожидаемому atAR2, а {p1_sysname}")
		assert_that(p1_sysdescr != '', f"System Description соседа обнаруженного на порту {port1} не равен ожидаемому Eltex ME5200 carrier DUT")
		assert_that(p1_syscap != '', f"System Capabilities соседа обнаруженного на порту {port1} не равен ожидаемому Bridge, DUT")
		assert_that(p1_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port1} не равен ожидаемому Bridge, DUT")
		assert_that(p1_manage_ip == DUT2.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port1} равен не ожидаемому 1.0.0.2, а {p1_manage_ip}")

		assert_that(p2_chassis !='', f"Chassis ID соседа обнаруженного на порту {port2} равен не ожидаемому e0:d9:e3:ff:48:80, а {p2_chassis}")
		assert_that(p2_port_id == DUT2.neighor2["interface"][1], f"Port id соседа обнаруженного на порту {port2} равен не ожидаемому te0/0/8, а {p2_port_id}")
		assert_that(p2_chassis != '', f"MAC адрес соседа обнаруженного на порту {port2} равен не ожидаемому e0:d9:e3:ff:48:88, а {p2_neib_mac}")
		assert_that(p2_sysname == DUT2.hostname, f"System Name соседа обнаруженного на порту {port2} равен не ожидаемому atAR2, а {p2_sysname}")
		assert_that(p2_sysdescr != '', f"System Description соседа обнаруженного на порту {port2} не равен ожидаемому Eltex ME5200 carrier DUT")
		assert_that(p2_syscap != '', f"System Capabilities соседа обнаруженного на порту {port2} не равен ожидаемому Bridge, DUT")
		assert_that(p2_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port2} не равен ожидаемому Bridge, DUT")
		assert_that(p2_manage_ip == DUT2.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port2} равен не ожидаемому 1.0.0.2, а {p2_manage_ip}")

		assert_that(p3_chassis !='', f"Chassis ID соседа обнаруженного на порту {port3} равен не ожидаемому a8:f9:4b:8b:92:80, а {p3_chassis}")
		assert_that(p3_port_id == DUT3.neighor1["interface"][0], f"Port id соседа обнаруженного на порту {port3} равен не ожидаемому te0/1/13, а {p3_port_id}")
		assert_that(p3_chassis != '', f"MAC адрес соседа обнаруженного на порту {port3} равен не ожидаемому a8:f9:4b:8b:92:ad, а {p3_neib_mac}")
		assert_that(p3_sysname == DUT3.hostname, f"System Name соседа обнаруженного на порту {port3} равен не ожидаемому atDR1, а {p3_sysname}")
		assert_that(p3_sysdescr != '', f"System Description соседа обнаруженного на порту {port3} не равен ожидаемому Eltex ME5000 modular carrier DUT")
		assert_that(p3_syscap != '', f"System Capabilities соседа обнаруженного на порту {port3} не равен ожидаемому Bridge, DUT")
		assert_that(p3_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port3} не равен ожидаемому Bridge, DUT")
		assert_that(p3_manage_ip == DUT3.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port3} равен не ожидаемому 1.0.0.1, а {p3_manage_ip}")
		
		assert_that(p4_chassis !='', f"Chassis ID соседа обнаруженного на порту {port4} равен не ожидаемому a8:f9:4b:8b:92:80, а {p4_chassis}")
		assert_that(p4_port_id == DUT3.neighor1["interface"][1], f"Port id соседа обнаруженного на порту {port4} равен не ожидаемому te0/1/14, а {p4_port_id}")
		assert_that(p4_chassis != '', f"MAC адрес соседа обнаруженного на порту {port4} равен не ожидаемому a8:f9:4b:8b:92:ae, а {p4_neib_mac}")
		assert_that(p4_sysname == DUT3.hostname, f"System Name соседа обнаруженного на порту {port4} равен не ожидаемому atDR1, а {p4_sysname}")
		assert_that(p4_sysdescr != '', f"System Description соседа обнаруженного на порту {port4} не равен ожидаемому Eltex ME5000 modular carrier DUT")
		assert_that(p4_syscap != '', f"System Capabilities соседа обнаруженного на порту {port4} не равен ожидаемому Bridge, DUT")
		assert_that(p4_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port4} не равен ожидаемому Bridge, DUT")
		assert_that(p4_manage_ip == DUT3.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port4} равен не ожидаемому 1.0.0.1, а {p4_manage_ip}")		
		
	if DUT.hostname == DUT2.hostname:
		assert_that(p1_chassis !='', f"Chassis ID соседа обнаруженного на порту {port1} равен не ожидаемому a8:f9:4b:8b:92:80, а {p1_chassis}")
		assert_that(p1_port_id == DUT3.neighor2["interface"][0], f"Port id соседа обнаруженного на порту {port1} равен не ожидаемому te0/8/3, а {p1_port_id}")
		assert_that(p1_chassis != '', f"MAC адрес соседа обнаруженного на порту {port1} равен не ожидаемому a8:f9:4b:8b:93:83, а {p1_neib_mac}")
		assert_that(p1_sysname == DUT3.hostname, f"System Name соседа обнаруженного на порту {port1} равен не ожидаемому atDR1, а {p1_sysname}")
		assert_that(p1_sysdescr != '', f"System Description соседа обнаруженного на порту {port1} не равен ожидаемому Eltex ME5000 modular carrier DUT")
		assert_that(p1_syscap != '', f"System Capabilities соседа обнаруженного на порту {port1} не равен ожидаемому Bridge, DUT")
		assert_that(p1_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port1} не равен ожидаемому Bridge, DUT")
		assert_that(p1_manage_ip == DUT3.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port1} равен не ожидаемому 1.0.0.1, а {p1_manage_ip}")

		assert_that(p2_chassis !='', f"Chassis ID соседа обнаруженного на порту {port2} равен не ожидаемому a8:f9:4b:8b:92:80, а {p2_chassis}")
		assert_that(p2_port_id == DUT3.neighor2["interface"][1], f"Port id соседа обнаруженного на порту {port2} равен не ожидаемому te0/8/4, а {p2_port_id}")
		assert_that(p2_chassis != '', f"MAC адрес соседа обнаруженного на порту {port2} равен не ожидаемому a8:f9:4b:8b:93:84, а {p2_neib_mac}")
		assert_that(p2_sysname == DUT3.hostname, f"System Name соседа обнаруженного на порту {port2} равен не ожидаемому atDR1, а {p2_sysname}")
		assert_that(p2_sysdescr != '', f"System Description соседа обнаруженного на порту {port2} не равен ожидаемому Eltex ME5000 modular carrier DUT")
		assert_that(p2_syscap != '', f"System Capabilities соседа обнаруженного на порту {port2} не равен ожидаемому Bridge, DUT")
		assert_that(p2_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port2} не равен ожидаемому Bridge, DUT")
		assert_that(p2_manage_ip == DUT3.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port2} равен не ожидаемому 1.0.0.1, а {p2_manage_ip}")

		assert_that(p3_chassis !='', f"Chassis ID соседа обнаруженного на порту {port3} равен не ожидаемому e4:5a:d4:de:c8:80, а {p3_chassis}")
		assert_that(p3_port_id == DUT1.neighor2["interface"][0], f"Port id соседа обнаруженного на порту {port3} равен не ожидаемому te0/0/1, а {p3_port_id}")
		assert_that(p3_chassis != '', f"MAC адрес соседа обнаруженного на порту {port3} равен не ожидаемому e4:5a:d4:de:c8:81, а {p3_neib_mac}")
		assert_that(p3_sysname == DUT1.hostname, f"System Name соседа обнаруженного на порту {port3} равен не ожидаемому atAR1, а {p3_sysname}")
		assert_that(p3_sysdescr != '', f"System Description соседа обнаруженного на порту {port3} не равен ожидаемому Eltex ME2001 carrier DUT")
		assert_that(p3_syscap != '', f"System Capabilities соседа обнаруженного на порту {port3} не равен ожидаемому Bridge, DUT")
		assert_that(p3_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port3} не равен ожидаемому Bridge, DUT")
		assert_that(p3_manage_ip == DUT1.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port3} равен не ожидаемому 1.0.0.3, а {p3_manage_ip}")
		
		assert_that(p4_chassis !='', f"Chassis ID соседа обнаруженного на порту {port4} равен не ожидаемому e4:5a:d4:de:c8:80, а {p4_chassis}")
		assert_that(p4_port_id == DUT1.neighor2["interface"][1], f"Port id соседа обнаруженного на порту {port4} равен не ожидаемому te0/0/2, а {p4_port_id}")
		assert_that(p4_chassis != '', f"MAC адрес соседа обнаруженного на порту {port4} равен не ожидаемому e4:5a:d4:de:c8:82, а {p4_neib_mac}")
		assert_that(p4_sysname == DUT1.hostname, f"System Name соседа обнаруженного на порту {port4} равен не ожидаемому atAR1, а {p4_sysname}")
		assert_that(p4_sysdescr != '', f"System Description соседа обнаруженного на порту {port4} не равен ожидаемому Eltex ME2001 carrier DUT")
		assert_that(p4_syscap != '', f"System Capabilities соседа обнаруженного на порту {port4} не равен ожидаемому Bridge, DUT")
		assert_that(p4_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port4} не равен ожидаемому Bridge, DUT")
		assert_that(p4_manage_ip == DUT1.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port4} равен не ожидаемому 1.0.0.3, а {p4_manage_ip}")   
		
	if DUT.hostname == DUT3.hostname:
		assert_that(p1_chassis !='', f"Chassis ID соседа обнаруженного на порту {port1} равен не ожидаемому e4:5a:d4:de:c8:80, а {p1_chassis}")
		assert_that(p1_port_id == DUT1.neighor1["interface"][0], f"Port id соседа обнаруженного на порту {port1} равен не ожидаемому te0/0/3, а {p1_port_id}")
		assert_that(p1_chassis != '', f"MAC адрес соседа обнаруженного на порту {port1} равен не ожидаемому e4:5a:d4:de:c8:83, а {p1_neib_mac}")
		assert_that(p1_sysname == DUT1.hostname, f"System Name соседа обнаруженного на порту {port1} равен не ожидаемому atAR1, а {p1_sysname}")
		assert_that(p1_sysdescr != '', f"System Description соседа обнаруженного на порту {port1} не равен ожидаемому Eltex ME2001 carrier DUT")
		assert_that(p1_syscap != '', f"System Capabilities соседа обнаруженного на порту {port1} не равен ожидаемому Bridge, DUT")
		assert_that(p1_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port1} не равен ожидаемому Bridge, DUT")
		assert_that(p1_manage_ip == DUT1.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port1} равен не ожидаемому 1.0.0.3, а {p1_manage_ip}")

		assert_that(p2_chassis !='', f"Chassis ID соседа обнаруженного на порту {port2} равен не ожидаемому e4:5a:d4:de:c8:80, а {p2_chassis}")
		assert_that(p2_port_id == DUT1.neighor1["interface"][1], f"Port id соседа обнаруженного на порту {port2} равен не ожидаемому te0/0/4, а {p2_port_id}")
		assert_that(p2_chassis != '', f"MAC адрес соседа обнаруженного на порту {port2} равен не ожидаемому e4:5a:d4:de:c8:84, а {p2_neib_mac}")
		assert_that(p2_sysname == DUT1.hostname, f"System Name соседа обнаруженного на порту {port2} равен не ожидаемому atAR1, а {p2_sysname}")
		assert_that(p2_sysdescr != '', f"System Description соседа обнаруженного на порту {port2} не равен ожидаемому Eltex ME2001 carrier DUT")
		assert_that(p2_syscap != '', f"System Capabilities соседа обнаруженного на порту {port2} не равен ожидаемому Bridge, DUT")
		assert_that(p2_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port2} не равен ожидаемому Bridge, DUT")
		assert_that(p2_manage_ip == DUT1.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port2} равен не ожидаемому 1.0.0.3, а {p2_manage_ip}")

		assert_that(p3_chassis !='', f"Chassis ID соседа обнаруженного на порту {port3} равен не ожидаемому e0:d9:e3:ff:48:80, а {p3_chassis}")
		assert_that(p3_port_id == DUT2.neighor1["interface"][0], f"Port id соседа обнаруженного на порту {port3} равен не ожидаемому te0/0/3, а {p3_port_id}")
		assert_that(p3_chassis != '', f"MAC адрес соседа обнаруженного на порту {port3} равен не ожидаемому e0:d9:e3:ff:48:83, а {p3_neib_mac}")
		assert_that(p3_sysname == DUT2.hostname, f"System Name соседа обнаруженного на порту {port3} равен не ожидаемому atAR2, а {p3_sysname}")
		assert_that(p3_sysdescr != '', f"System Description соседа обнаруженного на порту {port3} не равен ожидаемому Eltex ME5200 carrier DUT")
		assert_that(p3_syscap != '', f"System Capabilities соседа обнаруженного на порту {port3} не равен ожидаемому Bridge, DUT")
		assert_that(p3_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port3} не равен ожидаемому Bridge, DUT")
		assert_that(p3_manage_ip == DUT2.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port3} равен не ожидаемому 1.0.0.2, а {p3_manage_ip}")
		
		assert_that(p4_chassis !='', f"Chassis ID соседа обнаруженного на порту {port4} равен не ожидаемому e0:d9:e3:ff:48:80, а {p4_chassis}")
		assert_that(p4_port_id == DUT2.neighor1["interface"][1], f"Port id соседа обнаруженного на порту {port4} равен не ожидаемому te0/0/4, а {p4_port_id}")
		assert_that(p4_chassis != '', f"MAC адрес соседа обнаруженного на порту {port4} равен не ожидаемому e0:d9:e3:ff:48:84, а {p4_neib_mac}")
		assert_that(p4_sysname == DUT2.hostname, f"System Name соседа обнаруженного на порту {port4} равен не ожидаемому atAR2, а {p4_sysname}")
		assert_that(p4_sysdescr != '', f"System Description соседа обнаруженного на порту {port4} не равен ожидаемому Eltex ME5200 carrier DUT")
		assert_that(p4_syscap != '', f"System Capabilities соседа обнаруженного на порту {port4} не равен ожидаемому Bridge, DUT")
		assert_that(p4_encap != '', f"Enabled Capabilities соседа обнаруженного на порту {port4} не равен ожидаемому Bridge, DUT")
		assert_that(p4_manage_ip == DUT2.loopback["ip_witout_mask"], f"IP адрес управления соседа обнаруженного на порту {port4} равен не ожидаемому 1.0.0.2, а {p4_manage_ip}")   
