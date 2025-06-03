from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.1: Функциональное тестирование show-команд протокола RSVP-TE')
@allure.title('Проверка вывода команды show mpls rsvp tunnels')
@pytest.mark.part14_1
@pytest.mark.show_rsvp_tunnel
@pytest.mark.parametrize('ip, login, password', [(DUT3['host_ip'], DUT3['login'], DUT3['password']),(DUT2['host_ip'], DUT2['login'], DUT2['password']),(DUT1['host_ip'], DUT1['login'], DUT1['password']) ])
def test_show_rsvp_tunnel_part14_1 (ip, login, password):
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    if ip==DUT1['host_ip']:
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_atAR1.png','Вывод команды', attachment_type=allure.attachment_type.PNG) 
    if ip==DUT2['host_ip']:
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_atAR2.png','Вывод команды', attachment_type=allure.attachment_type.PNG) 
    if ip==DUT3['host_ip']:
        allure.attach.file('./network-schemes/part14_1_show_mpls_rsvp_tunnel_atDR1.png','Вывод команды', attachment_type=allure.attachment_type.PNG) 


    conn.set_prompt('#')
    time.sleep(20)
    cmd='show mpls rsvp tunnel'
    conn.execute(cmd)
    resp=conn.response
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'

    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show route' c шаблоном в файле parse_show_route.txt 
    template = open('./templates/parse_show_mpls_rsvp_tunnel.txt') 
    fsm = textfsm.TextFSM(template)

    conn.send('quit\r')
    conn.close()

    processed_result = fsm.ParseTextToDicts(resp) 
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    top=processed_result[0]['top']
    tun_name=processed_result[0]['tun_name']
    tun_src=processed_result[0]['tun_src']
    tun_dst=processed_result[0]['tun_dst']
    tun_status=processed_result[0]['tun_status']
    tun_state=processed_result[0]['tun_state']
    assert_that(top!='',"Табличный заголовок в выводе команды %s не соответствует шаблону"%cmd)
    assert_that(tun_name!='',"Имя ТЕ туннеля %s не соответствует шаблону"%tun_name)
    assert_that(tun_src!='',"Source IP ТЕ туннеля %s не соответствует шаблону"%tun_src)
    assert_that(tun_dst!='',"Destiation IP ТЕ туннеля %s не соответствует шаблону"%tun_dst)
    assert_that(tun_status=='up',"Статус  ТЕ туннеля не равен UP")
    assert_that(tun_state=='up',"Oper state  ТЕ туннеля не равен UP")

