from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.2:Функциональное тестирование форвардинга в BGP L3VPN через RSVP LSP')
@allure.title('Проверка форвардинга BGP L3VPN через RSVP LSP')
@pytest.mark.part14_2
@pytest.mark.ping_over_L3VPN_VRF40_RSVP
@pytest.mark.dependency(depends=["load_config142_dut1","load_config142_dut2","load_config142_dut3","load_config142_dut4"],scope='session')
@pytest.mark.parametrize('ip , hostname , login, password', [(DUT4['host_ip'], DUT4['hostname'], DUT4['login'], DUT4['password'])])
def test_ping_over_L3VPN_VRF40_part14_2 (ip, hostname, login, password): 
# В данном тесте будем проверять пинг между CE устройствами подключенными к L3VPN  VRF40
    allure.attach.file('./network-schemes/part14_2_ping_over_L3VPN_VRF40.png','Схема теста:', attachment_type=allure.attachment_type.PNG)      
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('ping vrf vrf42 192.168.168.43 source ip 192.168.168.42') 
    resp = conn.response    
    resp_output=resp.partition('ping vrf vrf42 192.168.168.43 source ip 192.168.168.42') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды ping vrf vrf42 192.168.168.43 source ip 192.168.168.42', attachment_type=allure.attachment_type.TEXT)
#    print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/0/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    result1_loss = processed_result[0]['loss']
    assert_that(int(result1_loss)==0,"Обнаружены потери пакетов между CE2 и CE3 в размере %s"%result1_loss)

    conn.execute('ping vrf vrf42 192.168.168.41 source ip 192.168.168.42') 
    resp = conn.response    
    resp_output=resp.partition('ping vrf vrf42 192.168.168.41 source ip 192.168.168.42') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды ping vrf vrf42 192.168.168.41 source ip 192.168.168.42', attachment_type=allure.attachment_type.TEXT)
#   print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/0/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)    
#   print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    result2_loss = processed_result[0]['loss']
    assert_that(int(result2_loss)==0,"Обнаружены потери пакетов между CE2 и CE1 в размере %s"%result2_loss)

    conn.execute('ping vrf vrf41 192.168.168.42 source ip 192.168.168.41') 
    resp = conn.response    
    resp_output=resp.partition('ping vrf vrf41 192.168.168.42 source ip 192.168.168.41') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды ping vrf vrf41 192.168.168.42 source ip 192.168.168.41', attachment_type=allure.attachment_type.TEXT)
#   print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/0/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#   print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    result3_loss = processed_result[0]['loss']
    assert_that(int(result3_loss)==0,"Обнаружены потери пакетов между CE1 и CE2 в размере %s"%result3_loss)

    conn.execute('ping vrf vrf41 192.168.168.43 source ip 192.168.168.41') 
    resp = conn.response    
    resp_output=resp.partition('ping vrf vrf41 192.168.168.43 source ip 192.168.168.41') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды ping vrf vrf41 192.168.168.43 source ip 192.168.168.41', attachment_type=allure.attachment_type.TEXT)
#   print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/0/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#   print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    result4_loss = processed_result[0]['loss']
    assert_that(int(result4_loss)==0,"Обнаружены потери пакетов между CE1 и CE3 в размере %s"%result4_loss)            


    conn.execute('ping vrf vrf43 192.168.168.41 source ip 192.168.168.43') 
    resp = conn.response    
    resp_output=resp.partition('ping vrf vrf43 192.168.168.41 source ip 192.168.168.43') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды ping vrf vrf43 192.168.168.41 source ip 192.168.168.43', attachment_type=allure.attachment_type.TEXT)
#   print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/0/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#   print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    result5_loss = processed_result[0]['loss']
    assert_that(int(result5_loss)==0,"Обнаружены потери пакетов между CE3 и CE1 в размере %s"%result5_loss)

    conn.execute('ping vrf vrf43 192.168.168.42 source ip 192.168.168.43') 
    resp = conn.response    
    resp_output=resp.partition('ping vrf vrf43 192.168.168.42 source ip 192.168.168.43') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды ping vrf vrf43 192.168.168.42 source ip 192.168.168.43', attachment_type=allure.attachment_type.TEXT)
#   print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/0/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#   print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    result6_loss = processed_result[0]['loss']
    conn.close()
    assert_that(int(result6_loss)==0,"Обнаружены потери пакетов между CE3 и CE2 в размере %s"%result6_loss)

