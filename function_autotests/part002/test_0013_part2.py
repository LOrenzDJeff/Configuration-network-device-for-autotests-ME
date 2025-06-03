from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show firmware')
@pytest.mark.part2
@pytest.mark.show_firmware
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
		        
def test_show_firmware_part2(DUT): 
# В данном тесте будем проверять вывод команды 'show firmware'   

    allure.attach.file('./network-schemes/part2_show_firmware.png','Что анализируем в тесте:', attachment_type=allure.attachment_type.PNG)    
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')        
# Определим тип маршрутизатора (ME5000 или ME2001 или ME5200)
    conn.execute('show system')
    resp = conn.response
    for RTtype in ['ME5210S', 'ME5100', 'ME5200', 'ME5200S']:
        index = resp.find(RTtype)
        if index != -1:
            SysType = RTtype
    #           print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.
    conn.execute('show firmware')


    conn.execute('show firmware')
    resp = conn.response
    allure.attach(resp, 'Вывод команды show firmware', attachment_type=allure.attachment_type.TEXT)
    #    print('show firmware  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show firmware'
    # C помощью магии модуля textFSM сравниваем вывод команды 'show firmware' c шаблоном в файле parse_show_firmware.txt
    template = open('./templates/parse_show_firmware.txt')
    fsm = textfsm.TextFSM(template)
    #    result = fsm.ParseText(resp)
    #    print(result)
    processed_result = fsm.ParseTextToDicts(resp)
    #    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    #    number_of_elements = len(processed_result)
    conn.send('quit\r')
    conn.close()

    if (SysType == 'ME5100') ^ (SysType == 'ME5200'):
        #        assert_that(number_of_elements==2, "Кол-во элементов в списке processed_result не соответсвует 2, а равно - %d"%number_of_elements)
        # count=0
        # for count in processed_result:
        #     Unit = processed_result[count]['Unit']
        #     Image = processed_result[count]['Image']
        #     Run_status = processed_result[count]['Run_status']
        #     Boot = processed_result[count]['Boot']
        #     Version = processed_result[count]['Version']
        #     Date = processed_result[count]['Date']
        #     count=count+1
        #     assert_that(Unit == '0/ME5200' or Unit == '0/ME5100',"Параметр Unit в строке %s в выводе команды не соответсвуют ожидамым значениям ME5100 или ME5200, а равен - %s"%(count+1,Unit))
        #     assert_that(Image == '0',"Параметр Image в строке %s в выводе команды не соответсвуют ожидаемому значению 0 , а равен - %s"%(count+1,Image))
        #     assert_that((Boot == ' ' and Run_status=='No') or (Boot == '*' and Run_status=='Yes'),"Параметры Boot и Run_status в строке %s в выводе команды не соответсвуют ожидамым значениям '' и No или '*'' и Yes соответсвенно, а равны Boot - %s и Run_status - %s"%(count+1,Boot,Run_status))
        #     assert_that(Version != '' ,"Параметр Version в строке %s в выводе команды не соответсвуют шаблону, а равен - %s"%(count+1,Version))
        #     assert_that(Date != '' ,"Параметр Date в строке %s в выводе команды не соответсвуют шаблону, а равен - %s"%(count+1,Date)) 

        Unit1 = processed_result[0]['Unit']
        Image1 = processed_result[0]['Image']
        Run_status1 = processed_result[0]['Run_status']
        Boot1 = processed_result[0]['Boot']
        Version1 = processed_result[0]['Version']
        Date1 = processed_result[0]['Date']

        Unit2 = processed_result[1]['Unit']
        Image2 = processed_result[1]['Image']
        Run_status2 = processed_result[1]['Run_status']
        Boot2 = processed_result[1]['Boot']
        Version2 = processed_result[1]['Version']
        Date2 = processed_result[1]['Date']

        assert_that((Boot1 != 'CONFIRMING') and (Boot1 != 'FALLBACK*'), "Не выполнена команда firmware confirm")

        # conn.send('quit\r')
        # conn.close()
        assert_that(Unit1 == '0/ME5200' or Unit1 == '0/ME5100',
                    "Параметр Unit1 в выводе команды не соответсвуют ожидамым значениям ME5100 или ME5200, а равен - %s" % Unit1)
        assert_that(Image1 == '0',
                    "Параметр Image1 в выводе команды не соответсвуют ожидаемому значению 0 , а равен - %s" % Image1)
        assert_that((Boot1 == '' and Run_status1 == 'No') or (Boot1 == '*' and Run_status1 == 'Yes'),
                    "Параметры Boot1 и Run_status1 в выводе команды не соответсвуют ожидамым значениям '' и No или '*'' и Yes соответсвенно, а равны Boot1 - %s и Run_status1 - %s" % (
                    Boot1, Run_status1))
        assert_that(Version1 != '',
                    "Параметр Version1 в выводе команды не соответсвуют шаблону, а равен - %s" % Version1)
        assert_that(Date1 != '', "Параметр Date1 в выводе команды не соответсвуют шаблону, а равен - %s" % Date1)

        assert_that(Unit2 == '0/ME5200' or Unit2 == '0/ME5100',
                    "Параметр Unit2 в выводе команды не соответсвуют ожидамым значениям ME5100 или ME5200, а равен - %s" % Unit2)
        assert_that(Image2 == '1',
                    "Параметр Image2 в выводе команды не соответсвуют ожидаемому значению 1, а равен - %s" % Image2)
        assert_that((Boot2 == '' and Run_status2 == 'No') or (Boot2 == '*' and Run_status2 == 'Yes'),
                    "Параметры Boot2 и Run_status2 в выводе команды не соответсвуют ожидамым значениям '' и No или '*' и Yes соответсвенно, а равны Boot2 - %s и Run_status2 - %s" % (
                    Boot2, Run_status2))
        assert_that(Version2 != '',
                    "Параметр Version2 в выводе команды не соответсвуют шаблону, а равен - %s" % Version2)
        assert_that(Date2 != '', "Параметр Date2 в выводе команды не соответсвуют шаблону, а равен - %s" % Date2)


    elif (SysType == 'ME5210S'):
        #        assert_that(number_of_elements==4, "Кол-во элементов в списке processed_result не соответсвует 4, а равно - %d"%number_of_elements)
        # count=0
        # for count in processed_result:
        #     Unit = processed_result[count]['Unit']
        #     Image = processed_result[count]['Image']
        #     Run_status = processed_result[count]['Run_status']
        #     Boot = processed_result[count]['Boot']
        #     Version = processed_result[count]['Version']
        #     Date = processed_result[count]['Date']
        #     count=count+1
        #     assert_that(Unit == '0/ME5210S' or Unit == '0/FMC1' ,"Параметр Unit в строке %s в выводе команды не соответсвуют ожидамым значениям 0/ME5210S или 0/FMC1, а равен - %s"%(count+1,Unit))
        #     assert_that(Image == '0',"Параметр Image в строке %s в выводе команды не соответсвуют ожидаемому значению 0 , а равен - %s"%(count+1,Image))
        #     assert_that((Boot == ' ' and Run_status=='No') or (Boot == '*' and Run_status=='Yes'),"Параметры Boot и Run_status в строке %s в выводе команды не соответсвуют ожидамым значениям '' и No или '*'' и Yes соответсвенно, а равны Boot - %s и Run_status - %s"%(count+1,Boot,Run_status))
        #     assert_that(Version != '' ,"Параметр Version в строке %s в выводе команды не соответсвуют шаблону, а равен - %s"%(count+1,Version))
        #     assert_that(Date != '' ,"Параметр Date в строке %s в выводе команды не соответсвуют шаблону, а равен - %s"%(count+1,Date)) 

        Unit1 = processed_result[0]['Unit']
        Image1 = processed_result[0]['Image']
        Run_status1 = processed_result[0]['Run_status']
        Boot1 = processed_result[0]['Boot']
        Version1 = processed_result[0]['Version']
        Date1 = processed_result[0]['Date']

        Unit2 = processed_result[1]['Unit']
        Image2 = processed_result[1]['Image']
        Run_status2 = processed_result[1]['Run_status']
        Boot2 = processed_result[1]['Boot']
        Version2 = processed_result[1]['Version']
        Date2 = processed_result[1]['Date']

        # Unit3 = processed_result[2]['Unit']
        # Image3 = processed_result[2]['Image']
        # Run_status3 = processed_result[2]['Run_status']
        # Boot3 = processed_result[2]['Boot']
        # Version3 = processed_result[2]['Version']
        # Date3 = processed_result[2]['Date']

        # Unit4 = processed_result[3]['Unit']
        # Image4 = processed_result[3]['Image']
        # Run_status4 = processed_result[3]['Run_status']
        # Boot4 = processed_result[3]['Boot']
        # Version4 = processed_result[3]['Version']
        # Date4 = processed_result[3]['Date']

        # conn.send('quit\r')
        # conn.close()

        assert_that((Boot1 != 'CONFIRMING') and (Boot1 != 'FALLBACK*'), "Не выполнена команда firmware confirm")

        assert_that(Unit1 == '0/ME5210S',
                    "Параметр Unit1 в выводе команды не соответсвуют ожидамым значениям 0/ME5210S, а равен - %s" % Unit1)
        assert_that(Image1 == '0',
                    "Параметр Image1 в выводе команды не соответсвуют ожидаемому значению 0, а равен - %s" % Image1)
        assert_that((Boot1 == '' and Run_status1 == 'No') or (Boot1 == '*' and Run_status1 == 'Yes'),
                    "Параметры Boot1 и Run_status1 в выводе команды не соответсвуют ожидамым значениям '' и No или '*' и Yes соответсвенно, а равны Boot1 - %s и Run_status1 - %s" % (
                    Boot1, Run_status1))
        assert_that(Version1 != '',
                    "Параметр Version1 в выводе команды не соответсвуют шаблону, а равен - %s" % Version1)
        assert_that(Date1 != '', "Параметр Date1 в выводе команды не соответсвуют шаблону, а равен - %s" % Date1)

        assert_that(Unit2 == '0/ME5210S',
                    "Параметр Unit2 в выводе команды не соответсвуют ожидамым значениям 0/ME5210S, а равен - %s" % Unit2)
        assert_that(Image2 == '1',
                    "Параметр Image2 в выводе команды не соответсвуют ожидаемому значению 1, а равен - %s" % Image2)
        assert_that((Boot2 == '' and Run_status2 == 'No') or (Boot2 == '*' and Run_status2 == 'Yes'),
                    "Параметры Boot2 и Run_status2 в выводе команды не соответсвуют ожидамым значениям '' и No или '*' и Yes соответсвенно, а равны Boot2 - %s и Run_status2 - %s" % (
                    Boot2, Run_status2))
        assert_that(Version2 != '',
                    "Параметр Version2 в выводе команды не соответсвуют шаблону, а равен - %s" % Version2)
        assert_that(Date2 != '', "Параметр Date2 в выводе команды не соответсвуют шаблону, а равен - %s" % Date2)
