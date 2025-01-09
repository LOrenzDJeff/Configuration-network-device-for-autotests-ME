from conftest import *

@allure.feature('01:Подготовка основного стенда-квадрата')
@allure.story('1.2:Проверка связности и управления')
@allure.title('В данном тесте будем  проверять IP связность с P2P соседями маршрутизатора')
@pytest.mark.part1
@pytest.mark.neighbor_connect
@pytest.mark.dependency(depends=["load_config001_dut1","load_config001_dut2","load_config001_dut3"],scope='session')
#@pytest.mark.parametrize('ip , int1 , int2 , int3, login , password', [(DUT1['host_ip'] ,DUT1['int1'] ,DUT1['int2'] , DUT1['int3'], DUT1['login'] , DUT1['password']) , (DUT2['host_ip'] ,DUT2['int1'] , DUT2['int2'] , DUT2['int3'], DUT2['login'] , DUT2['password']), (DUT3['host_ip'] ,DUT3['int1'] , DUT3['int2'] , DUT3['int3'], DUT3['login'] , DUT3['password'])])
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3),
			]
			)

def test_ping_neighbors_part1(DUT):
    neighbor1=locate_ipv4_neighbor(DUT.con,DUT.neighor1['int_name']) # Определяем  адрес соседа по интерфейсу DUT из файла config.json
    neighbor2=locate_ipv4_neighbor(DUT.con,DUT.neighor2['int_name'])
    neighbor3=locate_ipv4_neighbor(DUT.con,DUT.neighor3['int_name'])
    tempale_file = open("./templates/parse_ping_from_me.txt")
    tempale = textfsm.TextFSM(tempale_file)

    # neighbor1=locate_neighbor(conn,'ipv4', int1) # Определяем ipv4 адрес соседа по интерфейсу DUT из файла config.json
    # neighbor2=locate_neighbor(conn,'ipv4', int2)
    # neighbor3=locate_neighbor(conn,'ipv4', int3)

    cmd = ('ping %s count 10'%neighbor1)
    DUT.con.execute(cmd)
    string = DUT.con.response
#    resp_output=str.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе
    allure.attach(string, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
#    print(str)     #Раскомментируй, если хочешь посмотреть результат пинга
#    test_1 = 0
#    for i in range(1, 11):
#        resp_neighbor1 = str.find('%s/10'%str(i))
#        if resp_neighbor1 != -1:
#            test_1 = i
#            break
    gen_output = tempale.ParseTextToDicts(string)

    cmd = ('ping %s count 10'%neighbor2)
    DUT.con.execute(cmd)
    string = DUT.con.response
    allure.attach(string, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
#    print(str)    #Расскомментируй, если хочешь посмотреть результат пинга
    #resp_neighbor2 = str.find('10/10')
    gen_output = tempale.ParseTextToDicts(string)

    cmd = ('ping %s count 10'%neighbor3)
    DUT.con.execute(cmd)
    string = DUT.con.response
    allure.attach(string, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
#    print(str)    #Расскомментируй, если хочешь посмотреть результат пинга
    gen_output = tempale.ParseTextToDicts(string)
#    print(gen_output)
    tempale_file.close()
#    assert (resp_neighbor1 != -1) and (resp_neighbor2 != -1) and (resp_neighbor3 != -1) and (resp_remote_ip != -1) # Значит искомое (10/10)в выводе команд 'ping X.Y.Z.V count 10' присутствует
#    assert_that(resp_neighbor1 != -1,"Не пингуется P2P сосед %s"%neighbor1)
#    assert_that(resp_neighbor2 != -1,"Не пингуется P2P сосед %s"%neighbor2)
#    assert_that(resp_neighbor3 != -1,"Не пингуется P2P сосед %s"%neighbor3)
    assert_that(int(gen_output[0]['send_pkt']) > 8,"Не пингуется P2P сосед %s"%neighbor1 + " % успешности = " + gen_output[0]['send_pkt'] + "0")
    assert_that(int(gen_output[1]['send_pkt']) > 8,"Не пингуется P2P сосед %s"%neighbor2 + " % успешности = " + gen_output[1]['send_pkt'] + "0")
    assert_that(int(gen_output[2]['send_pkt']) > 8,"Не пингуется P2P сосед %s"%neighbor3 + " % успешности = " + gen_output[2]['send_pkt'] + "0")
