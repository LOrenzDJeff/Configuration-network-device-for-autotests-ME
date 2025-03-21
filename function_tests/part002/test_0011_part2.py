from conftest import *
import re

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show interface status')
@pytest.mark.part2
@pytest.mark.show_int_status
#@pytest.mark.parametrize('ip' , [DUT1['host_ip'] , DUT2['host_ip'] , DUT3['host_ip']])
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_interface_status(DUT): 
# В данном тесте будем проверять вывод команды 'show interface status'      
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')        
# Определим тип маршрутизатора (ME5000 или ME2001 или ME5200)
    conn.execute('show system')
    resp =conn.response
    for RTtype in ['ME5000', 'ME2001', 'ME5200']:
        index = resp.find(RTtype)
        if index!= -1:
            SysType=RTtype
#           print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.    
    conn.execute('terminal datadump')        
    resp = ''        
    conn.execute('show interface status') 
    resp = conn.response
    resp_output=resp.partition('show interface status') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе  
    allure.attach(resp_output[2], 'Вывод команды show interface status', attachment_type=allure.attachment_type.TEXT)               
#    print('show interface status  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show int status'
# C помощью магии модуля textFSM сравниваем вывод команды 'show int status' c шаблоном в файле parse_show_int_status.txt 
    template = open('./templates/parse_show_int_status.txt')
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
    Top=processed_result[0]['Top']
    assert_that(Top!='',"Табличный заголовок в выводе команды не соответсвует шаблону")
    assert_that(re.findall(r'\s+bu1\s+--\s+--\s+auto\s+--\s+Up', resp), "Вывод информации о аггрегированном интерфейсе bu1 не соответсвует шаблону")
    assert_that(re.findall(r'\s+bu2\s+--\s+--\s+auto\s+--\s+Up', resp), "Вывод информации о аггрегированном интерфейсе bu2 не соответсвует шаблону")
