from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 14.4')
@allure.story('Загрузка конфигурации на ME маршрутизатор')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part14_4
@pytest.mark.init_config14_4
@pytest.mark.parametrize('ip, hostname, login, password, part', 
			[pytest.param(DUT1['host_ip'], DUT1['hostname'], DUT1['login'], DUT1['password'], 'part14.4', marks=pytest.mark.dependency(name="load_config144_dut1")), 
 			 pytest.param(DUT2['host_ip'], DUT2['hostname'], DUT2['login'], DUT2['password'], 'part14.4', marks=pytest.mark.dependency(name="load_config144_dut2")), 
 			 pytest.param(DUT3['host_ip'], DUT3['hostname'], DUT3['login'], DUT3['password'], 'part14.4', marks=pytest.mark.dependency(name="load_config144_dut3"))])
 
@pytest.mark.usefixtures('me_init_configuration')
def test_me_init_config_upload_part14_4 (ip, hostname, login, password, part): 
# В данном тесте будем загружать начальную конфигурацию на ME маршрутизатор для тестов из Части 14.4 документа     
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
# # Сделаем clear BGP без этого не работает связность через EVPN (см задачу #285084)
#     conn.execute('clear bgp neighbor all')
#     print('\rВыполнили команду clear bgp neighbor all\r')


    #conn.set_prompt('will be used after clear mpls command')    
# По задаче #267523  необходимо выполнить clear mpls только после появления сообщения will become "1.0.0.2" after "clear mpls" command
# для этого выполним команду show mpls ldp parameters 
    cmd='show mpls ldp parameters'
    if hostname==DUT1['hostname']:
        conn.execute(cmd)
        resp=conn.response
        index_find=resp.find('will become "1.0.0.3" after "clear mpls" command')    
    if hostname==DUT2['hostname']:
        conn.execute(cmd)
        resp=conn.response
    #    print(resp)
        allure.attach(resp, 'Вывод команды %s до clear mpls'%cmd, attachment_type=allure.attachment_type.TEXT)
        template = open('./templates/parse_show_mpls_ldp_parameters_peers.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
    #    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        router_id=processed_result[0]['rt_id']
        transport_addr=processed_result[0]['transport_addr']

        if router_id!="1.0.0.2" or transport_addr!="1.0.0.2":
            print("\rШаг1. Router ID и Trasport address не равны значению 1.0.0.2, а равны %s и %s соответсвенно. Ждем 60 сек\r"%(router_id,transport_addr))
            time.sleep(60) # Подождем пока в телнет сессии не появится сообщение will be used after clear mpls command
        index_find=resp.find('will become "1.0.0.2" after "clear mpls" command')    
    if hostname==DUT3['hostname']:
        conn.execute(cmd)
        resp=conn.response
    #    print(resp)
        allure.attach(resp, 'Вывод команды %s до clear mpls'%cmd, attachment_type=allure.attachment_type.TEXT)
        template = open('./templates/parse_show_mpls_ldp_parameters_peers.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
    #    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        router_id=processed_result[0]['rt_id']
        transport_addr=processed_result[0]['transport_addr']

        if router_id!="1.0.0.1" or transport_addr!="1.0.0.1":
            print("\rШаг1. Router ID и Trasport address не равны значению 1.0.0.1, а равны %s и %s соответсвенно. Ждем 60 сек\r"%(router_id,transport_addr))
            time.sleep(60) # Подождем пока в телнет сессии не появится сообщение will be used after clear mpls command
        index_find=resp.find('will become "1.0.0.1" after "clear mpls" command')    
    if index_find !=-1:
        print('Обнаружена фраза will become "1.0.0.n" after "clear mpls" command до clear mpls')
    
    conn.set_timeout(60)
    conn.execute('clear mpls') # Перезапустим MPLS чтобы применился LSR-ID иначе LDP сосендства не установятся
    time.sleep(10) # Подождем пока mpls перезапустится и применится LSR-ID
# Повторно выполним команду show mpls ldp parameters уже после clear mpla и проанализируем её вывод

#     if hostname==DUT1['hostname']:
#         if router_id!="1.0.0.3" or transport_addr!="1.0.0.3":
#             print("\r Шаг2. Router ID и Trasport address не равны значению 1.0.0.3, а равны %s и %s соответсвенно. Ждем 60 сек\r"%(router_id,transport_addr))
# #            time.sleep(60) # Подождем пока в телнет сессии не появится сообщение will be used after clear mpls command
#         index_find=resp.find('will become "1.0.0.3" after "clear mpls" command')    
    if hostname==DUT2['hostname']:
        conn.execute(cmd)
        resp=conn.response
        allure.attach(resp, 'Вывод команды %s после clear mpls'%cmd, attachment_type=allure.attachment_type.TEXT)
        template = open('./templates/parse_show_mpls_ldp_parameters_peers.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
    #    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        router_id=processed_result[0]['rt_id']
        transport_addr=processed_result[0]['transport_addr']

        if router_id!="1.0.0.2" or transport_addr!="1.0.0.2":
            print("\rШаг2. Router ID и Trasport address не равны значению 1.0.0.2, а равны %s и %s соответсвенно. Ждем 60 сек\r"%(router_id,transport_addr))
#            time.sleep(60) # Подождем пока в телнет сессии не появится сообщение will be used after clear mpls command
        index_find=resp.find('will become "1.0.0.2" after "clear mpls" command')    
    if hostname==DUT3['hostname']:
        conn.execute(cmd)
        resp=conn.response
        allure.attach(resp, 'Вывод команды %s после clear mpls'%cmd, attachment_type=allure.attachment_type.TEXT)
        template = open('./templates/parse_show_mpls_ldp_parameters_peers.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
    #    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        router_id=processed_result[0]['rt_id']
        transport_addr=processed_result[0]['transport_addr']

        if router_id!="1.0.0.1" or transport_addr!="1.0.0.1":
            print("\rШаг2. Router ID и Trasport address не равны значению 1.0.0.1, а равны %s и %s соответсвенно. Ждем 60 сек\r"%(router_id,transport_addr))
#            time.sleep(60) # Подождем пока в телнет сессии не появится сообщение will be used after clear mpls command
        index_find=resp.find('will become "1.0.0.1" after "clear mpls" command')    
    if index_find !=-1:
        print('Обнаружена фраза will become "1.0.0.n" after "clear mpls" command после clear mpls')
    


    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))
    conn.send('quit\r')
    conn.close()

    print('Загрузка конфигурации для %s на %s прошла успешно!'%(part,hostname))

# Причина по которой тесты раздела 14_4 не выполняются на втором стенде
# 0/ME5210S:atDR1# show mpls ldp parameters 
# Thu Mar  7 10:41:30 2024
#   LDP Parameters:
#     Router ID: 10.0.19.5 (will become "1.0.0.1" after "clear mpls" command) <<<<< Вот!
#     Transport address: 10.0.19.5
#   Graceful Restart:
#     Status: disabled
#     Reconnect Timeout: 120 sec, Forwarding State Holdtime: 120 sec
  
#   Neighbors:
  
#     Peer address: 1.0.0.2 
#       BFD status: disabled
#       Holdtime interval: 40 sec
#       Hello interval: 0 sec
  
#   Interfaces:
  
#     Interface Bundle-ether 2 
#       BFD status: disabled
#       Holdtime interval: 40 sec
#       Hello interval: 15 sec
# 0/ME5210S:atDR1# 
