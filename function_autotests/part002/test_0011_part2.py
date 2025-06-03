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

    if DUT.host_ip == DUT1.host_ip:
        port1_name = processed_result[0]['port_name']
        port1_type = processed_result[0]['port_type']
        port1_duplex = processed_result[0]['port_duplex']
        port1_speed = processed_result[0]['port_speed']
        port1_neg = processed_result[0]['port_neg']
        port1_flow_ctl = processed_result[0]['port_flow_ctl']
        port1_link_state = processed_result[0]['port_link_state']
        port1_uptime = processed_result[0]['port_uptime']

        port2_name = processed_result[1]['port_name']
        port2_type = processed_result[1]['port_type']
        port2_duplex = processed_result[1]['port_duplex']
        port2_speed = processed_result[1]['port_speed']
        port2_neg = processed_result[1]['port_neg']
        port2_flow_ctl = processed_result[1]['port_flow_ctl']
        port2_link_state = processed_result[1]['port_link_state']
        port2_uptime = processed_result[1]['port_uptime']

        port3_name = processed_result[2]['port_name']
        port3_type = processed_result[2]['port_type']
        port3_duplex = processed_result[2]['port_duplex']
        port3_speed = processed_result[2]['port_speed']
        port3_neg = processed_result[2]['port_neg']
        port3_flow_ctl = processed_result[2]['port_flow_ctl']
        port3_link_state = processed_result[2]['port_link_state']
        port3_uptime = processed_result[2]['port_uptime']

        port4_name = processed_result[3]['port_name']
        port4_type = processed_result[3]['port_type']
        port4_duplex = processed_result[3]['port_duplex']
        port4_speed = processed_result[3]['port_speed']
        port4_neg = processed_result[3]['port_neg']
        port4_flow_ctl = processed_result[3]['port_flow_ctl']
        port4_link_state = processed_result[3]['port_link_state']
        port4_uptime = processed_result[3]['port_uptime']

        port11_name = processed_result[4]['port_name']
        port11_type = processed_result[4]['port_type']
        port11_duplex = processed_result[4]['port_duplex']
        port11_speed = processed_result[4]['port_speed']
        port11_neg = processed_result[4]['port_neg']
        port11_flow_ctl = processed_result[4]['port_flow_ctl']
        port11_link_state = processed_result[4]['port_link_state']
        port11_uptime = processed_result[4]['port_uptime']

        assert_that(port1_name == DUT1.neighor2['interface'][0],
                    "Параметр Interface в первой строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT1.neighor2['interface'][0],port1_name))
        assert_that(port1_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port1_name, port1_type))
        assert_that(port1_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port1_name, port1_duplex))
        assert_that(port1_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port1_name, port1_neg))
        assert_that(port1_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port1_name, port1_flow_ctl))
        assert_that(port1_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port1_name, port1_link_state))
        assert_that(port1_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port1_name, port1_uptime))

        assert_that(port2_name == DUT1.neighor2['interface'][1],
                    "Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT1.neighor2['interface'][1],port2_name))
        assert_that(port2_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port2_name, port2_type))
        assert_that(port2_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port2_name, port2_duplex))
        assert_that(port2_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port2_name, port2_neg))
        assert_that(port2_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port2_name, port2_flow_ctl))
        assert_that(port2_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port2_name, port2_link_state))
        assert_that(port2_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port2_name, port2_uptime))

        assert_that(port3_name == DUT1.neighor1['interface'][0],
                    "Параметр Interface в третьей строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT1.neighor1['interface'][0],port3_name))
        assert_that(port3_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port3_name, port3_type))
        assert_that(port3_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port3_name, port3_duplex))
        assert_that(port3_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port3_name, port3_neg))
        assert_that(port3_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port3_name, port3_flow_ctl))
        assert_that(port3_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port3_name, port3_link_state))
        assert_that(port3_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port3_name, port3_uptime))

        assert_that(port4_name == DUT1.neighor1['interface'][1],
                    "Параметр Interface в четвертой строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT1.neighor1['interface'][1],port4_name))
        assert_that(port4_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port4_name, port4_type))
        assert_that(port4_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port4_name, port4_duplex))
        assert_that(port4_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port4_name, port4_neg))
        assert_that(port4_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port4_name, port4_flow_ctl))
        assert_that(port4_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port4_name, port4_link_state))
        assert_that(port4_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port4_name, port4_uptime))

        assert_that(port11_name == DUT1.neighor3['interface'],
                    "Параметр Interface в одиннадцатой строке таблицы вывода команды не равен ожидаемому %s, а равен %s "%(DUT1.neighor3['interface'],port11_name))
        assert_that(port11_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port11_name, port11_type))
        assert_that(port11_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port11_name, port11_duplex))
        assert_that(port11_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port11_name, port11_neg))
        assert_that(port11_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port11_name, port11_flow_ctl))
        assert_that(port11_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port11_name, port11_link_state))
        assert_that(port11_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port11_name, port11_uptime))
    elif DUT.host_ip == DUT2.host_ip:
        port1_name = processed_result[0]['port_name']
        port1_type = processed_result[0]['port_type']
        port1_duplex = processed_result[0]['port_duplex']
        port1_speed = processed_result[0]['port_speed']
        port1_neg = processed_result[0]['port_neg']
        port1_flow_ctl = processed_result[0]['port_flow_ctl']
        port1_link_state = processed_result[0]['port_link_state']
        port1_uptime = processed_result[0]['port_uptime']

        port2_name = processed_result[1]['port_name']
        port2_type = processed_result[1]['port_type']
        port2_duplex = processed_result[1]['port_duplex']
        port2_speed = processed_result[1]['port_speed']
        port2_neg = processed_result[1]['port_neg']
        port2_flow_ctl = processed_result[1]['port_flow_ctl']
        port2_link_state = processed_result[1]['port_link_state']
        port2_uptime = processed_result[1]['port_uptime']

        port3_name = processed_result[2]['port_name']
        port3_type = processed_result[2]['port_type']
        port3_duplex = processed_result[2]['port_duplex']
        port3_speed = processed_result[2]['port_speed']
        port3_neg = processed_result[2]['port_neg']
        port3_flow_ctl = processed_result[2]['port_flow_ctl']
        port3_link_state = processed_result[2]['port_link_state']
        port3_uptime = processed_result[2]['port_uptime']

        port4_name = processed_result[3]['port_name']
        port4_type = processed_result[3]['port_type']
        port4_duplex = processed_result[3]['port_duplex']
        port4_speed = processed_result[3]['port_speed']
        port4_neg = processed_result[3]['port_neg']
        port4_flow_ctl = processed_result[3]['port_flow_ctl']
        port4_link_state = processed_result[3]['port_link_state']
        port4_uptime = processed_result[3]['port_uptime']

        port11_name = processed_result[4]['port_name']
        port11_type = processed_result[4]['port_type']
        port11_duplex = processed_result[4]['port_duplex']
        port11_speed = processed_result[4]['port_speed']
        port11_neg = processed_result[4]['port_neg']
        port11_flow_ctl = processed_result[4]['port_flow_ctl']
        port11_link_state = processed_result[4]['port_link_state']
        port11_uptime = processed_result[4]['port_uptime']

        assert_that(port1_name == DUT2.neighor2['interface'][0],
                    "Параметр Interface в первой строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT2.neighor2['interface'][0],port1_name))
        assert_that(port1_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port1_name, port1_type))
        assert_that(port1_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port1_name, port1_duplex))
        assert_that(port1_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port1_name, port1_neg))
        assert_that(port1_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port1_name, port1_flow_ctl))
        assert_that(port1_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port1_name, port1_link_state))
        assert_that(port1_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port1_name, port1_uptime))

        assert_that(port2_name == DUT2.neighor2['interface'][1],
                    "Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT2.neighor2['interface'][1],port2_name))
        assert_that(port2_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port2_name, port2_type))
        assert_that(port2_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port2_name, port2_duplex))
        assert_that(port2_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port2_name, port2_neg))
        assert_that(port2_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port2_name, port2_flow_ctl))
        assert_that(port2_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port2_name, port2_link_state))
        assert_that(port2_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port2_name, port2_uptime))

        assert_that(port3_name == DUT2.neighor1['interface'][0],
                    "Параметр Interface в третьей строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT2.neighor1['interface'][0],port3_name))
        assert_that(port3_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port3_name, port3_type))
        assert_that(port3_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port3_name, port3_duplex))
        assert_that(port3_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port3_name, port3_neg))
        assert_that(port3_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port3_name, port3_flow_ctl))
        assert_that(port3_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port3_name, port3_link_state))
        assert_that(port3_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port3_name, port3_uptime))

        assert_that(port4_name == DUT2.neighor1['interface'][1],
                    "Параметр Interface в четвертой строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT2.neighor1['interface'][1],port4_name))
        assert_that(port4_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port4_name, port4_type))
        assert_that(port4_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port4_name, port4_duplex))
        assert_that(port4_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port4_name, port4_neg))
        assert_that(port4_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port4_name, port4_flow_ctl))
        assert_that(port4_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port4_name, port4_link_state))
        assert_that(port4_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port4_name, port4_uptime))

        assert_that(port11_name == DUT2.neighor3['interface'],
                    "Параметр Interface в одиннадцатой строке таблицы вывода команды не равен ожидаемому %s, а равен %s "%(DUT2.neighor3['interface'],port11_name))
        assert_that(port11_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port11_name, port11_type))
        assert_that(port11_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port11_name, port11_duplex))
        assert_that(port11_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port11_name, port11_neg))
        assert_that(port11_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port11_name, port11_flow_ctl))
        assert_that(port11_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port11_name, port11_link_state))
        assert_that(port11_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port11_name, port11_uptime))
        
    elif DUT.host_ip == DUT3.host_ip:
        port1_name = processed_result[0]['port_name']
        port1_type = processed_result[0]['port_type']
        port1_duplex = processed_result[0]['port_duplex']
        port1_speed = processed_result[0]['port_speed']
        port1_neg = processed_result[0]['port_neg']
        port1_flow_ctl = processed_result[0]['port_flow_ctl']
        port1_link_state = processed_result[0]['port_link_state']
        port1_uptime = processed_result[0]['port_uptime']

        port2_name = processed_result[1]['port_name']
        port2_type = processed_result[1]['port_type']
        port2_duplex = processed_result[1]['port_duplex']
        port2_speed = processed_result[1]['port_speed']
        port2_neg = processed_result[1]['port_neg']
        port2_flow_ctl = processed_result[1]['port_flow_ctl']
        port2_link_state = processed_result[1]['port_link_state']
        port2_uptime = processed_result[1]['port_uptime']

        port3_name = processed_result[2]['port_name']
        port3_type = processed_result[2]['port_type']
        port3_duplex = processed_result[2]['port_duplex']
        port3_speed = processed_result[2]['port_speed']
        port3_neg = processed_result[2]['port_neg']
        port3_flow_ctl = processed_result[2]['port_flow_ctl']
        port3_link_state = processed_result[2]['port_link_state']
        port3_uptime = processed_result[2]['port_uptime']

        port4_name = processed_result[3]['port_name']
        port4_type = processed_result[3]['port_type']
        port4_duplex = processed_result[3]['port_duplex']
        port4_speed = processed_result[3]['port_speed']
        port4_neg = processed_result[3]['port_neg']
        port4_flow_ctl = processed_result[3]['port_flow_ctl']
        port4_link_state = processed_result[3]['port_link_state']
        port4_uptime = processed_result[3]['port_uptime']

        port11_name = processed_result[4]['port_name']
        port11_type = processed_result[4]['port_type']
        port11_duplex = processed_result[4]['port_duplex']
        port11_speed = processed_result[4]['port_speed']
        port11_neg = processed_result[4]['port_neg']
        port11_flow_ctl = processed_result[4]['port_flow_ctl']
        port11_link_state = processed_result[4]['port_link_state']
        port11_uptime = processed_result[4]['port_uptime']

        assert_that(port1_name == DUT3.neighor1['interface'][0],
                    "Параметр Interface в первой строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT3.neighor1['interface'][0],port1_name))
        assert_that(port1_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port1_name, port1_type))
        assert_that(port1_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port1_name, port1_duplex))
        assert_that(port1_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port1_name, port1_neg))
        assert_that(port1_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port1_name, port1_flow_ctl))
        assert_that(port1_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port1_name, port1_link_state))
        assert_that(port1_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port1_name, port1_uptime))

        assert_that(port2_name == DUT3.neighor1['interface'][1],
                    "Параметр Interface в второй строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT3.neighor1['interface'][1],port2_name))
        assert_that(port2_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port2_name, port2_type))
        assert_that(port2_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port2_name, port2_duplex))
        assert_that(port2_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port2_name, port2_neg))
        assert_that(port2_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port2_name, port2_flow_ctl))
        assert_that(port2_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port2_name, port2_link_state))
        assert_that(port2_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port2_name, port2_uptime))

        assert_that(port3_name == DUT3.neighor2['interface'][0],
                    "Параметр Interface в третьей строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT3.neighor2['interface'][0],port3_name))
        assert_that(port3_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port3_name, port3_type))
        assert_that(port3_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port3_name, port3_duplex))
        assert_that(port3_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port3_name, port3_neg))
        assert_that(port3_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port3_name, port3_flow_ctl))
        assert_that(port3_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port3_name, port3_link_state))
        assert_that(port3_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port3_name, port3_uptime))

        assert_that(port4_name == DUT3.neighor2['interface'][1],
                    "Параметр Interface в четвертой строке таблицы вывода команды не равен ожидаемому %s, а равен %s " %(DUT3.neighor2['interface'][1],port4_name))
        assert_that(port4_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port4_name, port4_type))
        assert_that(port4_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port4_name, port4_duplex))
        assert_that(port4_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port4_name, port4_neg))
        assert_that(port4_flow_ctl == 'rx',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port4_name, port4_flow_ctl))
        assert_that(port4_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port4_name, port4_link_state))
        assert_that(port4_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port4_name, port4_uptime))
        assert_that(port11_name == DUT3.neighor3['interface'],
                    "Параметр Interface в одиннадцатой строке таблицы вывода команды не равен ожидаемому %s, а равен %s "%(DUT3.neighor3['interface'],port11_name))
        assert_that(port11_type != '',
                    "Параметр Type для интерфейса %s не равен ожидаемому значению 10G-Copper, а равен %s " % (
                        port11_name, port11_type))
        assert_that(port11_duplex == 'Full',
                    "Параметр Duplex для интерфейса %s не равен ожидаемому значению Full, а равен %s " % (
                        port11_name, port11_duplex))
        assert_that(port11_neg == 'auto',
                    "Параметр Neg для интерфейса %s не равен ожидаемому значению auto, а равен %s " % (
                        port11_name, port11_neg))
        assert_that(port11_flow_ctl != '',
                    "Параметр Flow ctrl для интерфейса %s не равен ожидаемому значению rx, а равен %s " % (
                        port11_name, port11_flow_ctl))
        assert_that(port11_link_state == 'Up',
                    "Параметр Link State для интерфейса %s не равен ожидаемому значению Up, а равен %s " % (
                        port11_name, port11_link_state))
        assert_that(port11_uptime != '', "Параметр Up time для интерфейса %s не соответствует шаблону, и равен %s " % (
            port11_name, port11_uptime))