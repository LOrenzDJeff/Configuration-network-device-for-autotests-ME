from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show system inventory')
@pytest.mark.part2
@pytest.mark.show_system_inventory
#@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_system_inventory_part2(DUT):
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
    print(resp)
    for RTtype in ['ME5000', 'ME2001', 'ME5200','ME5100']:
        index = resp.find(RTtype)
        if index!= -1:
            SysType=RTtype

#    print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.
    conn.execute('terminal datadump')        
    resp = ''        
    conn.execute('show system inventory') 
    resp = conn.response
    resp_output=resp.partition('show system inventory') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе
    allure.attach(resp_output[2], 'Вывод команды show system inventory', attachment_type=allure.attachment_type.TEXT)      
#    print('show system inventory - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show system inventory'
# C помощью магии модуля textFSM сравниваем вывод команды 'show system inventory' c шаблоном в файле parse_show_system_inventory.txt 
    if SysType == 'ME2001':
        template = open('./templates/parse_show_system_inventory_me2001.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        #print(processed_result)
        MainModule = processed_result[0]['MainModule']
        ChassisSerail = processed_result[0]['ChassisSerial']
        HardVersion = processed_result[0]['HardVersion']
        HardRevision = processed_result[0]['HardRevision']
        MAC = processed_result[0]['MAC']
        RAM = processed_result[0]['RAM']
        StorModel = processed_result[0]['StorageModel']
        PSM1 = processed_result[0]['PSM1']
        PSM1_Serial = processed_result[0]['PSM1_Serial']
        PSM1_HardVer = processed_result[0]['PSM1_HardVer']
        PSM2 = processed_result[0]['PSM2']
        PSM2_Serial = processed_result[0]['PSM2_Serial']
        PSM2_HardVer = processed_result[0]['PSM2_HardVer']
        SM_STAT_board = processed_result[0]['SM_STAT']
        SM_STAT_Serial_Number = processed_result[0]['SM_STAT_Serial_number']
        SM_STAT_Hardware_version = processed_result[0]['SM_STAT_Hardware_version']
        conn.send('quit\r')
        conn.close()
        assert_that (MainModule == 'ME2001',"В выводе команды тип устройства не определился как ME2001, вместо этого он определился как %s"%MainModule)
        assert_that (ChassisSerail == 'ME4F000021',"Серийный номер устройства не равен ожидаемому значению ME4F000021, вместо этого он определился как %s"%ChassisSerail)
        assert_that (HardVersion =='1v0',"Аппаратная версия устройства не равна ожидаемому значению 1v0, вместо этого она определилась как %s"%HardVersion)
        assert_that (HardRevision =='0',"Аппаратная ревизия устройства не равна ожидаемому значению 0, вместо этого она определилась как %s"%HardRevision)
        assert_that (MAC =='e4:5a:d4:de:c8:80',"MAC адрес устройства не равен ожидаемому значению e4:5a:d4:de:c8:80, вместо этого он определился как %s"%MAC)
        assert_that (RAM =='16 GB',"Объем RAM устройства не равен ожидаемому значению 16 GB, вместо этого он определился как %s"%RAM)
        assert_that (StorModel =='Apacer AS2280P4 256GB',"Накопитель данных устройства не равен ожидаемому значению Apacer AS2280P4 256GB, вместо этого он определился как %s"%StorModel)
        assert_that (PSM2 =='ELTEX PM300T-48/12',"БП2 устройства не определился как ELTEX PM300T-48/12, вместо этого он определился как %s"%PSM2)
        assert_that (PSM2_Serial =='PM6F000025',"Серийный номер БП2 устройства не равен ожидаемому значению PM6F000025, вместо этого он определился как %s"%PSM2_Serial)
        assert_that (PSM2_HardVer =='1V0',"Аппаратная версия БП2 устройства не равна ожидаемому значению 1V0, вместо этого она определилась как %s"%PSM2_HardVer)
        assert_that (PSM1 =='not present',"БП1 устройства должен иметь статус present, вместо этого он определился как %s"%PSM1)
        if SM_STAT_board != '':
             assert_that (SM_STAT_board == '10AX048H3F34E2SG ME5200-SM-STAT',"Название модуля не соответствует ожидамому значению 10AX048H3F34E2SG ME5200-SM-STATвместо этого он определился как %s"%SM_STAT_board) 
             assert_that (SM_STAT_Serial_Number == 'ME0A000187',"Серийный номер не соответствует ожидамому значению ME0A000187 вместо этого он определился как %s"%SM_STAT_Serial_Number)
             assert_that (SM_STAT_Hardware_version == '1v3',"Аппаратная версия модуля не соответствует ожидамому значению 1v3 вместо этого она определился как %s"%SM_STAT_Hardware_version)
        

    if SysType == 'ME5200':
        template = open('./templates/parse_show_system_inventory_me5200.txt')   
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        #print(processed_result)
        MainModule = processed_result[0]['MainModule']
        ChassisSerail = processed_result[0]['ChassisSerial']
        HardVersion = processed_result[0]['HardVersion']
        HardRevision = processed_result[0]['HardRevision']
        MAC = processed_result[0]['MAC']
        RAM = processed_result[0]['RAM']
        StorModel = processed_result[0]['StorageModel']
        PSM1 = processed_result[1]['PSM1']
        PSM1_Serial = processed_result[1]['PSM1_Serial']
        PSM1_HardVer = processed_result[1]['PSM1_HardVer']
        PSM2 = processed_result[1]['PSM2']
        PSM2_Serial = processed_result[1]['PSM2_Serial']
        PSM2_HardVer = processed_result[1]['PSM2_HardVer']
        SM_STAT_board = processed_result[1]['SM_STAT']
        SM_STAT_Serial_Number = processed_result[1]['SM_STAT_Serial_number']
        SM_STAT_Hardware_version = processed_result[1]['SM_STAT_Hardware_version']
        conn.send('quit\r')
        conn.close()
        assert_that (MainModule == 'ME5200',"В выводе команды тип устройства не определился как ME5200, вместо этого он определился как %s"%MainModule)
        assert_that (ChassisSerail == 'ME10000031',"Серийный номер устройства не равен ожидаемому значению ME10000031, вместо этого он определился как %s"%ChassisSerail)
        assert_that (HardVersion =='1v3',"Аппаратная версия устройства не равна ожидаемому значению 1v3, вместо этого она определилась как %s"%HardVersion)
        assert_that (HardRevision =='0',"Аппаратная ревизия устройства не равна ожидаемому значению 0, вместо этого она определилась как %s"%HardRevision)
        assert_that (MAC =='e0:d9:e3:ff:48:80',"MAC адрес устройства не равен ожидаемому значению e0:d9:e3:ff:48:80, вместо этого он определился как %s"%MAC)
        assert_that (RAM =='16 GB',"Объем RAM устройства не равен ожидаемому значению 16 GB, вместо этого он определился как %s"%RAM)
        assert_that (StorModel =='8GB SATA Flash Drive',"Накопитель данных устройства не равен ожидаемому значению 8GB SATA Flash Drive, вместо этого он определился как %s"%StorModel)
        assert_that (PSM1 =='PM350-220/12:rev.B',"БП1 устройства не определился как PM350-220/12:rev.B, вместо этого он определился как %s"%PSM1)
        assert_that (PSM1_Serial =='PM26000818',"Серийный номер БП1 устройства не равен ожидаемому значению PM26000818, вместо этого он определился как %s"%PSM1_Serial)
        assert_that (PSM1_HardVer =='2v7',"Аппаратная версия БП1 устройства не равна ожидаемому значению 2v7, вместо этого она определилась как %s"%PSM1_HardVer)
        assert_that (PSM2 =='not present',"БП2 устройства должен иметь статус not present т.к. отсутсвует, вместо этого он определился как %s"%PSM2)
        assert_that (SM_STAT_board == '10AX057K2F40E1HG ME5000-SM-STAT2',"Название модуля не соответствует ожидамому значению 10AX057K2F40E1HG ME5000-SM-STAT2 вместо этого он определился как %s"%SM_STAT_board) 
        assert_that (SM_STAT_Serial_Number == 'ME14000053',"Серийный номер не соответствует ожидамому значению ME14000053 вместо этого он определился как %s"%SM_STAT_Serial_Number)
        assert_that (SM_STAT_Hardware_version == '1v1',"Аппаратная версия модуля не соответствует ожидамому значению 1v1 вместо этого она определился как %s"%SM_STAT_Hardware_version)

    elif SysType == 'ME5000':
        FMC0Check = False
        FMC1Check = False
        template = open('./templates/parse_show_system_inventory_me5000.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
#        print(processed_result)
        ChassisType = processed_result[0]['ChassisType']
        ChassisSerail = processed_result[0]['ChassisSerial']
        HardVersion = processed_result[0]['HardVersion']
        HardRevision = processed_result[0]['HardRev']
        MAC = processed_result[0]['MAC']
        FMC0 = processed_result[0]['SlotFMC0']
        FMC0Serial = processed_result[0]['FMC0_Serial']
        FMC0HardVer = processed_result[0]['FMC0_HardVersion']
        FMC0HardRev = processed_result[0]['FMC0_HardRev']
        FMC1 = processed_result[0]['SlotFMC1']
        FMC1Serial = processed_result[0]['FMC1_Serial']
        FMC1HardVer = processed_result[0]['FMC1_HardVersion']
        FMC1HardRev = processed_result[0]['FMC1_HardRev']
        Slot0 = processed_result[0]['Slot0']
        Slot1 = processed_result[0]['Slot1']
        Slot1Serial = processed_result[0]['Slot1_Serial']
        Slot1HardVer = processed_result[0]['Slot1_HardVersion']
        Slot1HardRev = processed_result[0]['Slot1_HardRev']
        Slot1SMSTATboard = processed_result[0]['Slot1_SM_STAT_board']
        Slot1SMSTATSerialNumber = processed_result[0]['Slot1_Serial_number']
        Slot1SMSTATHardversion = processed_result[0]['Slot1_Hardware_version']
        Slot2 = processed_result[0]['Slot2']
        Slot3 = processed_result[0]['Slot3']
        Slot4 = processed_result[0]['Slot4']
        Slot5 = processed_result[0]['Slot5']
        Slot6 = processed_result[0]['Slot6']
        Slot7 = processed_result[0]['Slot7']
        Slot8 = processed_result[0]['Slot8']
        Slot8Serial = processed_result[0]['Slot8_Serial']
        Slot8HardVer = processed_result[0]['Slot8_HardVersion']
        Slot8HardRev = processed_result[0]['Slot8_HardRev']
        # Slot8SMSTATboard = processed_result[0]['Slot8_SM_STAT_board']
        # Slot8SMSTATSerialNumber = processed_result[0]['Slot8_Serial_number']
        # Slot8SMSTATHardversion = processed_result[0]['Slot8_Hardware_version']
        Slot9 = processed_result[0]['Slot9']
        Slot10 = processed_result[0]['Slot10']
        Slot11 = processed_result[0]['Slot11']
        FanTop = processed_result[0]['FanTop']
        FanBottom = processed_result[0]['FanBottom']
        conn.send('quit\r')
        conn.close()    
        assert_that(FMC0=='FMC32',"FMC0 в выводе команды не равна ожидаемому значению FMC32, а равна - %s "%FMC0)
        assert_that(FMC0Serial == 'ME16000030',"Серийный номер FMC0 в выводе команды не равен ожидаемому значению ME16000030, а равен - %s "%FMC0Serial)
        assert_that(FMC0HardRev == '0',"Аппаратная ревизия FMC0 в выводе команды не равна ожидаемому значению 0, а равна - %s "%FMC0HardRev)
        assert_that(FMC0HardVer == '1v2',"Аппаратная версия FMC0 в выводе команды не равна ожидаемому значению 1v2, а равна - %s "%FMC0HardVer)                

#        assert_that(FMC1=='FMC32',"FMC1 в выводе команды не равна ожидаемому значению FMC32, а равна - %s "%FMC1)
#        assert_that(FMC1Serial == 'ME01000042',"Серийный номер FMC1 в выводе команды не равен ожидаемому значению ME01000042, а равен - %s "%FMC1Serial)
#        assert_that(FMC1HardRev == '0',"Аппаратная ревизия FMC1 в выводе команды не равна ожидаемому значению 0, а равна - %s "%FMC1HardRev)
 #       assert_that(FMC1HardVer == '1v4',"Аппаратная версия FMC1 в выводе команды не равна ожидаемому значению 1v4, а равна - %s "%FMC1HardRev)                

        assert_that(Slot1=='LC20XGE',"Плата в slot 1 в выводе команды не равна ожидаемому значению LC20XGE, а равна - %s "%Slot1)
        assert_that(Slot1Serial == 'ME13000028',"Серийный номер платы в слоту 1 в выводе команды не равен ожидаемому значению ME13000028, а равен - %s "%Slot1Serial)
        assert_that(Slot1HardRev == '0',"Аппаратная ревизия платы в слоту 1 в выводе команды не равна ожидаемому значению 0, а равна - %s "%Slot1HardRev)
        assert_that(Slot1HardVer == '1v2',"Аппаратная версия платы в слоту 1 в выводе команды не равна ожидаемому значению 1v2, а равна - %s "%Slot1HardVer)        
        assert_that(Slot1SMSTATboard == '10AX057K2F40E1HG ME5000-SM-STAT2',"Модуль SM-STAT на плате в slot 1 в выводе команды не равен ожидаемому значению 10AX057K2F40E1HG ME5000-SM-STAT2, а равна - %s "%Slot1SMSTATboard)
        assert_that(Slot1SMSTATSerialNumber == 'ME14000029',"Серийный номер модуля SM-STAT платы в слоту 1 в выводе команды не равен ожидаемому значению ME14000029, а равен - %s "%Slot1SMSTATSerialNumber)
        assert_that(Slot1SMSTATHardversion == '1v1',"Аппаратная версия модуля SM-STAT платы в слоту 1 в выводе команды не равна ожидаемому значению 1v1, а равна - %s "%Slot1SMSTATHardversion)

        assert_that(Slot8=='LC20XGE',"Плата в slot 8 в выводе команды не равна ожидаемому значению LC20XGE, а равна - %s "%Slot8)
        assert_that(Slot8Serial == 'ME13000023',"Серийный номер платы в слоту 8 в выводе команды не равен ожидаемому значению ME13000023, а равен - %s "%Slot8Serial)
        assert_that(Slot8HardRev == '0',"Аппаратная ревизия платы в слоту 8 в выводе команды не равна ожидаемому значению 0, а равна - %s "%Slot8HardRev)
        assert_that(Slot8HardVer == '1v1',"Аппаратная версия платы в слоту 8 в выводе команды не равна ожидаемому значению 1v1, а равна - %s "%Slot8HardRev)        
        # assert_that(Slot8SMSTATboard == '10AX057K2F40E1HG ME5000-SM-STAT2',"Модуль SM-STAT на плате в slot 8 в выводе команды не равен ожидаемому значению 10AX048H3F34E2SG ME5000-SM-STAT, а равна - %s "%Slot8SMSTATboard)
        # assert_that(Slot8SMSTATSerialNumber == 'ME0A000183',"Серийный номер модуля SM-STAT платы в слоту 8 в выводе команды не равен ожидаемому значению ME0A000183, а равен - %s "%Slot8SMSTATSerialNumber)
        # assert_that(Slot8SMSTATHardversion == '1v3',"Аппаратная версия модуля SM-STAT платы в слоту 8 в выводе команды не равна ожидаемому значению 1v3, а равна - %s "%Slot8SMSTATHardversion)

        assert_that(FanTop=='present',"Верхний вентилятор в выводе команды определился не корректно")
        assert_that(FanBottom=='present',"Нижний вентилятор в выводе команды определился не корректно")

#         if (FMC0 == 'FMC16') and (FMC0Serial == 'ME01000036') and (FMC0HardRev == '0') and (FMC0HardVer == '1v4'):
#             FMC0Check = True
#         else :
#             FMC0Check = False
# # Комплексная проверка параметров FMC1

#         if (FMC1 == 'FMC16') and (FMC1Serial == 'ME01000042') and (FMC1HardRev == '0') and (FMC1HardVer == '1v4'):
#             FMC1Check = True
#         else :
#             FMC1Check = False    
        
# # Комплексная проверка параметров в Slot1             

#         if (Slot1 == 'LC18XGE') and (Slot1Serial == 'ME02000037') and (Slot1HardRev == '0') and (Slot1HardVer == '1v3') and (Slot1SMSTATboard == '10AX048H3F34E2SG ME5000-SM-STAT') and (Slot1SMSTATSerialNumber == 'ME0A000183') and (Slot1SMSTATHardversion == '1v3'):
#             Slot1Check = True
#         else : 
#             Slot1Check = False    

# # Комплексная проверка параметров в Slot8             

#         if (Slot8 == 'LC18XGE') and (Slot8Serial == 'ME02000041') and (Slot8HardRev == '1') and (Slot8HardVer == '1v3') and (Slot8SMSTATboard == '10AX048H3F34E2SG ME5000-SM-STAT') and (Slot8SMSTATSerialNumber == 'ME0A000199') and (Slot8SMSTATHardversion == '1v3'):
#             Slot8Check = True
#         else : 
#             Slot8Check = False    

#         assert_that(FMC0Check==True,"Проверка управляющей платы FMC0 не прошла. Ожидаемые параметры платы Type/SerialNum/HardRevision/HardVersion - FMC16/ME01000036/0/1v4. Вместо них тест выдал %s/%s/%s/%s"%(FMC0,FMC0Serial,FMC0HardRev,FMC0HardVer))
#         assert_that(FMC1Check==True,"Проверка управляющей платы FMC1 не прошла. Ожидаемые параметры платы Type/SerialNum/HardRevision/HardVersion - FMC16/ME01000042/0/1v4. Вместо них тест выдал %s/%s/%s/%s"%(FMC1,FMC1Serial,FMC1HardRev,FMC1HardVer))
#         assert_that(Slot1Check==True,"Проверка линейной платы в Slot1 не прошла. Ожидаемые параметры платы Type/SerialNum/HardRevision/HardVersion/SMSTATboard/SMSTATSerialNumber/SMSTATHardversion - LC18XGE/ME02000037/0/1v3/10AX048H3F34E2SG ME5000-SM-STAT/ME0A000183/1v3. Вместо них тест выдал %s/%s/%s/%s/%s/%s/%s"%(Slot1,Slot1Serial,Slot1HardRev,Slot1HardVer,Slot1SMSTATboard,Slot1SMSTATSerialNumber,Slot1SMSTATHardversion))
#         assert_that(Slot8Check==True,"Проверка линейной платы в Slot8 не прошла. Ожидаемые параметры платы Type/SerialNum/HardRevision/HardVersion/SMSTATboard/SMSTATSerialNumber/SMSTATHardversion - LC18XGE/ME02000041/1/1v3/10AX048H3F34E2SG ME5000-SM-STAT/ME0A000199/1v3. Вместо них тест выдал %s/%s/%s/%s/%s/%s/%s"%(Slot8,Slot8Serial,Slot8HardRev,Slot8HardVer,Slot8SMSTATboard,Slot8SMSTATSerialNumber,Slot8SMSTATHardversion))
#         assert_that(Slot0==Slot2==Slot3==Slot4==Slot5==Slot6==Slot7==Slot9==Slot10==Slot11=='not present',"В выводе команды для одного или нескольких слотов 0/2/3/4/5/6/7/9/10/11 шасси отображается значение отличное от ожидаемого 'not present'")


