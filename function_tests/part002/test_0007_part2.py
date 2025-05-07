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
    if SysType == 'ME5100':
        template = open('./templates/parse_show_system_inventory_me5100.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        # print(processed_result)
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
        assert_that(MainModule == 'ME5100',
                    "В выводе команды тип устройства не определился как ME5100, вместо этого он определился как %s" % MainModule)
        assert_that(ChassisSerail != '',
                    "Не удалось спарсить информацию о серийном номере")
        assert_that(HardVersion == '3v2',
                    "Аппаратная версия устройства не равна ожидаемому значению 3v2, вместо этого она определилась как %s" % HardVersion)
        assert_that(HardRevision == '0',
                    "Аппаратная ревизия устройства не равна ожидаемому значению 0, вместо этого она определилась как %s" % HardRevision)
        assert_that(MAC != 'e0:d9:e3:df:35:80',
                    "Не удалось спарсить информацию о MAC-адресе")
        assert_that(RAM == '8 GB',
                    "Объем RAM устройства не равен ожидаемому значению 8 GB, вместо этого он определился как %s" % RAM)
        assert_that(StorModel == '8GB SATA Flash Drive',
                    "Накопитель данных устройства не равен ожидаемому значению 8GB SATA Flash Drive, вместо этого он определился как %s" % StorModel)
        #assert_that(PSM2 == 'PM350-220/12:rev.B',
        #            "БП2 устройства не определился как PM350-220/12:rev.B, вместо этого он определился как %s" % PSM2)
        #assert_that(PSM2_Serial != '',
        #            "Не удалось спарсить информацию о серийном номере" % PSM2_Serial)
        #assert_that(PSM2_HardVer == '2v6',
        #            "Аппаратная версия БП2 устройства не равна ожидаемому значению 2v6, вместо этого она определилась как %s" % PSM2_HardVer)
        #assert_that(PSM1 == 'not present',
        #            "БП1 устройства должен иметь статус not present т.к. отсутсвует, вместо этого он определился как %s" % PSM1)
        # assert_that (SM_STAT_board == '10AX048H3F34E2SG ME5200-SM-STAT',"Название модуля не соответствует ожидамому значению 10AX048H3F34E2SG ME5200-SM-STATвместо этого он определился как %s"%SM_STAT_board) 
        # assert_that (SM_STAT_Serial_Number == 'ME0A000187',"Серийный номер не соответствует ожидамому значению ME0A000187 вместо этого он определился как %s"%SM_STAT_Serial_Number)
        # assert_that (SM_STAT_Hardware_version == '1v3',"Аппаратная версия модуля не соответствует ожидамому значению 1v3 вместо этого она определился как %s"%SM_STAT_Hardware_version)

    if SysType == 'ME5200':
        template = open('./templates/parse_show_system_inventory_me5200.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        # print(processed_result)
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
        assert_that(MainModule == 'ME5200',
                    "В выводе команды тип устройства не определился как ME5200, вместо этого он определился как %s" % MainModule)
        assert_that(ChassisSerail != '',
                    "Серийный номер устройства не равен ожидаемому значению ME10000027, вместо этого он определился как %s" % ChassisSerail)
        assert_that(HardVersion != '',
                    "Аппаратная версия устройства не равна ожидаемому значению 1v2, вместо этого она определилась как %s" % HardVersion)
        assert_that(HardRevision != '',
                    "Аппаратная ревизия устройства не равна ожидаемому значению 1, вместо этого она определилась как %s" % HardRevision)
        assert_that(MAC != '',
                    "MAC адрес устройства не равен ожидаемому значению e0:d9:e3:df:6e:80, вместо этого он определился как %s" % MAC)
        assert_that(RAM == '16 GB',
                    "Объем RAM устройства не равен ожидаемому значению 16 GB, вместо этого он определился как %s" % RAM)
        assert_that(StorModel == '8GB SATA Flash Drive',
                    "Накопитель данных устройства не равен ожидаемому значению 8GB SATA Flash Drive, вместо этого он определился как %s" % StorModel)
        #assert_that(PSM1 == 'PM350-220/12:rev.B',
        #            "БП1 устройства не определился как PM350-220/12:rev.B, вместо этого он определился как %s" % PSM1)
        #assert_that(PSM1_Serial == 'PM26000321',
        #            "Серийный номер БП1 устройства не равен ожидаемому значению PM26000321, вместо этого он определился как %s" % PSM1_Serial)
        #assert_that(PSM1_HardVer == '2v6',
        #            "Аппаратная версия БП1 устройства не равна ожидаемому значению 2v6, вместо этого она определилась как %s" % PSM1_HardVer)
        #assert_that(PSM2 == 'not present',
        #            "БП2 устройства должен иметь статус not present т.к. отсутсвует, вместо этого он определился как %s" % PSM2)
        # assert_that (SM_STAT_board == '10AX057K2F40E1HG ME5000-SM-STAT2',"Название модуля не соответствует ожидамому значению 10AX057K2F40E1HG ME5000-SM-STAT2 вместо этого он определился как %s"%SM_STAT_board) 
        # assert_that (SM_STAT_Serial_Number == 'ME14000053',"Серийный номер не соответствует ожидамому значению ME14000053 вместо этого он определился как %s"%SM_STAT_Serial_Number)
        # assert_that (SM_STAT_Hardware_version == '1v1',"Аппаратная версия модуля не соответствует ожидамому значению 1v1 вместо этого она определился как %s"%SM_STAT_Hardware_version)

    elif SysType == 'ME5210S':
        template = open('./templates/parse_show_system_inventory_me5210.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(resp)
        # print(processed_result)
        MainModule = processed_result[0]['MainModule']
        ChassisSerail = processed_result[0]['ChassisSerial']
        HardVersion = processed_result[0]['HardVersion']
        HardRevision = processed_result[0]['HardRevision']
        MAC = processed_result[0]['MAC']
        RAM = processed_result[0]['RAM']
        StorModel = processed_result[0]['StorageModel']
        PSM1 = processed_result[1]['PSM1']
        #PSM1_Serial = processed_result[1]['PSM1_Serial']
        #PSM1_HardVer = processed_result[1]['PSM1_HardVer']
        PSM2 = processed_result[1]['PSM2']
        PSM2_Serial = processed_result[1]['PSM2_Serial']
        PSM2_HardVer = processed_result[1]['PSM2_HardVer']
        SM_STAT_board = processed_result[0]['SM_STAT']
        SM_STAT_Serial_Number = processed_result[0]['SM_STAT_Serial_number']
        SM_STAT_Hardware_version = processed_result[0]['SM_STAT_Hardware_version']
        conn.send('quit\r')
        conn.close()
        assert_that(MainModule == 'ME5210S',
                    "В выводе команды тип устройства не определился как ME5210S, вместо этого он определился как %s" % MainModule)
        assert_that(ChassisSerail == 'ME4C000021',
                    "Серийный номер устройства не равен ожидаемому значению ME4C000021, вместо этого он определился как %s" % ChassisSerail)
        assert_that(HardVersion == '1v1',
                    "Аппаратная версия устройства не равна ожидаемому значению 1v1, вместо этого она определилась как %s" % HardVersion)
        assert_that(HardRevision == '0',
                    "Аппаратная ревизия устройства не равна ожидаемому значению 0, вместо этого она определилась как %s" % HardRevision)
        assert_that(MAC == '68:13:e2:d8:16:80',
                    "MAC адрес устройства не равен ожидаемому значению 68:13:e2:d8:16:80, вместо этого он определился как %s" % MAC)
        assert_that(RAM == '64 GB',
                    "Объем RAM устройства не равен ожидаемому значению 64 GB, вместо этого он определился как %s" % RAM)
        assert_that(StorModel == '256GB',
                    "Накопитель данных устройства не равен ожидаемому значению 256GB, вместо этого он определился как %s" % StorModel)
        assert_that(PSM2 == 'ARTESYN DS800SL-3',
                    "БП1 устройства не определился как ARTESYN DS800SL-3, вместо этого он определился как %s" % PSM2)
        assert_that(PSM2_Serial == 'I081260015APP',
                    "Серийный номер БП1 устройства не равен ожидаемому значению ARTESYN DS800SL-3, вместо этого он определился как %s" % PSM2_Serial)
        assert_that(PSM2_HardVer == 'AP',
                    "Аппаратная версия БП1 устройства не равна ожидаемому значению 2v6, вместо этого она определилась как %s" % PSM2_HardVer)
        assert_that(PSM1 == 'not present',
                    "БП2 устройства должен иметь статус not present т.к. отсутсвует, вместо этого он определился как %s" % PSM1)
