from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.02:Функциональное тестирование IS-IS')  
@allure.story('Проверка вывода команды show isis neighbor на соответствие шаблону')  
@pytest.mark.part4_2
@pytest.mark.show_isis_neighbor
@pytest.mark.dependency(depends=["load_config042_dut1","load_config042_dut2","load_config042_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
							   
def test_show_isis_neighbor_part4_2(DUT):
# В данном тесте будем проверять вывод команды 'show isis neighbor' 
	allure.attach.file('./network-schemes/part4_show_isis_neighbors.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)	 
	resp = ''
	conn = Telnet()
	acc = Account(DUT.login, DUT.password)
	conn.connect(DUT.host_ip)
	conn.login(acc)
	conn.set_prompt('#')
	if DUT.host_ip == DUT1.host_ip:
		time.sleep(60)  # Подождем пока поднимутся isis соседства.
	cmd = ('show isis neighbors')
	conn.execute(cmd) 
	resp = conn.response   
	allure.attach(resp, 'Вывод команды %s' % cmd, attachment_type=allure.attachment_type.TEXT)	  
#	print('show isis neighbors  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show isis neighbors'
# C помощью магии модуля textFSM сравниваем вывод команды 'show isis neighbors' c шаблоном в файле parse_isis_neighbors.txt 
	template = open('./templates/parse_show_isis_neighbors.txt')
	fsm = textfsm.TextFSM(template)
	result = fsm.ParseTextToDicts(resp)
	loc_index = 0
	if DUT.hostname == DUT1.hostname:
		located_index = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT3.hostname, loc_index)
		assert_that(located_index!=999, "В выводе команды %s не обнаружен сосед atDR1" % cmd)  
		located_index1 = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT2.hostname, loc_index)
		assert_that(located_index1!=999, "В выводе команды %s не обнаружен сосед atAR2" % cmd)	
		located_index2 = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT4.hostname, loc_index)
		assert_that(located_index2!=999, "В выводе команды %s не обнаружен сосед LABR01" % cmd) 
	if DUT.hostname == DUT2.hostname:
		located_index = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT3.hostname, loc_index)
		assert_that(located_index!=999, "В выводе команды %s не обнаружен сосед atDR1" % cmd)  
		located_index1 = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT1.hostname, loc_index)
		assert_that(located_index1!=999, "В выводе команды %s не обнаружен сосед atAR1" % cmd)	
		located_index2 = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT4.hostname, loc_index)
		assert_that(located_index2!=999, "В выводе команды %s не обнаружен сосед LABR01" % cmd) 
	if DUT.hostname == DUT3.hostname:
		located_index = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT1.hostname, loc_index)
		assert_that(located_index!=999, "В выводе команды %s не обнаружен сосед atAR1" % cmd)  
		located_index1 = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT2.hostname, loc_index)
		assert_that(located_index1!=999, "В выводе команды %s не обнаружен сосед atAR2" % cmd)	
		located_index2 = locate_index_in_ListOfDict(result, 'nbr_hostname', DUT4.hostname, loc_index)
		assert_that(located_index2!=999, "В выводе команды %s не обнаружен сосед LABR01" % cmd)	  
	
			
	#	print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
	line1 = result[located_index]['line1']
	Top = result[located_index]['Top']
	nbr_system_id = result[located_index]['nbr_system_id']
	nbr_int = result[located_index]['nbr_int']
	nbr_state = result[located_index]['nbr_state']
	nbr_type = result[located_index]['nbr_type']
	nbr_nsf = result[located_index]['nbr_nsf']
	nbr_bfd = result[located_index]['nbr_bfd']
	nbr_hostname = result[located_index]['nbr_hostname']
	
	line11 = result[located_index1]['line1']
	Top1 = result[located_index1]['Top']
	nbr_system_id1 = result[located_index1]['nbr_system_id']
	nbr_int1 = result[located_index1]['nbr_int']
	nbr_state1 = result[located_index1]['nbr_state']
	nbr_type1 = result[located_index1]['nbr_type']
	nbr_nsf1 = result[located_index1]['nbr_nsf']
	nbr_bfd1 = result[located_index1]['nbr_bfd']
	nbr_hostname1 = result[located_index1]['nbr_hostname']
	
	line12 = result[located_index2]['line1']
	Top2 = result[located_index2]['Top']
	nbr_system_id2 = result[located_index2]['nbr_system_id']
	nbr_int2 = result[located_index2]['nbr_int']
	nbr_state2 = result[located_index2]['nbr_state']
	nbr_type2 = result[located_index2]['nbr_type']
	nbr_nsf2 = result[located_index2]['nbr_nsf']
	nbr_bfd2 = result[located_index2]['nbr_bfd']
	nbr_hostname2 = result[located_index2]['nbr_hostname']
	
	assert_that((line1 != '')or(line11 != '')or(line12 != ''), "Строка IS-IS Router test adjacency не соответсвует шаблону")
	assert_that((Top != '')or(Top1 != '')or(Top2 != ''), "Заголовок табличного вывода не соответсвует шаблону")
	
	if DUT.hostname == DUT1.hostname:
		assert_that(nbr_system_id == DUT3.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0001, a %s" % (nbr_hostname, nbr_system_id))
		assert_that(nbr_system_id1 == DUT2.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0002, a %s" % (nbr_hostname1, nbr_system_id1))
		assert_that(nbr_system_id2 == DUT4.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0004, a %s" % (nbr_hostname2, nbr_system_id2))
		
	if DUT.hostname == DUT2.hostname:
		assert_that(nbr_system_id == DUT3.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0001, a %s" % (nbr_hostname, nbr_system_id))
		assert_that(nbr_system_id1 == DUT1.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0003, a %s" % (nbr_hostname1, nbr_system_id1))
		assert_that(nbr_system_id2 == DUT4.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0004, a %s" % (nbr_hostname2, nbr_system_id2))		
		
	if DUT.hostname == DUT3.hostname:
		assert_that(nbr_system_id == DUT1.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0003, a %s" % (nbr_hostname, nbr_system_id))
		assert_that(nbr_system_id1 == DUT2.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0002, a %s" % (nbr_hostname1, nbr_system_id1))
		assert_that(nbr_system_id2 == DUT4.isis[8:22], "Значение System ID для соседа %s равно не ожидаемому 0010.0000.0004, a %s" % (nbr_hostname2, nbr_system_id2))
	 
	
	assert_that(nbr_int == 'bu1', "Значение Interface для соседа %s равно не ожидаемому bu1, a %s" % (nbr_hostname, nbr_int))
	assert_that(nbr_state == 'up', "Значение State для соседа %s равно не ожидаемому up, a %s" % (nbr_hostname, nbr_state))
	assert_that(nbr_type == 'level-2', "Значение Type для соседа %s равно не ожидаемому level-2, a %s" % (nbr_hostname, nbr_type))
	assert_that(nbr_nsf == 'true', "Значение NSF для соседа %s равно не ожидаемому true, a %s" % (nbr_hostname, nbr_nsf))
	assert_that(nbr_bfd == 'up', "Значение BFD для соседа %s равно не ожидаемому up, a %s" % (nbr_hostname, nbr_bfd))
	
	assert_that(nbr_int1 == 'bu2', "Значение Interface для соседа %s равно не ожидаемому bu2, a %s" % (nbr_hostname1, nbr_int1))
	assert_that(nbr_state1 == 'up', "Значение State для соседа %s равно не ожидаемому up, a %s" % (nbr_hostname1, nbr_state1))
	assert_that(nbr_type1 == 'level-2', "Значение Type для соседа %s равно не ожидаемому level-2, a %s" % (nbr_hostname1, nbr_type1))
	assert_that(nbr_nsf1 == 'true', "Значение NSF для соседа %s равно не ожидаемому true, a %s" % (nbr_hostname1, nbr_nsf1))
	assert_that(nbr_bfd1 == 'up', "Значение BFD для соседа %s равно не ожидаемому up, a %s" % (nbr_hostname1, nbr_bfd1))   
	
	interface_labr01 = 0
	interface_labr01 = DUT.neighor3['int_name']
	
	assert_that(nbr_int2 == '%s' % interface_labr01, "Значение Interface для соседа %s равно не ожидаемому %s, a %s" % (nbr_hostname2, interface_labr01, nbr_int2))
	assert_that(nbr_state2 == 'up', "Значение State для соседа %s равно не ожидаемому up, a %s" % (nbr_hostname2, nbr_state2))
	assert_that(nbr_type2 == 'level-2', "Значение Type для соседа %s равно не ожидаемому level-2, a %s" % (nbr_hostname2, nbr_type2))
	assert_that(nbr_nsf2 == 'true', "Значение NSF для соседа %s равно не ожидаемому true, a %s" % (nbr_hostname2, nbr_nsf2))
	assert_that(nbr_bfd2 == 'none', "Значение BFD для соседа %s равно не ожидаемому none, a %s" % (nbr_hostname2, nbr_bfd2))	  
