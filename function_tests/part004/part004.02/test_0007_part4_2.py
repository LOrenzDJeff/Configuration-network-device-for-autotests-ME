from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.02:Функциональное тестирование IS-IS') 
@allure.title('Проверка вывода команды show route isis ipv6')
@pytest.mark.part4_2
@pytest.mark.show_route_isis_ipv6
@pytest.mark.dependency(depends=["load_config042_dut1","load_config042_dut2","load_config042_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_route_isis_ipv6_part4_2 (DUT): 
# В данном тесте будем проверять вывод команды 'show route isis ipv6', а точнее парсить наличие префикса 2004:0:10:1::4/128, пришедшего со стороны маршрутизатора Juniper LABR01
# А так же общее кол-во ISIS IPV6 маршрутов - 6
    resp = ''
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('show route isis ipv6') 
    resp = conn.response
    resp_output=resp.partition('show route isis ipv6') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды show route isis ipv6', attachment_type=allure.attachment_type.TEXT)    
#    print('show route isis ipv6  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show route isis ipv6'
# C помощью магии модуля textFSM сравниваем вывод команды 'show route isis ipv6' c шаблоном в файле parse_show_route_isis_ipv6.txt 
    template = open('./templates/parse_show_route_isis_ipv6.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()
    line1 = result[0][0]
    line2 = result[0][1]
    route_ipv6 = result[0][2]
    total_count = result[0][3]
    assert_that(total_count == '6', "Общее количество маршрутов не равно ожидаемым 6 и составило %s"%total_count)
    assert_that((line1 != '') and (line2 != ''),"Заголовок в выводе команды не соответсвует шаблону")
    assert_that(route_ipv6 !='',"IPv6 маршрут к префиксу 2004:0:10:1::4/128 не соответсвует шаблону")
