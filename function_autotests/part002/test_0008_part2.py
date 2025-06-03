from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show system environment')
@pytest.mark.part2
@pytest.mark.show_system_environment
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_system_environment_part2 (DUT):
# Подключаемся к маршрутизатору 'ip'
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
# Определим тип маршрутизатора (ME5000 или ME2001 или ME5200)
    conn.execute('show system')
    resp =conn.response
    for RTtype in ['ME5000', 'ME2001', 'ME5200','ME5100']:
        index = resp.find(RTtype)
        if index!= -1:
            SysType=RTtype

 #   print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.
    conn.execute('terminal datadump')        
    resp = ''      
    cmd='show system environment'  
    conn.execute(cmd) 
    resp = conn.response 
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)      
#    print('show system environment  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show system environment '
# C помощью магии модуля textFSM сравниваем вывод команды 'show system environment' c шаблоном в файле parse_show_system_environment.txt 
    if SysType == 'ME5100':
        template = open('./templates/parse_show_system_environment_me5100.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        #        result = fsm.ParseText(resp)
        #        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        Chassis = processed_result[0]['Chassis_number']
        MainModule = processed_result[0]['MainModule']
        CpuTemp_int = processed_result[0]['CpuTemp_int']
        CpuTemp_ext = processed_result[0]['CpuTemp_ext']
        SwitchEngineTemp_int = processed_result[0]['SwitchEngineTemp_int']
        SwitchEngineTemp_ext = processed_result[0]['SwitchEngineTemp_ext']
        SMSTAT_Temp_int = processed_result[0]['SMSTAT_Temp_int']
        SMSTAT_Temp_ext = processed_result[0]['SMSTAT_Temp_ext']
        LookupEngineTemp_int = processed_result[0]['LookupEngineTemp_int']
        LookupEngineTemp_ext = processed_result[0]['LookupEngineTemp_ext']
        BoardTemp = processed_result[0]['BoardTemp']
        FanSpeed = processed_result[0]['FanSpeed']
        Fan1 = processed_result[0]['Fan1']
        Fan2 = processed_result[0]['Fan2']
        Fan3 = processed_result[0]['Fan3']
        PSM1Fan = processed_result[0]['PSM1Fan']
        PSM2Fan = processed_result[0]['PSM2Fan']

        conn.send('quit\r')
        conn.close()
        assert_that(Chassis == '0',
                    "Параметр Hardware environment information for chassis не равен 0, а равен - %s" % Chassis)
        assert_that(MainModule == 'ME5100', "Параметр  Main system module не равен ME5100, а равен - %s" % MainModule)
        assert_that(CpuTemp_int != '', "Параметр CpuTemp_int не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(CpuTemp_int) <= 50,
                    "Внутренний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С" % CpuTemp_int)
        assert_that(int(CpuTemp_ext) <= 50,
                    "Внешний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С" % CpuTemp_ext)
        assert_that(int(SwitchEngineTemp_int) <= 60,
                    "Внутренний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 60 градусов С" % SwitchEngineTemp_int)
        assert_that(int(SwitchEngineTemp_ext) <= 50,
                    "Внешний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 50 градусов С" % SwitchEngineTemp_ext)
        #assert_that(int(SMSTAT_Temp_int) <= 60,
        #            "Внутренний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 60 градусов С" % SMSTAT_Temp_int)
        #assert_that(int(SMSTAT_Temp_ext) <= 50,
        #            "Внешний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 50 градусов С" % SMSTAT_Temp_ext)
        assert_that(int(LookupEngineTemp_int) <= 50,
                    "Внутренний температурный датчик TCAM показывает значение - %s, что больше порогового значения 50 градусов С" % LookupEngineTemp_int)
        assert_that(int(LookupEngineTemp_ext) <= 50,
                    "Внешний температурный датчик TCAM показывает значение - %s, что больше порогового значения 50 градусов С" % LookupEngineTemp_ext)
        assert_that(int(BoardTemp) <= 50,
                    "Температурный датчик Board sensor (inlet) показывает значение - %s, что больше порогового значения 50 градусов С" % BoardTemp)
        assert_that(int(FanSpeed) <= 50,
                    "Скорость вращения корпусных вентиляторов превысила 50 %% и составила - %s %%" % FanSpeed)
        assert_that(Fan1 != '', "Параметр Fan1 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan1) <= 5000, "Скорость вращения Fan 1 превысила 5000 RPM и составила - %s" % Fan1)
        assert_that(Fan2 != '', "Параметр Fan2 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan2) <= 5000, "Скорость вращения Fan 2 превысила 5000 RPM и составила - %s" % Fan2)
        assert_that(Fan3 != '', "Параметр Fan3 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan3) <= 5000, "Скорость вращения Fan 3 превысила 5000 RPM и составила - %s" % Fan3)
        assert_that(PSM1Fan != '', "Параметр Power supply 1 не соответствует описанному в шаблоне")
        assert_that(PSM2Fan != '', "Параметр Power supply 2 не соответствует описанному в шаблоне")
    #        assert (MainModule != '') and (Chassis != '') and (CpuTemp !='') and (SwitchEngineTemp != '') and (LookupEngineTemp != '') and (BoardTemp != '') and (FanSpeed != '') and (Fan1 != '') and (Fan2 != '') and (Fan3 != '') and (PSM1Fan != '') and (PSM2Fan != '')
    elif SysType == 'ME5200':
        template = open('./templates/parse_show_system_environment_me5200.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        #        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга

        Chassis = processed_result[0]['Chassis_number']
        MainModule = processed_result[0]['MainModule']
        CpuTemp_int = processed_result[0]['CpuTemp_int']
        CpuTemp_ext = processed_result[0]['CpuTemp_ext']
        SwitchEngineTemp_int = processed_result[0]['SwitchEngineTemp_int']
        SwitchEngineTemp_ext = processed_result[0]['SwitchEngineTemp_ext']
        #        SMSTAT_Temp_int = processed_result[0]['SMSTAT_Temp_int']
        #        SMSTAT_Temp_ext = processed_result[0]['SMSTAT_Temp_ext']
        LookupEngineTemp = processed_result[0]['LookupEngineTemp']
        BoardTemp = processed_result[0]['BoardTemp']
        FanSpeed = processed_result[0]['FanSpeed']
        Fan1 = processed_result[0]['Fan1']
        Fan2 = processed_result[0]['Fan2']
        Fan3 = processed_result[0]['Fan3']
        PSM1Fan = processed_result[0]['PSM1Fan']
        PSM2Fan = processed_result[0]['PSM2Fan']

        conn.send('quit\r')
        conn.close()
        assert_that(Chassis == '0',
                    "Параметр Hardware environment information for chassis не равен 0, а равен - %s" % Chassis)
        assert_that(MainModule == 'ME5200', "Параметр  Main system module не равен ME5200, а равен - %s" % MainModule)
        assert_that(int(CpuTemp_int) <= 50,
                    "Внутренний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С" % CpuTemp_int)
        assert_that(int(CpuTemp_ext) <= 50,
                    "Внешний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С" % CpuTemp_ext)
        assert_that(int(SwitchEngineTemp_int) <= 60,
                    "Внутренний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 60 градусов С" % SwitchEngineTemp_int)
        assert_that(int(SwitchEngineTemp_ext) <= 50,
                    "Внешний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 50 градусов С" % SwitchEngineTemp_ext)
        #        assert_that(int(SMSTAT_Temp_int)<=60,"Внутренний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 60 градусов С"%SMSTAT_Temp_int)
        #        assert_that(int(SMSTAT_Temp_ext)<=50,"Внешний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 50 градусов С"%SMSTAT_Temp_ext)
        assert_that(int(LookupEngineTemp) <= 50,
                    "Внутренний температурный датчик TCAM показывает значение - %s, что больше порогового значения 50 градусов С" % LookupEngineTemp)
        assert_that(int(BoardTemp) <= 50,
                    "Температурный датчик Board sensor (inlet) показывает значение - %s, что больше порогового значения 50 градусов С" % BoardTemp)
        assert_that(int(FanSpeed) <= 52,
                    "Скорость вращения корпусных вентиляторов превысила 52 %% и составила - %s %%" % FanSpeed)
        assert_that(Fan1 != '', "Параметр Fan1 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan1) <= 5000, "Скорость вращения Fan 1 превысила 5000 RPM и составила - %s" % Fan1)
        assert_that(Fan2 != '', "Параметр Fan2 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan2) <= 5000, "Скорость вращения Fan 2 превысила 5000 RPM и составила - %s" % Fan2)
        assert_that(Fan3 != '', "Параметр Fan3 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan3) <= 5000, "Скорость вращения Fan 3 превысила 5000 RPM и составила - %s" % Fan3)
        assert_that(PSM1Fan != '', "Параметр Power supply 1 не соответствует описанному в шаблоне")
        assert_that(PSM2Fan != '', "Параметр Power supply 2 не соответствует описанному в шаблоне")


    elif SysType == 'ME5210S':
        template = open('./templates/parse_show_system_environment_me5210.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        #        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга

        Chassis = processed_result[0]['Chassis_number']
        MainModule = processed_result[0]['MainModule']
        CpuTemp_int = processed_result[0]['CpuTemp_int']
        SwitchEngineTemp_int = processed_result[0]['SwitchEngineTemp_int']
        SwitchEngineTemp_ext = processed_result[0]['SwitchEngineTemp_ext']
        #        SMSTAT_Temp_int = processed_result[0]['SMSTAT_Temp_int']
        #        SMSTAT_Temp_ext = processed_result[0]['SMSTAT_Temp_ext']
        LookupEngineTemp = processed_result[0]['LookupEngineTemp']
        BoardTemp = processed_result[0]['BoardTemp']
        FanSpeed = processed_result[0]['FanSpeed']
        Fan1 = processed_result[0]['Fan1']
        Fan2 = processed_result[0]['Fan2']
        Fan3 = processed_result[0]['Fan3']
        Fan4 = processed_result[0]['Fan4']
        Fan5 = processed_result[0]['Fan5']
        PSM1Fan = processed_result[0]['PSM1Fan']
        PSM2Fan = processed_result[0]['PSM2Fan']

        conn.send('quit\r')
        conn.close()
        assert_that(Chassis == '0',
                    "Параметр Hardware environment information for chassis не равен 0, а равен - %s" % Chassis)
        assert_that(MainModule == 'ME5210S', "Параметр  Main system module не равен ME5210S, а равен - %s" % MainModule)
        assert_that(int(CpuTemp_int) <= 65,
                    "Внутренний температурный датчик CPU  показывает значение - %s, что больше порогового значения 65 градусов С" % CpuTemp_int)
        assert_that(int(SwitchEngineTemp_int) <= 65,
                    "Внутренний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 65 градусов С" % SwitchEngineTemp_int)
        assert_that(int(SwitchEngineTemp_ext) <= 65,
                    "Внешний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 65 градусов С" % SwitchEngineTemp_ext)
        #        assert_that(int(SMSTAT_Temp_int)<=60,"Внутренний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 60 градусов С"%SMSTAT_Temp_int)
        #        assert_that(int(SMSTAT_Temp_ext)<=50,"Внешний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 50 градусов С"%SMSTAT_Temp_ext)
        assert_that(int(LookupEngineTemp) <= 50,
                    "Внутренний температурный датчик TCAM показывает значение - %s, что больше порогового значения 50 градусов С" % LookupEngineTemp)
        assert_that(int(FanSpeed) <= 100,
                    "Скорость вращения корпусных вентиляторов превысила 100 %% и составила - %s %%" % FanSpeed)
        assert_that(Fan1 != '', "Параметр Fan1 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan1) <= 20500, "Скорость вращения Fan 1 превысила 20500 RPM и составила - %s" % Fan1)
        assert_that(Fan2 != '', "Параметр Fan2 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan2) <= 20500, "Скорость вращения Fan 2 превысила 20500 RPM и составила - %s" % Fan2)
        assert_that(Fan3 != '', "Параметр Fan3 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan3) <= 20500, "Скорость вращения Fan 3 превысила 20500 RPM и составила - %s" % Fan3)
        assert_that(Fan4 != '', "Параметр Fan4 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan4) <= 20500, "Скорость вращения Fan 4 превысила 20500 RPM и составила - %s" % Fan4)
        assert_that(Fan5 != '', "Параметр Fan5 не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(Fan5) <= 20500, "Скорость вращения Fan 5 превысила 20500 RPM и составила - %s" % Fan5)
        assert_that(PSM1Fan != '', "Параметр Power supply 1 не соответствует описанному в шаблоне")
        assert_that(PSM2Fan != '', "Параметр Power supply 2 не соответствует описанному в шаблоне")
