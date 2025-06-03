from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show users')
@pytest.mark.part2
@pytest.mark.show_users
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_users (DUT): 
# В данном тесте будем проверять вывод команды 'show users'      
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')        
    conn.execute('show users') 
    resp = conn.response 
    resp_output=resp.partition('show users') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе  
    allure.attach(resp_output[2], 'Вывод команды show users', attachment_type=allure.attachment_type.TEXT)   
#    print('show users  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show users'
# C помощью магии модуля textFSM сравниваем вывод команды 'show users' c шаблоном в файле parse_show_users.txt 
    template = open('./templates/parse_show_users.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    Top = result[0][0]
    user = result[0][1]
    conn.send('quit\r')
    conn.close()
    assert (Top != '') and (user != '')

