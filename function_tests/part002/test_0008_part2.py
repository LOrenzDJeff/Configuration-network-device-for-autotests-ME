from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show system environment')
@pytest.mark.part2
@pytest.mark.show_system_environment
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param("DUT1"), 
 			 pytest.param("DUT2"), 
 			 pytest.param("DUT3")
			]
			)
def test_show_system_environment_part2 (DUT):
# Подключаемся к маршрутизатору 'ip'
    router = setting_ME(DUT)     
    resp = ''
    conn = Telnet()
    acc = Account(router.login, router.password)
    conn.connect(router.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
# Определим тип маршрутизатора (ME5000 или ME2001 или ME5200)
    conn.execute('show system')
    resp =conn.response
    for RTtype in ['ME5000', 'ME2001', 'ME5200']:
        index = resp.find(RTtype)
        if index!= -1:
            SysType=RTtype

#    print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.
    conn.execute('terminal datadump')        
    resp = ''      
    cmd='show system environment'  
    conn.execute(cmd) 
    resp = conn.response 
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)      
#    print('show system environment  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show system environment '
# C помощью магии модуля textFSM сравниваем вывод команды 'show system environment' c шаблоном в файле parse_show_system_environment.txt 
    if SysType == 'ME2001':
        template = open('./templates/parse_show_system_environment_me2001.txt')
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
#        result = fsm.ParseText(resp)
#        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        Chassis = processed_result[0]['Chassis_number']
        MainModule = processed_result[0]['MainModule']
        CpuTemp_int = processed_result[0]['CpuTemp_int']
        SwitchEngineTemp_int = processed_result[0]['SwitchEngineTemp_int']
        SwitchEngineTemp_ext = processed_result[0]['SwitchEngineTemp_ext']
        PLLTemp_int = processed_result[0]['PLLTemp_int']
        HighTemp = processed_result[0]['HighTemp']
        FanSpeed = processed_result[0]['FanSpeed']
        Fan1 = processed_result[0]['Fan1']
        Fan2 = processed_result[0]['Fan2']
        Fan3 = processed_result[0]['Fan3']
        Fan4 = processed_result[0]['Fan4']
        Fan5 = processed_result[0]['Fan5']
        PSM1Fan = processed_result[0]['PSM1Fan']
        PSM2FanTemp = processed_result[0]['PSM2FanTemp']

        conn.send('quit\r')
        conn.close()
        assert_that(Chassis=='0',"Параметр Hardware environment information for chassis не равен 0, а равен - %s" % Chassis)
        assert_that(MainModule=='ME2001',"Параметр  Main system module не равен ME2001, а равен - %s" % MainModule)
        assert_that(CpuTemp_int!='',"Параметр CpuTemp_int не обнаружен парсингом в выводе команды %s" % cmd)
        assert_that(int(CpuTemp_int)<=50,"Внутренний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С" % CpuTemp_int)
        assert_that(int(SwitchEngineTemp_int)<=60,"Внутренний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 60 градусов С" % SwitchEngineTemp_int)
        assert_that(int(SwitchEngineTemp_ext)<=50,"Внешний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 50 градусов С" % SwitchEngineTemp_ext)
        assert_that(int(PLLTemp_int)<=60,"Внутренний температурный датчик PLL показывает значение - %s, что больше порогового значения 60 градусов С" % PLLTemp_int)
        assert_that(int(HighTemp)<=50,"Температура трансивера - %s, что больше порогового значения 50 градусов С" % HighTemp)
        assert_that(int(FanSpeed)<=60,"Скорость вращения корпусных вентиляторов превысила 60 %% и составила - %s %%" % FanSpeed)
        assert_that(Fan1!='',"Параметр Fan1 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan1)<=14000,"Скорость вращения Fan 1 превысила 14000 RPM и составила - %s"%Fan1) #для данной модели вентиляторов максимальная скорость вращения 17600
        assert_that(Fan2!='',"Параметр Fan2 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan2)<=14000,"Скорость вращения Fan 2 превысила 14000 RPM и составила - %s"%Fan2)
        assert_that(Fan3!='',"Параметр Fan3 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan3)<=14000,"Скорость вращения Fan 3 превысила 14000 RPM и составила - %s"%Fan3)
        assert_that(Fan4!='',"Параметр Fan2 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan4)<=14000,"Скорость вращения Fan 2 превысила 14000 RPM и составила - %s"%Fan4)
        assert_that(Fan5!='',"Параметр Fan3 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan5)<=14000,"Скорость вращения Fan 3 превысила 14000 RPM и составила - %s"%Fan5)
        assert_that(int(PSM2FanTemp)<=50,"Температура источника питания - %s, что больше порогового значения 50 градусов С" % PSM2FanTemp)
        assert_that(PSM1Fan!='',"Параметр Power supply 1 не соответсвует описанному в шаблоне")
#        assert (MainModule != '') and (Chassis != '') and (CpuTemp !='') and (SwitchEngineTemp != '') and (LookupEngineTemp != '') and (BoardTemp != '') and (FanSpeed != '') and (Fan1 != '') and (Fan2 != '') and (Fan3 != '') and (PSM1Fan != '') and (PSM2Fan != '')    
    elif SysType == 'ME5200':
        template = open('./templates/parse_show_system_environment_me5200.txt')   
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)        
#        print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга

        Chassis = processed_result[0]['Chassis_number']
        MainModule = processed_result[0]['MainModule']
        CpuTemp_int = processed_result[0]['CpuTemp_int']
        CpuTemp_ext = processed_result[0]['CpuTemp_ext']
        SwitchEngineTemp_int = processed_result[0]['SwitchEngineTemp_int']
        SwitchEngineTemp_ext = processed_result[0]['SwitchEngineTemp_ext']
        SMSTAT_Temp_int = processed_result[0]['SMSTAT_Temp_int']
        SMSTAT_Temp_ext = processed_result[0]['SMSTAT_Temp_ext']
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
        assert_that(Chassis=='0',"Параметр Hardware environment information for chassis не равен 0, а равен - %s"%Chassis)
        assert_that(MainModule=='ME5200',"Параметр  Main system module не равен ME5200, а равен - %s"%MainModule)
        assert_that(int(CpuTemp_int)<=50,"Внутренний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С"%CpuTemp_int)
        assert_that(int(CpuTemp_ext)<=50,"Внешний температурный датчик CPU  показывает значение - %s, что больше порогового значения 50 градусов С"%CpuTemp_ext)
        assert_that(int(SwitchEngineTemp_int)<=60,"Внутренний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 60 градусов С"%SwitchEngineTemp_int)
        assert_that(int(SwitchEngineTemp_ext)<=50,"Внешний температурный датчик Фабрики коммутации показывает значение - %s, что больше порогового значения 50 градусов С"%SwitchEngineTemp_ext)
        assert_that(int(SMSTAT_Temp_int)<=60,"Внутренний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 60 градусов С"%SMSTAT_Temp_int)
        assert_that(int(SMSTAT_Temp_ext)<=50,"Внешний температурный датчик платы SM-STAT показывает значение - %s, что больше порогового значения 50 градусов С"%SMSTAT_Temp_ext)
        assert_that(int(LookupEngineTemp)<=50,"Внутренний температурный датчик TCAM показывает значение - %s, что больше порогового значения 50 градусов С"%LookupEngineTemp)
        assert_that(int(BoardTemp)<=50,"Температурный датчик Board sensor (inlet) показывает значение - %s, что больше порогового значения 50 градусов С"%BoardTemp)
        assert_that(int(FanSpeed)<=52,"Скорость вращения корпусных вентиляторов превысила 52 %% и составила - %s %%"%FanSpeed)
        assert_that(Fan1!='',"Параметр Fan1 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan1)<=5000,"Скорость вращения Fan 1 превысила 5000 RPM и составила - %s"%Fan1)
        assert_that(Fan2!='',"Параметр Fan2 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan2)<=5000,"Скорость вращения Fan 2 превысила 5000 RPM и составила - %s"%Fan2)
        assert_that(Fan3!='',"Параметр Fan3 не обнаружен парсингом в выводе команды %s"%cmd)
        assert_that(int(Fan3)<=5000,"Скорость вращения Fan 3 превысила 5000 RPM и составила - %s"%Fan3)
        assert_that(PSM1Fan!='',"Параметр Power supply 1 не соответсвует описанному в шаблоне")
        assert_that(PSM2Fan!='',"Параметр Power supply 2 не соответсвует описанному в шаблоне")


    elif SysType == 'ME5000':
        FMC0Check = False
        FMC1Check = False
        template = open('./templates/parse_show_system_environment_me5000.txt')
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)        
#        result = fsm.ParseText(resp)
        #print(processed_result)
        FMC0=processed_result[0]['FMC0']
        FMC0_CpuTemp_int=processed_result[0]['FMC0_CpuTemp_int']
        FMC0_FabricTemp_int=processed_result[0]['FMC0_FabricTemp_int']
        FMC0_FabricTemp_ext=processed_result[0]['FMC0_FabricTemp_ext']


        FMC1=processed_result[0]['FMC1']
        FMC1_CpuTemp_int=processed_result[0]['FMC1_CpuTemp_int']
        FMC1_FabricTemp_int=processed_result[0]['FMC1_FabricTemp_int']
        FMC1_FabricTemp_ext=processed_result[0]['FMC1_FabricTemp_ext']

        Slot1=processed_result[0]['Slot1']
        Slot1_CpuTemp_int=processed_result[0]['Slot1_CpuTemp_int']
        Slot1_Switch_Temp_int=processed_result[0]['Slot1_Switch_Temp_int']
        Slot1_Switch_Temp_ext=processed_result[0]['Slot1_Switch_Temp_ext']
        Slot1_Lookup_Temp_int=processed_result[0]['Slot1_Lookup_Temp_int']
        Slot1_SMSTAT_Temp_int=processed_result[0]['Slot1_SMSTAT_Temp_ext']
        Slot1_SMSTAT_Temp_ext=processed_result[0]['Slot1_SMSTAT_Temp_ext']
        Slot1_Board_Temp=processed_result[0]['Slot1_Board_Temp']

        Slot8=processed_result[0]['Slot8']
        Slot8_CpuTemp_int=processed_result[0]['Slot8_CpuTemp_int']
        Slot8_Switch_Temp_int=processed_result[0]['Slot8_Switch_Temp_int']
        Slot8_Switch_Temp_ext=processed_result[0]['Slot8_Switch_Temp_ext']
        Slot8_Lookup_Temp_int=processed_result[0]['Slot8_Lookup_Temp_int']
        Slot8_Board_Temp=processed_result[0]['Slot8_Board_Temp']

        FanTop=processed_result[0]['FanTop']
        Fan1Top=processed_result[0]['Fan1Top']        
        Fan2Top=processed_result[0]['Fan2Top']        
        Fan3Top=processed_result[0]['Fan3Top']
        Fan4Top=processed_result[0]['Fan4Top']                
        Fan5Top=processed_result[0]['Fan5Top']        
        Fan6Top=processed_result[0]['Fan6Top']        


        FanBottom=processed_result[0]['FanBottom']
        Fan1Bottom=processed_result[0]['Fan1Bottom']        
        Fan2Bottom=processed_result[0]['Fan2Bottom']        
        Fan3Bottom=processed_result[0]['Fan3Bottom']
        Fan4Bottom=processed_result[0]['Fan4Bottom']                
        Fan5Bottom=processed_result[0]['Fan5Bottom']        
        Fan6Bottom=processed_result[0]['Fan6Bottom']        

        conn.send('quit\r')
        conn.close()
        assert_that(FMC0=='FMC32',"Параметр Module in slot FMC0 не равен ожидаемому FMC32, а равен - %s"%FMC0)
        assert_that(int(FMC0_CpuTemp_int)<=55,"Внутренний температурный датчик ЦПУ на FMC0 показывает значение - %s, что больше 50 градусов C"%FMC0_CpuTemp_int)
        assert_that(int(FMC0_FabricTemp_int)<=65,"Внутренний температурный датчик Фабрики коммутации на FMC0 показывает значение - %s, что больше 65 градусов C"%FMC0_FabricTemp_int)
        assert_that(int(FMC0_FabricTemp_ext)<=50,"Внешнний температурный датчик Фабрики коммутации на FMC0 показывает значение - %s, что больше 50 градусов C"%FMC0_FabricTemp_ext)
       # assert_that(int(FMC0_Board_Temp)<=50,"Температурный датчик Board sensor (inlet) на FMC0 показывает значение - %s, что больше порогового значения 50 градусов С"%FMC0_Board_Temp)


        assert_that(FMC1=='FMC32',"Параметр Module in slot FMC1 не равен ожидаемому FMC32, а равен - %s"%FMC1)
        assert_that(int(FMC1_CpuTemp_int)<=50,"Внутренний температурный датчик ЦПУ на FMC1 показывает значение - %s, что больше 50 градусов C"%FMC1_CpuTemp_int)
     #   assert_that(int(FMC1_CpuTemp_ext)<=50,"Внешний температурный датчик ЦПУ на FMC1 показывает значение - %s, что больше 50 градусов C"%FMC1_CpuTemp_ext)
        assert_that(int(FMC1_FabricTemp_int)<=65,"Внутренний температурный датчик Фабрики коммутации на FMC1 показывает значение - %s, что больше 65 градусов C"%FMC1_FabricTemp_int)
        assert_that(int(FMC1_FabricTemp_ext)<=50,"Внешнний температурный датчик Фабрики коммутации на FMC1 показывает значение - %s, что больше 50 градусов C"%FMC1_FabricTemp_ext)
     #   assert_that(int(FMC1_Board_Temp)<=50,"Температурный датчик Board sensor (inlet) на FMC1 показывает значение - %s, что больше порогового значения 50 градусов С"%FMC1_Board_Temp)

        assert_that(Slot1=='LC20XGE',"Параметр Module in slot 1 не равен ожидаемому LC20XGE, а равен - %s"%Slot1)
        assert_that(int(Slot1_CpuTemp_int)<=50,"Внутренний температурный датчик ЦПУ на плате в слоту 1 показывает значение - %s, что больше 50 градусов C"%Slot1_CpuTemp_int)
#        assert_that(int(Slot1_CpuTemp_ext)<=50,"Внешнний температурный датчик ЦПУ на плате в слоту 1 показывает значение - %s, что больше 50 градусов C"%Slot1_CpuTemp_ext)
        assert_that(int(Slot1_Switch_Temp_int)<=65,"Внутренний температурный датчик Фабрики коммутации на плате в слоту 1 показывает значение - %s, что больше 65 градусов C"%Slot1_Switch_Temp_int)
        assert_that(int(Slot1_Switch_Temp_ext)<=50,"Внешнний температурный датчик Фабрики коммутации на плате в слоту 1 показывает значение - %s, что больше 50 градусов C"%Slot1_Switch_Temp_ext)        
        assert_that(int(Slot1_Lookup_Temp_int)<=65,"Внутренний температурный датчик TCAM на плате в слоту 1 показывает значение - %s, что больше 65 градусов C"%Slot1_Lookup_Temp_int)
#        assert_that(int(Slot1_Lookup_Temp_ext)<=50,"Внешнний температурный датчик TCAM на плате в слоту 1 показывает значение - %s, что больше 50 градусов C"%Slot1_Lookup_Temp_ext) 
        assert_that(int(Slot1_SMSTAT_Temp_int)<=65,"Внутренний температурный датчик платы SM-STAT на плате в слоту 1 показывает значение - %s, что больше 65 градусов C"%Slot1_SMSTAT_Temp_int)
        assert_that(int(Slot1_SMSTAT_Temp_ext)<=50,"Внешнний температурный датчик платы SM-STAT на плате в слоту 1 показывает значение - %s, что больше 50 градусов C"%Slot1_SMSTAT_Temp_ext)                   
        assert_that(int(Slot1_Board_Temp)<=50,"Температурный датчик (inlet) на плате  плате в слоту 1 показывает значение - %s, что больше порогового значения 50 градусов С"%Slot1_Board_Temp)        

        assert_that(Slot8=='LC20XGE',"Параметр Module in slot 8 не равен ожидаемому LC20XGE, а равен - %s"%Slot8)
        assert_that(int(Slot8_CpuTemp_int)<=50,"Внутренний температурный датчик ЦПУ на плате в слоту 8 показывает значение - %s, что больше 50 градусов C"%Slot8_CpuTemp_int)
#        assert_that(int(Slot8_CpuTemp_ext)<=50,"Внешнний температурный датчик ЦПУ на плате в слоту 8 показывает значение - %s, что больше 50 градусов C"%Slot8_CpuTemp_ext)
        assert_that(int(Slot8_Switch_Temp_int)<=65,"Внутренний температурный датчик Фабрики коммутации на плате в слоту 8 показывает значение - %s, что больше 65 градусов C"%Slot8_Switch_Temp_int)
        assert_that(int(Slot8_Switch_Temp_ext)<=50,"Внешнний температурный датчик Фабрики коммутации на плате в слоту 8 показывает значение - %s, что больше 50 градусов C"%Slot8_Switch_Temp_ext)        
        assert_that(int(Slot8_Lookup_Temp_int)<=65,"Внутренний температурный датчик TCAM на плате в слоту 8 показывает значение - %s, что больше 65 градусов C"%Slot8_Lookup_Temp_int)
#        assert_that(int(Slot8_Lookup_Temp_ext)<=50,"Внешнний температурный датчик TCAM на плате в слоту 8 показывает значение - %s, что больше 50 градусов C"%Slot8_Lookup_Temp_ext)      
#        assert_that(int(Slot8_SMSTAT_Temp_int)<=65,"Внутренний температурный датчик платы SM-STAT на LC18XGE в слоту 8 показывает значение - %s, что больше 65 градусов C"%Slot8_SMSTAT_Temp_int)
#        assert_that(int(Slot8_SMSTAT_Temp_ext)<=50,"Внешнний температурный датчик платы SM-STAT на LC18XGE в слоту 8 показывает значение - %s, что больше 50 градусов C"%Slot8_SMSTAT_Temp_ext)           
        assert_that(int(Slot8_Board_Temp)<=50,"Температурный датчик (inlet) на плате  LC18XGE в слоту 8 показывает значение - %s, что больше порогового значения 50 градусов С"%Slot8_Board_Temp)                

        assert_that(int(FanTop)<=70,"Скорость вращения верхних корпусных вентиляторов превысила 70 %% и составила - %s %%"%FanTop)
        assert_that(int(Fan1Top)<=5000,"Скорость вращения верхнего Fan 1 превысила 5000 RPM и составила - %s"%Fan1Top)
        assert_that(int(Fan2Top)<=5000,"Скорость вращения верхнего Fan 2 превысила 5000 RPM и составила - %s"%Fan2Top)
        assert_that(int(Fan3Top)<=5000,"Скорость вращения верхнего Fan 3 превысила 5000 RPM и составила - %s"%Fan3Top)
        assert_that(int(Fan4Top)<=5000,"Скорость вращения верхнего Fan 4 превысила 5000 RPM и составила - %s"%Fan4Top)
        assert_that(int(Fan5Top)<=5000,"Скорость вращения верхнего Fan 5 превысила 5000 RPM и составила - %s"%Fan5Top)
        assert_that(int(Fan6Top)<=5000,"Скорость вращения верхнего Fan 6 превысила 5000 RPM и составила - %s"%Fan6Top)

        assert_that(int(FanBottom)<=70,"Скорость вращения нижних корпусных вентиляторов превысила 70 %% и составила - %s %%"%FanBottom)
        assert_that(int(Fan1Bottom)<=5000,"Скорость вращения нижнего Fan 1 превысила 5000 RPM и составила - %s"%Fan1Bottom)
        assert_that(int(Fan2Bottom)<=5000,"Скорость вращения нижнего Fan 2 превысила 5000 RPM и составила - %s"%Fan2Bottom)
        assert_that(int(Fan3Bottom)<=5000,"Скорость вращения нижнего Fan 3 превысила 5000 RPM и составила - %s"%Fan3Bottom)
        assert_that(int(Fan4Bottom)<=5000,"Скорость вращения нижнего Fan 4 превысила 5000 RPM и составила - %s"%Fan4Bottom)
        assert_that(int(Fan5Bottom)<=5000,"Скорость вращения нижнего Fan 5 превысила 5000 RPM и составила - %s"%Fan5Bottom)
        assert_that(int(Fan6Bottom)<=5000,"Скорость вращения нижнего Fan 6 превысила 5000 RPM и составила - %s"%Fan6Bottom)

