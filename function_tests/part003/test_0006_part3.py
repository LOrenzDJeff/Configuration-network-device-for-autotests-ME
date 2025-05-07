from conftest import *

@allure.feature('03:Функциональное тестирование протокола LLDP')
@allure.story('3.2:Проверка LLDP')
@allure.title('В данном тесте будем  проверять вывод комнады show lldp interface')
@pytest.mark.part3
@pytest.mark.show_lldp_interface
@pytest.mark.dependency(depends=["load_config003_dut1","load_config003_dut2","load_config003_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
									  
#@pytest.mark.parametrize('ip, int1, int2, int3, int4' , [('192.168.17.138', 'te0/0/1', 'te0/0/2', 'te0/0/3', 'te0/0/4') , ('192.168.17.139', 'te0/0/1', 'te0/0/2', 'te0/0/3', 'te0/0/4') , ('192.168.17.146', 'te0/1/3', 'te0/1/4', 'te0/8/3', 'te0/8/4')])
def test_show_lldp_interface_part3 (DUT): 
    allure.attach.file('./network-schemes/part3_show_lldp_interface.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)
# В данном тесте будем проверять вывод команды 'show lldp interface'
    conn = Telnet()
    acc = Account(DUT.login , DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    

    arr_name = [] # массив параметров
    arr_value = [] # массив значений параметров 
    
    for interface in [DUT.neighor1["full_interface"][0], DUT.neighor1["full_interface"][1], DUT.neighor2["full_interface"][0],DUT.neighor2["full_interface"][1]]:
        arr_name.clear()
        arr_value.clear()
        conn.execute('show lldp interface %s'%interface) 
        resp = conn.response
        allure.attach(resp, 'Вывод команды show lldp interface %s'%interface, attachment_type=allure.attachment_type.TEXT) 
        resp_output = resp.partition('Interface')
        new_resp = resp_output[1]+resp_output[2]                  
#    print('show lldp interface  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show lldp interface'
# C помощью магии модуля textFSM сравниваем вывод команды 'show lldp interface' c шаблоном в файле parse_show_lldp_interface.txt 
        template = open('./templates/parse_show_lldp_interface.txt')
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseTextToDicts(new_resp)
        for i in range(12):
            arr_name.append(result[i]['name'])
            arr_value.append(result[i]['value'])
        #print(arr_name)
        #print(arr_value)
        for i in range(12):
            if arr_name[i] == 'Interface ':
                assert_that(arr_value[i] == '%s' % interface, "Значение параметра Interface равно %s" % (arr_value[i]))
            if arr_name[i] == 'Agent type: ':
                assert_that(arr_value[i] == 'nearest-bridge', "Значение параметра Agent type равно не ожидаемому nearest-bridge, а %s" % arr_value[i])       
            if arr_name[i] == 'Tx: ':
                assert_that(arr_value[i] == 'enabled', "Значение параметра Tx равно не ожидаемому enabled, а %s" % arr_value[i])  		
            if arr_name[i] == 'Rx: ':
                assert_that(arr_value[i] == 'enabled', "Значение параметра Rx равно не ожидаемому enabled, а %s" % arr_value[i])  
            if arr_name[i] == 'Enable management address TLV is ':
                assert_that(arr_value[i] == 'transmited', "Значение параметра Management address равно не ожидаемому transmited, а %s" % arr_value[i])      
            if arr_name[i] == 'Enable port description TLV is ':
                assert_that(arr_value[i] == 'transmited', "Значение параметра Port description равно не ожидаемому transmited, а %s" % arr_value[i])   
            if arr_name[i] == 'Enable system capabilities TLV is ':
                assert_that(arr_value[i] == 'transmited', "Значение параметра System capabilities равно не ожидаемому transmited, а %s" % arr_value[i])         
            if arr_name[i] == 'Enable system name TLV is transmited ':
                assert_that(arr_value[i] == 'transmited', "Значение параметра System name равно не ожидаемому transmited, а %s" % arr_value[i])   
            if arr_name[i] == 'Notification tables is ':
                assert_that(arr_value[i] == 'enabled', "Значение параметра Notification tables равно не ожидаемому enabled, а %s" % arr_value[i]) 
            if arr_name[i] == 'Notification device is ':
                assert_that(arr_value[i] == 'enabled', "Значение параметра Notification device равно не ожидаемому enabled, а %s" % arr_value[i])	
   		   		
