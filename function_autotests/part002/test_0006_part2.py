from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show system')
@pytest.mark.part2
@pytest.mark.show_system
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_system_part2(DUT):
# Подключаемся к маршрутизатору 'ip'
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    cmd="show system"
    conn.execute(cmd) 
    resp = conn.response
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)  
#    print('show system - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show system'
# C помощью магии модуля textFSM сравниваем вывод команды 'show system' c шаблоном в файле parse_show_system.txt 
    template = open('./templates/parse_show_system.txt')
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
    SysType = processed_result[0]['SysType'] # Сохраняем значение из многомерного списка в переменную SysType (переменная будет не пустой строкой, если вывод команды в строке совпадает с шаблоном из файла)
    SysName = processed_result[0]['SysName']       # Сохраняем значение из многомерного списка в переменную SysName
    SysVersion = processed_result[0]['SysVersion']   # Сохраняем значение из многомерного списка в переменную SysVersion
    SysUptime = processed_result[0]['SysUptime']    # Сохраняем значение из многомерного списка в переменную SysUptime
    SysRestart = processed_result[0]['SysRestartTime']   # Сохраняем значение из многомерного списка в переменную SysRestart
    SysMac = processed_result[0]['SysMac'] # Сохраняем значение из многомерного списка в переменную SysMac
    SysPSM1 = processed_result[0]['SysPSM1'] # Сохраняем значение из многомерного списка в переменную SysPSM1
    SysPSM2 = processed_result[0]['SysPSM2'] # Сохраняем значение из многомерного списка в переменную SysPSM2   
    print ('Router %s has system Uptime: %s end_of_uptime\r'%(DUT.host_ip,SysUptime))
    conn.send('quit\r')
    conn.close()
    assert_that(SysType!='',"В выводе команды параметр SysType не соответсвует шаблону")  
    assert_that(SysName!='',"В выводе команды параметр SysName не соответсвует шаблону") 
    assert_that(SysVersion!='',"В выводе команды параметр SysVersion не соответсвует шаблону") 
    assert_that(SysUptime!='',"В выводе команды параметр SysUptime не соответсвует шаблону") 
    assert_that(SysRestart!='',"В выводе команды параметр SysRestart не соответсвует шаблону")
    assert_that(SysMac!='',"В выводе команды параметр SysMac не соответсвует шаблону") 
    assert_that(SysPSM1!='',"В выводе команды параметр SysPSM1 не соответсвует шаблону") 
    assert_that(SysPSM2!='',"В выводе команды параметр SysPSM2 не соответсвует шаблону")

