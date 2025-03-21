from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show privilege')
@pytest.mark.part2
@pytest.mark.show_privilege
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_privilege (DUT): 
# В данном тесте будем проверять вывод команды 'show privilege'      
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')        
    conn.execute('show privilege') 
    resp = conn.response  
    resp_output=resp.partition('show privilege') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе  
    allure.attach(resp_output[2], 'Вывод команды show privilege', attachment_type=allure.attachment_type.TEXT)   
 #   print('show privilege  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show privilege'
# C помощью магии модуля textFSM сравниваем вывод команды 'show firmware' c шаблоном в файле parse_show_privilege.txt 
    template = open('./templates/parse_show_privilege.txt')
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
    conn.send('quit\r')
    conn.close()
#    result = fsm.ParseText(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    number_of_elements = len(processed_result)
    assert_that(number_of_elements==1, "Кол-во элементов в списке processed_result не соответсвует 1, а равно - %d"%number_of_elements)
    lvl = processed_result[0]['lvl']
    assert_that (lvl =='15',"Уровень привилегий пользователя не равен ожидаемому 15, а равен- %s"%lvl)

