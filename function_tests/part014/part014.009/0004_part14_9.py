from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.9:Функциональное тестирование MPLS TE FRR node-protection')
@allure.title('Проверка свичинга ICMP пакетов при срабатывании TE FRR Facility protection NNHOP:')
@pytest.mark.part14_9
#@pytest.mark.timeout(timeout=180, method='signal')
@pytest.mark.switching_L3VPN_TE_FRR_Faclity_NNHOP_protection
@pytest.mark.dependency(depends=["load_config149_dut1","load_config149_dut2","load_config149_dut3","load_config149_dut6"],scope='session')
@pytest.mark.parametrize('ip , login, password, int1', [(DUT3['host_ip'] , DUT3['login'] , DUT3['password'] , 'bu1'),(DUT1['host_ip'] , DUT1['login'] , DUT1['password'] , 'bu2')])
#@pytest.mark.parametrize('ip , login, password, int1', [(DUT1['host_ip'] , DUT1['login'] , DUT1['password'] , 'te0/0/11.352')])
def test_switching_L3VPN_TE_FRR_Faclity_NNHOP_protection_part14_9 (ip, login, password, int1):   
# В данном тесте запустим пинг между 192.168.41.2 (CE1) и 192.168.42.2 (CE2), а затем вызывовем переключение TE FRR protection. Т.е. защищаемый RSVP LSP to_atAR2@main будет
# перенаправлен в защитный RSVP LSP to_atAR1@bypass  
    result_loss=0 # Данная переменная нужна для процедуры generate_uu_trafic_from_labr02
# Подключимся к atAR2 и отправим в shutdown АС-интерфейс te0/0/11.12
    allure.attach.file('./network-schemes/part14_9_switching_L3VPN_TE_FRR_Facility_NNHOP_protection.png','Схема Теста', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(login , password)
    allure.step('Подключаемся к atDR1  по протоколу telnet')
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
# Шаг1. Начинаем проверку по переключению трафика путем отправки в shutdown интерфейса bu1 на atDR1     
    conn.execute('terminal datadump ')   
    cmd='show mpls rsvp lsps tunnel to_atAR2'
    conn.execute(cmd)
    resp = conn.response 
    allure.attach(resp, 'Шаг1. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    cmd='show mpls rsvp lsps tunnel to_atAR1'
    conn.execute(cmd)
    resp = conn.response 
    allure.attach(resp, 'Шаг1. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
    time.sleep(15)  # Подождем пока появится маршрутная информация на CE1 о префиксах CE2. Часто тест заканчивается по причине Network Unreachable  
# Запустим генерацию трафика с ESR-a путем запуска функции generate_uu_trafic_from_labr02 данный способ позволяет получить результат из функции в родительский thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'40027' , DUT4['login'] , DUT4['password'] , '192.168.42.2', 'vrf41' ,result_loss)
#        future = executor.map(generate_uu_trafic_from_labr02, timeout=180)
        conn.execute('config')
        cmd=('interface %s'%int1)
        conn.execute(cmd)
        conn.execute('shutdown')
        time.sleep(5) # Подождем пока трфик генерируется в параллельном потоке через защищаемый RSVP LSP
        conn.execute('commit') # После этого ожидаем что трафик переключится в bypass RSVP LSP
        print('Шаг1. Выполнили shutdown интерфейса %s на %s\r'%(int1,ip))
        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
        packet_sent = param_list[1]
        packet_recv = param_list[2]
        net_unreach = param_list[3]
    if (int(packet_loss) > 0):
        final_result=('Обнаружены потери пакетов (%s %%) между CE1 и CE2. Отправлено - %s пакетов, получено - %s пакетов'%(packet_loss,packet_sent,packet_recv))
        allure.attach(final_result,'Результат НЕ успешного теста на Шаге 1:')
    elif (int(packet_loss) == 0):
        final_result=('Потери пакетов между CE1 и CE2 НЕ обнаружены. Отправлено - %s пакетов, получено - %s пакетов'%(packet_sent,packet_recv))
        allure.attach(final_result,'Результат успешного теста на Шаге 1:')  

# Шаг2. восстанавливаем изначальный путь прохождения RSVP LSP туннеля to_atAR2 путем восстановления интерфейса bu1 и выполнения ручного переключения make-before-break 
    conn.execute('no shutdown')
    conn.execute('commit') # Возвращаем bu1 в первоночальное состояние 
    time.sleep(15) # Подождем когда туннель to_atAR2 вернется на изначальный путь   
    print('Шаг2. Подняли интерфейс %s на %s\r'%(int1,ip))    
    conn.execute('do mpls rsvp make-before-break to_atAR2')
    cmd='do show mpls rsvp lsps tunnel to_atAR2'
    conn.execute(cmd)
    resp = conn.response 
    allure.attach(resp, 'Шаг2. Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)        
    conn.execute('end')


    assert_that(net_unreach =='','Шаг1. В результатах пинга CE1<-->CE2 обнаружен признак Network is unreachable')
    assert_that(int(packet_loss) == 0,'Шаг1. Обнаружены потери пакетов %s %% между CE1 и CE2'%packet_loss)
