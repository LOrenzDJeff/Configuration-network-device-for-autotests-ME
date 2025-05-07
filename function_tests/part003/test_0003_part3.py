from conftest import *
import re

@allure.feature('03:Функциональное тестирование протокола LLDP')
@allure.story('3.2:Проверка LLDP')
@allure.title('В данном тесте будем  проверять вывод комнады show lldp statistic')
@pytest.mark.part3
@pytest.mark.show_lldp_stat
@pytest.mark.dependency(depends=["load_config003_dut1","load_config003_dut2","load_config003_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_lldp_stat_part3(DUT):
    allure.attach.file('./network-schemes/part3_show_lldp_statistic.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG) 
# В данном тесте будем проверять вывод команды 'show lldp statistic'      
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login , DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    cmd = ('show lld statistic')
    conn.execute('terminal datadump')        
    conn.execute(cmd) 
    resp = conn.response 
    allure.attach(resp, 'Вывод команды show lld statistic', attachment_type=allure.attachment_type.TEXT)   
#    print('show users  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show users'
# C помощью магии модуля textFSM сравниваем вывод команды 'show users' c шаблоном в файле parse_show_users.txt 
    template = open('./templates/parse_show_lldp_statistic.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseTextToDicts(resp)
    assert_that(len(result) > 0, f"Пустой вывод команды {cmd}")
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    line1 = result[0]['line1']
    line2 = result[0]['line2']
    line3 = result[0]['line3']
    line4 = result[0]['line4']
    line5 = result[0]['line5']
    line6 = result[0]['line6']
    Top = result[0]['Top']
    assert_that(line1 != '' and line2 != '' and line3 != '' and line4 != '' and line5 != '' and line6 != '', f'LLDP traffic statistics не соответствует шаблону')
    assert_that(Top != '', f"Заголовок таблицы в выводе команды {cmd} не соответствует шаблону")    
    
    port1 = result[0]['port']
    port2 = result[1]['port']
    port3 = result[2]['port']
    port4 = result[3]['port']
    
    if DUT.host_ip == DUT1.host_ip or DUT.host_ip == DUT2.host_ip:
        assert_that(re.match(DUT.neighor2["interface"][0], port1) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/1') 
        assert_that(re.match(DUT.neighor2["interface"][1], port2) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/2')
        assert_that(re.match(DUT.neighor1["interface"][0], port3) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/3')
        assert_that(re.match(DUT.neighor1["interface"][1], port4) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/4')

    elif DUT.host_ip == DUT3.host_ip:
        assert_that(re.match(DUT.neighor1["interface"][0], port1) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/1') 
        assert_that(re.match(DUT.neighor1["interface"][1], port2) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/2')
        assert_that(re.match(DUT.neighor2["interface"][0], port3) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/3')
        assert_that(re.match(DUT.neighor2["interface"][1], port4) != None, f'В выводе команды {cmd} отсуствует (или не соответствует шаблону) порт te0/0/4')
    
    conn.send('quit\r')
    conn.close()
    
