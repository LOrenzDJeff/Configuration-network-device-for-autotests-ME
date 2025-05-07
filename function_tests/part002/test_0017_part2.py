from conftest import *
import re
import textfsm
import time
@pytest.mark.part2
@pytest.mark.show_arp_age_part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.008:Проверка системных Proxy ARP')
@allure.title('В данном тесте будем проверять частоту обновления arp-таблицы')
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_arp_age(DUT):
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    cmd='config'
    conn.execute(cmd)
    cmd='arp aging-time 1'
    conn.execute(cmd)
    cmd='exit'
    conn.execute(cmd)
    cmd='commit'
    conn.execute(cmd)
    time.sleep(5)
    cmd='exit'
    conn.execute(cmd)
    cmd = 'show arp interfaces '+ DUT.neighor1['int_name']
    conn.execute(cmd)
    resp1 = conn.response
    allure.attach(resp1, 'Результат выполнения команды '+cmd, attachment_type=allure.attachment_type.TEXT)
    template1 = open('./templates/parse_show_arp_age.txt')
    fsm1 = textfsm.TextFSM(template1)
    result1 = fsm1.ParseTextToDicts(resp1)
    data = result1[0]['age']
    minutes_start= data[3] + data[4]
    seconds_start = data[6] + data[7]
    time_to_update_start=int(seconds_start) + (int(minutes_start))*60 +1
    minutes = data[3] + data[4]
    seconds = data[6] + data[7]   
    time_to_update = int(seconds) + (int(minutes))*60
    start_time = time.time()
    while time_to_update >= time_to_update_start:
      conn.execute(cmd)
      resp1 = conn.response
      template1 = open('./templates/parse_show_arp_age.txt')
      fsm1 = textfsm.TextFSM(template1)
      result1 = fsm1.ParseTextToDicts(resp1)
      data = result1[0]['age']
      minutes = data[3] + data[4]
      seconds = data[6] + data[7]
      time_to_update = int(seconds) + (int(minutes))*60 - 1
    else:
      run_time = int(time.time()-start_time + time_to_update_start)
      assert_that(run_time <= 30,'ARP-таблица обновляется слишком медленно, вместо ожидаемых 30 секунд - %s'%run_time)
      allure.attach('Время обновления arp-таблицы %d'%run_time + ' сек.','Тест успешно пройден, результат: ', attachment_type=allure.attachment_type.TEXT)
      cmd='config'
      conn.execute(cmd)
      cmd='no arp'
      conn.execute(cmd)
      cmd='commit'
      conn.execute(cmd)
      time.sleep(5)
      cmd='exit'
      conn.execute(cmd)
      conn.close()
