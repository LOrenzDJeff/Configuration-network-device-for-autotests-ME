from conftest import *

@allure.epic('14:RSVP TE и Traffic Engineering')
@allure.feature('14.8:Функциональное тестирование RSVP транспорта для GRT трафика')
@allure.title('Проверка форвардинга GRT трафика через MPLS TE туннели с помощью статических маршрутов')
@pytest.mark.part14_8
@pytest.mark.GRT_traffic_over_RSVP_LSP_by_static_routes
@pytest.mark.dependency(depends=["load_config148_dut1","load_config148_dut2","load_config148_dut3","load_config148_dut4"],scope='session')
@pytest.mark.parametrize('ip , login, password, int1', [(DUT3['host_ip'] , DUT3['login'] , DUT3['password'] , 'to_atAR2')])
def test_GRT_traffic_over_RSVP_LSP_by_static_routes_part14_8 (ip, login, password, int1):   
# В данном тесте запустим пинг между 192.168.70.1 (CE1) и 192.168.56.1 (CE2) трафик перенаправляется в RSVP LSP с помощью статического маршрута
    result_loss=0 # Данная переменная нужна для процедуры generate_uu_trafic_from_labr02
# Подключимся к atDR1 и отправим в shutdown интерфейс bu1
    allure.attach.file('./network-schemes/part14_8_GRT_traffic_over_RSVP_LSP_by_static_routes.png','Схема Теста', attachment_type=allure.attachment_type.PNG)
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')    

#********************************************************************************************************
# Шаг 1
# Запустим генерацию трафика с ESR-a путем запуска функции generate_uu_trafic_from_labr02 данный способ позволяет получить результат из функции в родительский thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'10027' , DUT4['login'] , DUT4['password'] , '192.168.41.2', 'vrf42' ,result_loss)

        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
    if (int(packet_loss) > 0):
        final_result=('Обнаружены потери пакетов (%s %%) между CE1 и CE2'%packet_loss)
        allure.attach(final_result,'Шаг1: Результат НЕ успешного теста:')
    elif (int(packet_loss) == 0):
        final_result=('Потери пакетов между CE1 и CE2 НЕ обнаружены')
        allure.attach(final_result,'Шаг1: Результат успешного теста:')  

    assert_that(int(packet_loss) == 0,'На шаге 1 обнаружены потери пакетов %s %%  между CE1 и CE2'%packet_loss)

#********************************************************************************************************
# Запустим генерацию трафика с ESR-a путем запуска функции generate_uu_trafic_from_labr02 данный способ позволяет получить результат из функции в родительский thread
# Шаг 2
# Одновременно с генерацией отправляем в shutdown bu1 на atDR1
    conn.execute('config')
    cmd=('mpls rsvp tunnel  %s'%int1)
    conn.execute(cmd)
    conn.execute('shutdown')
    time.sleep(5) # Подождем пока трфик генерируется в параллельном потоке через защищаемый RSVP LSP
    conn.execute('commit') # После этого ожидаем что трафик переключится в bypass RSVP LSP
    print('Выполнили shutdown туннеля %s на %s\r'%(int1,ip))
# Шаг 3
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'10027' , DUT4['login'] , DUT4['password'] , '192.168.41.2', 'vrf42' ,result_loss)

        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
    if (int(packet_loss) > 0):
        final_result=('Обнаружены потери пакетов (%s %%) между CE1 и CE2'%packet_loss)
        allure.attach(final_result,'Шаг 3: Результат успешного теста:')
    elif (int(packet_loss) == 0):
        final_result=('Потери пакетов между CE1 и CE2 НЕ обнаружены')
        allure.attach(final_result,'Шаг 3: Результат НЕ успешного теста:')  
    assert_that(int(packet_loss) != 0,'На шаге 3 должны быть обнаружены потери пакетов между CE1 и CE2, однако их нет.')
# Шаг 4
    conn.execute('no shutdown')
    conn.execute('commit') # Возвращаем bu1 в первоночальное состояние
    print('Подняли туннель %s на %s\r'%(int1,ip))
# Шаг5

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_uu_trafic_from_labr02, DUT4['host_ip'],'10027' , DUT4['login'] , DUT4['password'] , '192.168.41.2', 'vrf42' ,result_loss)

        param_list = future.result() # Получаем из параллельного потока значение % потерянных пакетов и кол-во отправленных и принятых пакетов!
        packet_loss = param_list[0]
    if (int(packet_loss) > 0):
        final_result=('Обнаружены потери пакетов (%s %%) между CE1 и CE2'%packet_loss)
        allure.attach(final_result,'Шаг 5: Результат НЕ успешного теста:')
    elif (int(packet_loss) == 0):
        final_result=('Потери пакетов между CE1 и CE2 НЕ обнаружены')
        allure.attach(final_result,'Шаг 5: Результат успешного теста:')

    conn.execute('end')
    conn.close()
    assert_that(int(packet_loss) == 0,'На шаге 5 обнаружены потери пакетов %s %%  между CE1 и CE2'%packet_loss)

