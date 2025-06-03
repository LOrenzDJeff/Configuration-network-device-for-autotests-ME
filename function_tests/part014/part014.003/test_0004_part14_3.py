from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.3:Функциональное тестирование bandwidth reservation протокола RSVP-TE')
@allure.title('Проверка построения RSVP LSP туннеля to_vMX-1 с учетом ограничения bandwidth reservation')
@pytest.mark.part14_3
@pytest.mark.show_mpls_rsvp_te_int
@pytest.mark.dependency(depends=["load_config143_dut1","load_config143_dut2","load_config143_dut3","load_config143_dut4"],scope='session')
@pytest.mark.parametrize('ip, login, password, int_name', [(DUT3['host_ip'], DUT3['login'], DUT3['password'], 'bu1'),(DUT2['host_ip'], DUT2['login'], DUT2['password'], 'te0/0/11.351'),(DUT1['host_ip'], DUT1['login'], DUT1['password'], 'bu2')])
def test_show_mpls_rsvp_te_int_part14_3 (ip, login, password, int_name): 
    allure.attach.file('./network-schemes/part14_3_show_mpls_rsvp_te_link-admin_band-alloc.png','Схема Теста', attachment_type=allure.attachment_type.PNG) 
    if ip == DUT3['host_ip']:
        allure.attach.file('./network-schemes/part14_3_show_mpls_rsvp_interfaces_cmd_atDR1.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)
    elif ip == DUT2['host_ip']: 
        allure.attach.file('./network-schemes/part14_3_show_mpls_rsvp_interfaces_cmd_atAR2.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)
    elif ip == DUT1['host_ip']: 
        allure.attach.file('./network-schemes/part14_3_show_mpls_rsvp_interfaces_cmd_atAR1.png','Что анализируется в выводе команды', attachment_type=allure.attachment_type.PNG)

    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    cmd=('show mpls rsvp interfaces')
    conn.execute(cmd)
    resp=conn.response    
#    print(resp) # Раскомментируй, если хочешь посмотреть вывод команды 'show mpls rsvp tunnels'
#    resp_output=resp.partition(cmd) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
#    allure.attach(resp_output[2], 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    # C помощью магии модуля textFSM сравниваем вывод команды 'show mpls rsvp tunnel-lsp' c шаблоном в файле parse_show_mpls_rsvp_tunnel-lsp.txt 
    template = open('./templates/parse_show_mpls_rsvp_interfaces.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()
    int1_name=processed_result[0]['int_name']
    int1_max_resv_bw=processed_result[0]['int_max_resv_bw']
    int1_alloc_bw=processed_result[0]['int_alloc_bw']

    int2_name=processed_result[1]['int_name']
    int2_max_resv_bw=processed_result[1]['int_max_resv_bw']
    int2_alloc_bw=processed_result[1]['int_alloc_bw']

    int3_name=processed_result[2]['int_name']
    int3_max_resv_bw=processed_result[2]['int_max_resv_bw']
    int3_alloc_bw=processed_result[2]['int_alloc_bw']

    if ip == DUT3['host_ip']:
        assert_that(int1_name=='te0/0/5.350',"В первой сторке вывода команды имя интерфейса не соответствует ожидаемому te0/0/5.350, а равно %s"%int1_name)
        assert_that(int1_max_resv_bw=='100.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 100 Mbps в выводе команды, а соответствует - %s"%(int1_name,int1_max_resv_bw))
        assert_that(int1_alloc_bw=='100.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 100 Mbps в выводе команды, а соответствует - %s"%(int1_name,int1_alloc_bw))

        assert_that(int2_name=='bu1',"Во второй сторке вывода команды имя интерфейса не соответствует ожидаемому bu1, а равно %s"%int2_name)
        assert_that(int2_max_resv_bw=='3000.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 3Gbps в выводе команды, а соответствует - %s"%(int2_name,int2_max_resv_bw))
        assert_that(int2_alloc_bw=='2000.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 2Gbps в выводе команды, а соответствует - %s"%(int2_name,int2_alloc_bw))

        assert_that(int3_name=='bu2',"Во второй сторке вывода команды имя интерфейса не соответствует ожидаемому bu1, а равно %s"%int3_name)
        assert_that(int3_max_resv_bw=='100.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 10 Mbps в выводе команды, а соответствует - %s"%(int3_name,int3_max_resv_bw))
        assert_that(int3_alloc_bw=='100.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 100 Mbps в выводе команды, а соответствует - %s"%(int3_name,int3_alloc_bw))

    elif ip == DUT2['host_ip']:
        assert_that(int1_name=='te0/0/11.351',"Имя интерфейса в выводе команды не соответствует ожидаемому te0/0/11.351, а равно %s"%int1_name)
        assert_that(int1_max_resv_bw=='3000.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 3Gbps в выводе команды, а соответствует - %s"%(int1_name,int1_max_resv_bw))
        assert_that(int1_alloc_bw=='0.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 0Gbps в выводе команды, а соответствует - %s"%(int1_name,int1_alloc_bw))

        assert_that(int2_name=='bu1',"Имя интерфейса в выводе команды не соответствует ожидаемому bu1, а равно %s"%int2_name)
        assert_that(int2_max_resv_bw=='100.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 100 Mbps в выводе команды, а соответствует - %s"%(int2_name,int2_max_resv_bw))
        assert_that(int2_alloc_bw=='100.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 100Mbps в выводе команды, а соответствует - %s"%(int2_name,int2_alloc_bw))

        assert_that(int3_name=='bu2',"Имя интерфейса в выводе команды не соответствует ожидаемому bu2, а равно %s"%int3_name)
        assert_that(int3_max_resv_bw=='100.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 100 Mbps в выводе команды, а соответствует - %s"%(int3_name,int3_max_resv_bw))
        assert_that(int3_alloc_bw=='100.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 100 Mbps в выводе команды, а соответствует - %s"%(int3_name,int3_alloc_bw))                

    elif ip == DUT1['host_ip']:
        assert_that(int1_name=='te0/0/11.352',"Имя интерфейса в выводе команды не соответствует ожидаемому te0/0/11.352, а равно %s"%int1_name)
        assert_that(int1_max_resv_bw=='100.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 100Mbps в выводе команды, а соответствует - %s"%(int1_name,int1_max_resv_bw))
        assert_that(int1_alloc_bw=='100.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 100Mbps в выводе команды, а соответствует - %s"%(int1_name,int1_alloc_bw))

        assert_that(int2_name=='bu1',"Имя интерфейса в выводе команды не соответствует ожидаемому bu1, а равно %s"%int2_name)
        assert_that(int2_max_resv_bw=='3000.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 3Gbps в выводе команды, а соответствует - %s"%(int2_name,int2_max_resv_bw))
        assert_that(int2_alloc_bw=='2000.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 2Gbps в выводе команды, а соответствует - %s"%(int2_name,int2_alloc_bw))

        assert_that(int3_name=='bu2',"Имя интерфейса в выводе команды не соответствует ожидаемому bu2, а равно %s"%int3_name)
        assert_that(int3_max_resv_bw=='3000.00',"Максимальная полоса пропускания доступная к резервированию на интерфейсе %s не равна ожидаемому значению 3Gbps в выводе команды, а соответствует - %s"%(int3_name,int3_max_resv_bw))
        assert_that(int3_alloc_bw=='1000.00',"Доступная к резервированию полоса пропускания на интерфейсе %s не равна ожидаемому значению 1Gbps в выводе команды, а соответствует - %s"%(int3_name,int3_alloc_bw))                
   