#    print(processed_result) # Раскомментируй, если хочешь посмотреть результат парсинга

    if (SysType == 'ME2001'):
        loc_index = 0
        located_index1 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/1', loc_index)
        assert_that(located_index1!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/1")
        located_index2 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/2', loc_index)
        assert_that(located_index2!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/2" )
        located_index4 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/4', loc_index)
        assert_that(located_index4!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/4")
        located_index11 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/11', loc_index)
        assert_that(located_index11!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/11")
        
        port1_name=processed_result[located_index1]['port_name']
        port1_type=processed_result[located_index1]['port_type']
        port1_duplex=processed_result[located_index1]['port_duplex']
        port1_speed=processed_result[located_index1]['port_speed']
        port1_neg=processed_result[located_index1]['port_neg']
        port1_flow_ctl=processed_result[located_index1]['port_flow_ctl']
        port1_link_state=processed_result[located_index1]['port_link_state']
        port1_uptime=processed_result[located_index1]['port_uptime']
        
        port2_name=processed_result[located_index2]['port_name']
        port2_type=processed_result[located_index2]['port_type']
        port2_duplex=processed_result[located_index2]['port_duplex']
        port2_speed=processed_result[located_index2]['port_speed']
        port2_neg=processed_result[located_index2]['port_neg']
        port2_flow_ctl=processed_result[located_index2]['port_flow_ctl']
        port2_link_state=processed_result[located_index2]['port_link_state']
        port2_uptime=processed_result[located_index2]['port_uptime']
        
        port4_name=processed_result[located_index4]['port_name']
        port4_type=processed_result[located_index4]['port_type']
        port4_duplex=processed_result[located_index4]['port_duplex']
        port4_speed=processed_result[located_index4]['port_speed']
        port4_neg=processed_result[located_index4]['port_neg']
        port4_flow_ctl=processed_result[located_index4]['port_flow_ctl']
        port4_link_state=processed_result[located_index4]['port_link_state']
        port4_uptime=processed_result[located_index4]['port_uptime']
        
        port11_name=processed_result[located_index11]['port_name']
        port11_type=processed_result[located_index11]['port_type']
        port11_duplex=processed_result[located_index11]['port_duplex']
        port11_speed=processed_result[located_index11]['port_speed']
        port11_neg=processed_result[located_index11]['port_neg']
        port11_flow_ctl=processed_result[located_index11]['port_flow_ctl']
        port11_link_state=processed_result[located_index11]['port_link_state']
        port11_uptime=processed_result[located_index11]['port_uptime']
        
        assert_that(port1_name=='te0/0/1',"Параметр Interface в первой строке таблицы вывода команды не равен ожидаемому te0/0/1, а равен %s "%port1_name)
        assert_that(port1_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port1_name,port1_type))
        assert_that(port1_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port1_name,port1_duplex))
        assert_that(port1_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port1_name,port1_neg))
        assert_that(port1_flow_ctl=='on',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению on, а равен %s "%(port1_name,port1_flow_ctl))
        assert_that(port1_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port1_name,port1_link_state))
        assert_that(port1_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port1_name,port1_uptime))
        assert_that(port1_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port1_name,port1_speed))
        
        assert_that(port2_name=='te0/0/2',"Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому te0/0/2, а равен %s "%port2_name)
        assert_that(port2_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port2_name,port2_type))       
        assert_that(port2_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port2_name,port2_duplex))
        assert_that(port2_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port2_name,port2_neg))
        assert_that(port2_flow_ctl=='on',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению on, а равен %s "%(port2_name,port2_flow_ctl))
        assert_that(port2_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port2_name,port2_link_state))
        assert_that(port2_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port2_name,port2_uptime))
        assert_that(port2_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port2_name,port2_speed))
        
        assert_that(port4_name=='te0/0/4',"Параметр Interface в четвертой строке таблицы вывода команды не равен ожидаемому te0/0/4, а равен %s "%port4_name)
        assert_that(port4_type=='25G-Fiber',"Параметр Type для интерфейса %s не равен ожидаемому значению 25G-Fiber, а равен %s "%(port4_name,port4_type))
        assert_that(port4_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port4_name,port4_duplex))
        assert_that(port4_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port4_name,port4_neg))
        assert_that(port4_flow_ctl=='on',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению on, а равен %s "%(port4_name,port4_flow_ctl))
        assert_that(port4_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port4_name,port4_link_state))
        assert_that(port4_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port4_name,port4_uptime))
        assert_that(port4_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port4_name,port4_speed))
        
        assert_that(port11_name=='te0/0/11',"Параметр Interface в одиннадцатой строке таблицы вывода команды не равен ожидаемому te0/0/11, а равен %s "%port11_name)
        assert_that(port11_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port11_name,port11_type))
        assert_that(port11_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port11_name,port11_duplex))
        assert_that(port11_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port11_name,port11_neg))
        assert_that(port11_flow_ctl=='on',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению on, а равен %s "%(port11_name,port11_flow_ctl))
        assert_that(port11_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port11_name,port11_link_state))
        assert_that(port11_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port11_name,port11_uptime))
        assert_that(port11_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port11_name,port11_speed))    
        
    if (SysType == 'ME5200'):
        loc_index = 0
        located_index1 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/1', loc_index)
        assert_that(located_index1!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/1")
        located_index2 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/2', loc_index)
        assert_that(located_index2!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/2" )
        located_index3 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/3', loc_index)
        assert_that(located_index3!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/3" )
        located_index4 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/4', loc_index)
        assert_that(located_index4!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/4")
        located_index11 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/0/11', loc_index)
        assert_that(located_index11!=999, "В выводе команды show interface status не обнаружен интерфейс te0/0/11")
        
        port1_name=processed_result[located_index1]['port_name']
        port1_type=processed_result[located_index1]['port_type']
        port1_duplex=processed_result[located_index1]['port_duplex']
        port1_speed=processed_result[located_index1]['port_speed']
        port1_neg=processed_result[located_index1]['port_neg']
        port1_flow_ctl=processed_result[located_index1]['port_flow_ctl']
        port1_link_state=processed_result[located_index1]['port_link_state']
        port1_uptime=processed_result[located_index1]['port_uptime']
        
        port2_name=processed_result[located_index2]['port_name']
        port2_type=processed_result[located_index2]['port_type']
        port2_duplex=processed_result[located_index2]['port_duplex']
        port2_speed=processed_result[located_index2]['port_speed']
        port2_neg=processed_result[located_index2]['port_neg']
        port2_flow_ctl=processed_result[located_index2]['port_flow_ctl']
        port2_link_state=processed_result[located_index2]['port_link_state']
        port2_uptime=processed_result[located_index2]['port_uptime']
        
        port3_name=processed_result[located_index3]['port_name']
        port3_type=processed_result[located_index3]['port_type']
        port3_duplex=processed_result[located_index3]['port_duplex']
        port3_speed=processed_result[located_index3]['port_speed']
        port3_neg=processed_result[located_index3]['port_neg']
        port3_flow_ctl=processed_result[located_index3]['port_flow_ctl']
        port3_link_state=processed_result[located_index3]['port_link_state']
        port3_uptime=processed_result[located_index3]['port_uptime']
        
        port4_name=processed_result[located_index4]['port_name']
        port4_type=processed_result[located_index4]['port_type']
        port4_duplex=processed_result[located_index4]['port_duplex']
        port4_speed=processed_result[located_index4]['port_speed']
        port4_neg=processed_result[located_index4]['port_neg']
        port4_flow_ctl=processed_result[located_index4]['port_flow_ctl']
        port4_link_state=processed_result[located_index4]['port_link_state']
        port4_uptime=processed_result[located_index4]['port_uptime']
        
        port11_name=processed_result[located_index11]['port_name']
        port11_type=processed_result[located_index11]['port_type']
        port11_duplex=processed_result[located_index11]['port_duplex']
        port11_speed=processed_result[located_index11]['port_speed']
        port11_neg=processed_result[located_index11]['port_neg']
        port11_flow_ctl=processed_result[located_index11]['port_flow_ctl']
        port11_link_state=processed_result[located_index11]['port_link_state']
        port11_uptime=processed_result[located_index11]['port_uptime']
        
        assert_that(port1_name=='te0/0/1',"Параметр Interface в первой строке таблицы вывода команды не равен ожидаемому te0/0/1, а равен %s "%port1_name)
        assert_that(port1_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port1_name,port1_type))
        assert_that(port1_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port1_name,port1_duplex))
        assert_that(port1_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port1_name,port1_neg))
        assert_that(port1_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port1_name,port1_flow_ctl))
        assert_that(port1_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port1_name,port1_link_state))
        assert_that(port1_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port1_name,port1_uptime))
        assert_that(port1_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port1_name,port1_speed))
        
        assert_that(port2_name=='te0/0/2',"Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому te0/0/2, а равен %s "%port2_name)
        assert_that(port2_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port2_name,port2_type))       
        assert_that(port2_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port2_name,port2_duplex))
        assert_that(port2_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port2_name,port2_neg))
        assert_that(port2_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port2_name,port2_flow_ctl))
        assert_that(port2_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port2_name,port2_link_state))
        assert_that(port2_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port2_name,port2_uptime))
        assert_that(port2_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port2_name,port2_speed))
        
        assert_that(port3_name=='te0/0/3',"Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому te0/0/3, а равен %s "%port3_name)
        assert_that(port3_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port3_name,port3_type))       
        assert_that(port3_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port3_name,port3_duplex))
        assert_that(port3_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port3_name,port3_neg))
        assert_that(port3_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port3_name,port3_flow_ctl))
        assert_that(port3_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port3_name,port3_link_state))
        assert_that(port3_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port3_name,port3_uptime))
        assert_that(port3_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port3_name,port3_speed))
        
        assert_that(port4_name=='te0/0/4',"Параметр Interface в четвертой строке таблицы вывода команды не равен ожидаемому te0/0/4, а равен %s "%port4_name)
        assert_that(port4_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port4_name,port4_type))
        assert_that(port4_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port4_name,port4_duplex))
        assert_that(port4_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port4_name,port4_neg))
        assert_that(port4_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port4_name,port4_flow_ctl))
        assert_that(port4_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port4_name,port4_link_state))
        assert_that(port4_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port4_name,port4_uptime))
        assert_that(port4_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port4_name,port4_speed))
        
        assert_that(port11_name=='te0/0/11',"Параметр Interface в одиннадцатой строке таблицы вывода команды не равен ожидаемому te0/0/11, а равен %s "%port11_name)
        assert_that(port11_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port11_name,port11_type))
        assert_that(port11_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port11_name,port11_duplex))
        assert_that(port11_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port11_name,port11_neg))
        assert_that(port11_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port11_name,port11_flow_ctl))
        assert_that(port11_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port11_name,port11_link_state))
        assert_that(port11_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port11_name,port11_uptime))
        assert_that(port11_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port11_name,port11_speed))    

    if (SysType == 'ME5000'):
        loc_index = 0
        located_index13 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/1/3', loc_index)
        assert_that(located_index13!=999, "В выводе команды show interface status не обнаружен интерфейс te0/1/3")
        located_index14 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/1/4', loc_index)
        assert_that(located_index14!=999, "В выводе команды show interface status не обнаружен интерфейс te0/1/4" )
        located_index15 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/1/5', loc_index)
        assert_that(located_index15!=999, "В выводе команды show interface status не обнаружен интерфейс te0/1/5" )
        located_index83 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/8/3', loc_index)
        assert_that(located_index83!=999, "В выводе команды show interface status не обнаружен интерфейс te0/8/3")
        located_index84 = locate_index_in_ListOfDict(processed_result, 'port_name', 'te0/8/4', loc_index)
        assert_that(located_index84!=999, "В выводе команды show interface status не обнаружен интерфейс te0/8/4")
        
        port13_name=processed_result[located_index13]['port_name']
        port13_type=processed_result[located_index13]['port_type']
        port13_duplex=processed_result[located_index13]['port_duplex']
        port13_speed=processed_result[located_index13]['port_speed']
        port13_neg=processed_result[located_index13]['port_neg']
        port13_flow_ctl=processed_result[located_index13]['port_flow_ctl']
        port13_link_state=processed_result[located_index13]['port_link_state']
        port13_uptime=processed_result[located_index13]['port_uptime']
        
        port14_name=processed_result[located_index14]['port_name']
        port14_type=processed_result[located_index14]['port_type']
        port14_duplex=processed_result[located_index14]['port_duplex']
        port14_speed=processed_result[located_index14]['port_speed']
        port14_neg=processed_result[located_index14]['port_neg']
        port14_flow_ctl=processed_result[located_index14]['port_flow_ctl']
        port14_link_state=processed_result[located_index14]['port_link_state']
        port14_uptime=processed_result[located_index14]['port_uptime']
        
        port15_name=processed_result[located_index15]['port_name']
        port15_type=processed_result[located_index15]['port_type']
        port15_duplex=processed_result[located_index15]['port_duplex']
        port15_speed=processed_result[located_index15]['port_speed']
        port15_neg=processed_result[located_index15]['port_neg']
        port15_flow_ctl=processed_result[located_index15]['port_flow_ctl']
        port15_link_state=processed_result[located_index15]['port_link_state']
        port15_uptime=processed_result[located_index15]['port_uptime']
        
        port83_name=processed_result[located_index83]['port_name']
        port83_type=processed_result[located_index83]['port_type']
        port83_duplex=processed_result[located_index83]['port_duplex']
        port83_speed=processed_result[located_index83]['port_speed']
        port83_neg=processed_result[located_index83]['port_neg']
        port83_flow_ctl=processed_result[located_index83]['port_flow_ctl']
        port83_link_state=processed_result[located_index83]['port_link_state']
        port83_uptime=processed_result[located_index83]['port_uptime']
        
        port84_name=processed_result[located_index84]['port_name']
        port84_type=processed_result[located_index84]['port_type']
        port84_duplex=processed_result[located_index84]['port_duplex']
        port84_speed=processed_result[located_index84]['port_speed']
        port84_neg=processed_result[located_index84]['port_neg']
        port84_flow_ctl=processed_result[located_index84]['port_flow_ctl']
        port84_link_state=processed_result[located_index84]['port_link_state']
        port84_uptime=processed_result[located_index84]['port_uptime']
        
        assert_that(port13_name=='te0/1/3',"Параметр Interface в первой строке таблицы вывода команды не равен ожидаемому te0/1/3, а равен %s "%port13_name)
        assert_that(port13_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port13_name,port13_type))
        assert_that(port13_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port13_name,port13_duplex))
        assert_that(port13_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port13_name,port13_neg))
        assert_that(port13_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port13_name,port13_flow_ctl))
        assert_that(port13_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port13_name,port13_link_state))
        assert_that(port13_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port13_name,port13_uptime))
        assert_that(port13_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port13_name,port13_speed))
        
        assert_that(port14_name=='te0/1/4',"Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому te0/1/4, а равен %s "%port14_name)
        assert_that(port14_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port14_name,port14_type))       
        assert_that(port14_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port14_name,port14_duplex))
        assert_that(port14_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port14_name,port14_neg))
        assert_that(port14_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port14_name,port14_flow_ctl))
        assert_that(port14_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port14_name,port14_link_state))
        assert_that(port14_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port14_name,port14_uptime))
        assert_that(port14_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port14_name,port14_speed))
        
        assert_that(port15_name=='te0/1/5',"Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому te0/1/5, а равен %s "%port15_name)
        assert_that(port15_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port15_name,port15_type))       
        assert_that(port15_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port15_name,port15_duplex))
        assert_that(port15_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port15_name,port15_neg))
        assert_that(port15_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port15_name,port15_flow_ctl))
        assert_that(port15_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port15_name,port15_link_state))
        assert_that(port15_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port15_name,port15_uptime))
        assert_that(port15_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port15_name,port15_speed))
        
        assert_that(port83_name=='te0/8/3',"Параметр Interface в четвертой строке таблицы вывода команды не равен ожидаемому te0/8/3, а равен %s "%port83_name)
        assert_that(port83_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port83_name,port83_type))
        assert_that(port83_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port83_name,port83_duplex))
        assert_that(port83_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port83_name,port83_neg))
        assert_that(port83_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port83_name,port83_flow_ctl))
        assert_that(port83_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port83_name,port83_link_state))
        assert_that(port83_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port83_name,port83_uptime))
        assert_that(port83_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port83_name,port83_speed))
        
        assert_that(port84_name=='te0/8/4',"Параметр Interface в одиннадцатой строке таблицы вывода команды не равен ожидаемому te0/8/4, а равен %s "%port84_name)
        assert_that(port84_type=='10G-Copper',"Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s "%(port84_name,port84_type))
        assert_that(port84_duplex=='Full',"Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s "%(port84_name,port84_duplex))
        assert_that(port84_neg=='auto',"Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s "%(port84_name,port84_neg))
        assert_that(port84_flow_ctl=='rx',"Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s "%(port84_name,port84_flow_ctl))
        assert_that(port84_link_state=='Up',"Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s "%(port84_name,port84_link_state))
        assert_that(port84_uptime!='',"Параметр Up time для интерфейса %s не соответсвует шаблону, и равен %s "%(port84_name,port84_uptime))
        assert_that(port84_speed=='10G',"Параметр Speed для интерфейса %s не равен ожидаемому 10G, а равен %s"%(port84_name,port84_speed))    
