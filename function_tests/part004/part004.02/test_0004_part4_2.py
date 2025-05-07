from conftest import *
@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.02:Функциональное тестирование IS-IS') 
@allure.title('Проверка вывода команды show isis interface')    
@pytest.mark.part4_2
@pytest.mark.show_isis_interface
@pytest.mark.dependency(depends=["load_config042_dut1","load_config042_dut2","load_config042_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_isis_interface_part4_2 (DUT): 
# В данном тесте будем проверять вывод команды 'show isis interface'    
    allure.attach.file('./network-schemes/part4_show_isis_interface.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)  
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('show isis interface') 
    resp = conn.response 
    resp_output=resp.partition('show isis interface') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды show isis interface', attachment_type=allure.attachment_type.TEXT)   
#    print('show isis interface  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show isis interface'
# C помощью магии модуля textFSM сравниваем вывод команды 'show isis interface' c шаблоном в файле parse_show_isis_interface.txt 
    template = open('./templates/parse_show_isis_interface.txt')
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    result = fsm.ParseText(resp)
    conn.send('quit\r')
    conn.close()
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    Top1=processed_result[0]['Top1']
    Top2=processed_result[0]['Top2']
    int1_name=processed_result[0]['int_name']
    int1_oper_state=processed_result[0]['int_oper_state']
    int1_last_up=processed_result[0]['int_last_up']
    int1_l1_adj=processed_result[0]['int_l1_adj']
    int1_l2_adj=processed_result[0]['int_l2_adj']
    int1_l1_metric=processed_result[0]['int_l1_metric']
    int1_l2_metric=processed_result[0]['int_l2_metric']    
    int1_l1_priority=processed_result[0]['int_l1_priority']
    int1_l2_priority=processed_result[0]['int_l2_priority']
    int1_pdu=processed_result[0]['int_pdu']
    int1_mode=processed_result[0]['int_mode']    
    int1_bfd_4=processed_result[0]['int_bfd_4']
    int1_bfd_6=processed_result[0]['int_bfd_6']

    int2_name=processed_result[1]['int_name']
    int2_oper_state=processed_result[1]['int_oper_state']
    int2_last_up=processed_result[1]['int_last_up']
    int2_l1_adj=processed_result[1]['int_l1_adj']
    int2_l2_adj=processed_result[1]['int_l2_adj']
    int2_l1_metric=processed_result[1]['int_l1_metric']
    int2_l2_metric=processed_result[1]['int_l2_metric']    
    int2_l1_priority=processed_result[1]['int_l1_priority']
    int2_l2_priority=processed_result[1]['int_l2_priority']
    int2_pdu=processed_result[1]['int_pdu']
    int2_mode=processed_result[1]['int_mode']    
    int2_bfd_4=processed_result[1]['int_bfd_4']
    int2_bfd_6=processed_result[1]['int_bfd_6']    

    int3_name=processed_result[2]['int_name']
    int3_oper_state=processed_result[2]['int_oper_state']
    int3_last_up=processed_result[2]['int_last_up']
    int3_l1_adj=processed_result[2]['int_l1_adj']
    int3_l2_adj=processed_result[2]['int_l2_adj']
    int3_l1_metric=processed_result[2]['int_l1_metric']
    int3_l2_metric=processed_result[2]['int_l2_metric']    
    int3_l1_priority=processed_result[2]['int_l1_priority']
    int3_l2_priority=processed_result[2]['int_l2_priority']
    int3_pdu=processed_result[2]['int_pdu']
    int3_mode=processed_result[2]['int_mode']    
    int3_bfd_4=processed_result[2]['int_bfd_4']
    int3_bfd_6=processed_result[2]['int_bfd_6']

    int4_name=processed_result[3]['int_name']
    int4_oper_state=processed_result[3]['int_oper_state']
    int4_last_up=processed_result[3]['int_last_up']
    int4_l1_adj=processed_result[3]['int_l1_adj']
    int4_l2_adj=processed_result[3]['int_l2_adj']
    int4_l1_metric=processed_result[3]['int_l1_metric']
    int4_l2_metric=processed_result[3]['int_l2_metric']    
    int4_l1_priority=processed_result[3]['int_l1_priority']
    int4_l2_priority=processed_result[3]['int_l2_priority']
    int4_pdu=processed_result[3]['int_pdu']
    int4_mode=processed_result[3]['int_mode']    
    int4_bfd_4=processed_result[3]['int_bfd_4']
    int4_bfd_6=processed_result[3]['int_bfd_6']

    assert_that(Top1!='',"Строка 1 в заголовке вывода команды не соответсвует шаблону")
    assert_that(Top2!='',"Строка 2 в заголовке вывода команды не соответсвует шаблону")    

    assert_that(int1_name == DUT.neighor1['int_name'], "Интерфейс %s не соответсвует значению Bu1"%int1_name)
    assert_that(int1_oper_state == 'up',"Operstate  на интерфейсе %s не в состоянии UP"%int1_name)
    assert_that(int1_last_up != ''," Параметр LastUp на интерфейсе %s не соответсвует шаблону"%int1_name)
    assert_that(int1_l1_adj == '-',"L1 Adjacency на интерфейсе %s не соответсвует ожидаемому значению -. Т.е. их быть не должно, однако этот Параметр равен %s"%(int1_name,int1_l1_adj))
    assert_that(int1_l2_adj == '1',"L2 Adjacency на интерфейсе %s не соответсвует ожидаемому значению 1. Вместо этого параметр равен %s"%(int1_name,int1_l2_adj))
    assert_that(int1_l1_metric == '-',"L1 метрика на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 метрика равена %s"%(int1_name,int1_l1_metric))    
    assert_that(int1_l2_metric == '10',"L2 метрика на интерфейсе %s не соответсвует ожидаемому значению 10. Вместо этого L2 метрика равна %s"%(int1_name,int1_l2_metric))
    assert_that(int1_l1_priority == '-',"L1 Prioirity на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 Prioirity равен %s"%(int1_name,int1_l1_priority)) 
    assert_that(int1_l2_priority == '64',"L2 Prioirity на интерфейсе %s не соответсвует ожидаемому значению 64. Вместо этого L2 Prioirity равен %s"%(int1_name,int1_l2_priority))
    assert_that(int1_pdu == '1500',"Параметр  PDU на интерфейсе %s не соответсвует ожидаемому значению 1500. Вместо этого  PDU равен %s"%(int1_name,int1_pdu))
    assert_that(int1_mode == 'active',"Параметр  Mode на интерфейсе %s не соответсвует ожидаемому значению active. Вместо этого  Mode равен %s"%(int1_name,int1_mode))    
    assert_that(int1_bfd_4 == 'Y',"Флаг активности BFD IPV4 на интерфейсе %s не соответсвует ожидаемому значению Y. Вместо этого  BFD для IPV4 равен %s"%(int1_name,int1_bfd_4))
    assert_that(int1_bfd_6 == 'N',"Флаг активности BFD IPV6 на интерфейсе %s не соответсвует ожидаемому значению N. Вместо этого  BFD для IPV6 равен %s"%(int1_name,int1_bfd_6))            

    assert_that(int2_name == DUT.neighor2['int_name'],"Интерфейс %s не соответсвует значению Bu2"%int2_name)
    assert_that(int2_oper_state == 'up',"Operstate  на интерфейсе %s не в состоянии UP"%int2_name)
    assert_that(int2_last_up != ''," Параметр LastUp на интерфейсе %s не соответсвует шаблону"%int2_name)
    assert_that(int2_l1_adj == '-',"L1 Adjacency на интерфейсе %s не соответсвует ожидаемому значению -. Т.е. их быть не должно, однако этот Параметр равен %s"%(int2_name,int2_l1_adj))
    assert_that(int2_l2_adj == '1',"L2 Adjacency на интерфейсе %s не соответсвует ожидаемому значению 1. Вместо этого параметр равен %s"%(int2_name,int2_l2_adj))
    assert_that(int2_l1_metric == '-',"L1 метрика на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 метрика равена %s"%(int2_name,int2_l1_metric))    
    assert_that(int2_l2_metric == '10',"L2 метрика на интерфейсе %s не соответсвует ожидаемому значению 10. Вместо этого L2 метрика равна %s"%(int2_name,int2_l2_metric))
    assert_that(int2_l1_priority == '-',"L1 Prioirity на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 Prioirity равен %s"%(int2_name,int2_l1_priority)) 
    assert_that(int2_l2_priority == '64',"L2 Prioirity на интерфейсе %s не соответсвует ожидаемому значению 64. Вместо этого L2 Prioirity равен %s"%(int2_name,int2_l2_priority))
    assert_that(int2_pdu == '1500',"Параметр  PDU на интерфейсе %s не соответсвует ожидаемому значению 1500. Вместо этого  PDU равен %s"%(int2_name,int2_pdu))
    assert_that(int2_mode == 'active',"Параметр  Mode на интерфейсе %s не соответсвует ожидаемому значению active. Вместо этого  Mode равен %s"%(int2_name,int2_mode))    
    assert_that(int2_bfd_4 == 'Y',"Флаг активности BFD IPV4 на интерфейсе %s не соответсвует ожидаемому значению Y. Вместо этого  BFD для IPV4 равен %s"%(int2_name,int2_bfd_4))
    assert_that(int2_bfd_6 == 'N',"Флаг активности BFD IPV6 на интерфейсе %s не соответсвует ожидаемому значению N. Вместо этого  BFD для IPV6 равен %s"%(int2_name,int2_bfd_6))            

    assert_that(int3_name == 'lo10',"Интерфейс %s не соответсвует значению Lo10"%int3_name)
    assert_that(int3_oper_state == 'up',"Operstate  на интерфейсе %s не в состоянии UP"%int3_name)
    assert_that(int3_last_up == 'never'," Параметр LastUp на интерфейсе %s не соответсвует значению never"%int3_name)
    assert_that(int3_l1_adj == '-',"L1 Adjacency на интерфейсе %s не соответсвует ожидаемому значению -. Т.е. их быть не должно, однако этот Параметр равен %s"%(int3_name,int3_l1_adj))
    assert_that(int3_l2_adj == '-',"L2 Adjacency на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого параметр равен %s"%(int3_name,int3_l2_adj))
    assert_that(int3_l1_metric == '-',"L1 метрика на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 метрика равена %s"%(int3_name,int3_l1_metric))    
    assert_that(int3_l2_metric == '-',"L2 метрика на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L2 метрика равна %s"%(int3_name,int3_l2_metric))
    assert_that(int3_l1_priority == '-',"L1 Prioirity на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 Prioirity равен %s"%(int3_name,int3_l1_priority)) 
    assert_that(int3_l2_priority == '-',"L2 Prioirity на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L2 Prioirity равен %s"%(int3_name,int3_l2_priority))
    assert_that(int3_pdu == '1492',"Параметр  PDU на интерфейсе %s не соответсвует ожидаемому значению 1492. Вместо этого  PDU равен %s"%(int3_name,int3_pdu))
    assert_that(int3_mode == 'passive',"Параметр  Mode на интерфейсе %s не соответсвует ожидаемому значению passive. Вместо этого  Mode равен %s"%(int3_name,int3_mode))    
    assert_that(int3_bfd_4 == 'N',"Флаг активности BFD IPV4 на интерфейсе %s не соответсвует ожидаемому значению N. Вместо этого  BFD для IPV4 равен %s"%(int3_name,int3_bfd_4))
    assert_that(int3_bfd_6 == 'N',"Флаг активности BFD IPV6 на интерфейсе %s не соответсвует ожидаемому значению N. Вместо этого  BFD для IPV6 равен %s"%(int3_name,int3_bfd_6))            

    assert_that(int4_name == DUT.neighor3['int_name'],"Интерфейс %s не соответсвует значению te0/0/11.352"%int4_name)
    assert_that(int4_oper_state == 'up',"Operstate  на интерфейсе %s не в состоянии UP"%int4_name)
    assert_that(int4_last_up != ''," Параметр LastUp на интерфейсе %s не соответсвует шаблону"%int4_name)
    assert_that(int4_l1_adj == '-',"L1 Adjacency на интерфейсе %s не соответсвует ожидаемому значению -. Т.е. их быть не должно, однако этот Параметр равен %s"%(int4_name,int4_l1_adj))
    assert_that(int4_l2_adj == '1',"L2 Adjacency на интерфейсе %s не соответсвует ожидаемому значению 1. Вместо этого параметр равен %s"%(int4_name,int4_l2_adj))
    assert_that(int4_l1_metric == '-',"L1 метрика на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 метрика равена %s"%(int4_name,int4_l1_metric))    
    assert_that(int4_l2_metric == '10',"L2 метрика на интерфейсе %s не соответсвует ожидаемому значению 10. Вместо этого L2 метрика равна %s"%(int4_name,int4_l2_metric))
    assert_that(int4_l1_priority == '-',"L1 Prioirity на интерфейсе %s не соответсвует ожидаемому значению -. Вместо этого L1 Prioirity равен %s"%(int4_name,int4_l1_priority)) 
    assert_that(int4_l2_priority == '64',"L2 Prioirity на интерфейсе %s не соответсвует ожидаемому значению 64. Вместо этого L2 Prioirity равен %s"%(int4_name,int4_l2_priority))
    assert_that(int4_pdu == '1500',"Параметр  PDU на интерфейсе %s не соответсвует ожидаемому значению 1500. Вместо этого  PDU равен %s"%(int4_name,int4_pdu))
    assert_that(int4_mode == 'active',"Параметр  Mode на интерфейсе %s не соответсвует ожидаемому значению active. Вместо этого  Mode равен %s"%(int4_name,int4_mode))    
    assert_that(int4_bfd_4 == 'N',"Флаг активности BFD IPV4 на интерфейсе %s не соответсвует ожидаемому значению N. Вместо этого  BFD для IPV4 равен %s"%(int4_name,int4_bfd_4))
    assert_that(int4_bfd_6 == 'N',"Флаг активности BFD IPV6 на интерфейсе %s не соответсвует ожидаемому значению N. Вместо этого  BFD для IPV6 равен %s"%(int4_name,int4_bfd_6))                