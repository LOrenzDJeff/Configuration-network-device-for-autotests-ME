from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show interface utilization')
@pytest.mark.part2
@pytest.mark.show_int_utilization
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_interface_utilization(DUT):
#@pytest.mark.parametrize('ip' , [DUT1['host_ip'] , DUT2['host_ip'] , DUT3['host_ip']])
#def test_show_interface_utilization (ip): 
# В данном тесте будем проверять вывод команды 'show interface utilization'      
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')        
# Определим тип маршрутизатора (ME5000 или ME2001 или ME5200)
    conn.execute('show system')
    resp =conn.response
    for RTtype in ['ME5000', 'ME2001', 'ME5200', 'ME5100']:
        index = resp.find(RTtype)
        if index!= -1:
            SysType=RTtype
#           print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.    
    conn.execute('terminal datadump')        
    resp = ''        
    conn.execute('show interface utilization') 
    resp = conn.response 
    resp_output=resp.partition('show interface utilization') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе  
    allure.attach(resp_output[2], 'Вывод команды show interface utilization', attachment_type=allure.attachment_type.TEXT)      
#    print('show interface utilization  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show int utilization'
# C помощью магии модуля textFSM сравниваем вывод команды 'show int utilization' c шаблоном в файле parse_show_int_utilization_pizzabox_me.txt 
    if (SysType == 'ME2001')^(SysType == 'ME5200')^(SysType == 'ME5200'):
        template = open('./templates/parse_show_int_utilization_pizzabox_me.txt')
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
#        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        Top = result[0][0]
        port1 = result[1][1]
        port2 = result[2][2]
        port3 = result[3][3]
        port4 = result[4][4]
        port11 = result[5][5]
        bu1 = result[6][6]
        bu2 = result[7][7]
        conn.send('quit\r')
        conn.close()
        assert (Top != '') and (port1 != '') and (port2 != '') and (port3 != '') and (port4 != '') and (port11 != '') and (bu1 != '') and (bu2 != '')
    if (SysType == 'ME5000'):
        template = open('./templates/parse_show_int_utilization_me5000.txt')
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
#        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        Top = result[0][0]
        port013 = result[1][1]
        port014 = result[2][2]
        port015 = result[3][3]
        port083 = result[4][4]
        port084 = result[5][5]
        bu1 = result[6][6]
        bu2 = result [7][7]
        conn.send('quit\r')
        conn.close()
        assert (Top != '') and (port013 != '') and (port014 != '') and (port015 != '') and (port083 != '') and (port084 !='') and (bu1 != '') and (bu2 != '')    

