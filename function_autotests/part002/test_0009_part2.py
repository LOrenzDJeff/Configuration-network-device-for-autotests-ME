from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show version')
@pytest.mark.part2
@pytest.mark.show_version
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_version (DUT):
# Подключаемся к маршрутизатору 'ip'    
    resp = ''   
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')        
    conn.execute('show version') 
    resp = conn.response 
    resp_output=resp.partition('show version') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе  
    allure.attach(resp_output[2], 'Вывод команды show version', attachment_type=allure.attachment_type.TEXT)           
    print('show version  - %s'%resp)  # Не надо комментировать этот принт. Версия ПО из лог-файла используется при отправке телеграмм-сообщений
# C помощью магии модуля textFSM сравниваем вывод команды 'show system environment' c шаблоном в файле parse_show_version.txt    
    template = open('./templates/parse_show_version.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)    # Раскомментируй, если хочешь посмотреть результат парсинга    
    conn.send('quit\r')
    conn.close()
#    print('Router %s has version %s\r end_of_version'%(ip,result[0][0]))
    version=processed_result[0]['Version']
    return(version)
    assert_that (version!='',"Параметр Software Version не соответсвует шаблону")   # Если элемент многомерного массива не пустой значит вывод команды show version совпал с шаблоном из файла ./templates/parse_show_version.txt   

