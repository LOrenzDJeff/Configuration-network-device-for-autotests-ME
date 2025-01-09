from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.007:Проверка системных show-команд')
@allure.title('В данном тесте будем проверять вывод команды show interface description')
@pytest.mark.part2
@pytest.mark.show_int_description
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param("DUT1"), 
 			 pytest.param("DUT2"), 
 			 pytest.param("DUT3")
			]
			)
def test_show_interface_description (DUT):
# В данном тесте будем проверять description у интерфейсов, но только у тех которые используются в лаюораторном стенде    
# Подключаемся к маршрутизатору 'ip'    
    resp = ''
    with open('config_OOP.json', 'r', encoding='utf-8') as file:
        check = json.load(file)
    router = setting_ME(DUT)
    conn = Telnet()
    acc = Account(router.login, router.password)
    conn.connect(router.host_ip)
    conn.login(acc)
#    conn.set_prompt('#')        
# # Определим тип маршрутизатора (ME5000 или ME5100 или ME5200)
#     conn.execute('show system')
#     resp =conn.response
#     for RTtype in ['ME5000', 'ME5100', 'ME5200']:
#         index = resp.find(RTtype)
#         if index!= -1:
#             SysType=RTtype
#           print(SysType)        # Раскомментируй, если хочешь посмотреть как определился тип устройства.    
    conn.execute('terminal datadump')        
    resp = ''        
    conn.execute('show interface description') 
    resp = conn.response 
    resp_output=resp.partition('show interface description') # Данное действие необходимо чтобы избавиться от 'мусора ESC-последовательностей' в выводе  
    allure.attach(resp_output[2], 'Вывод команды show interface description', attachment_type=allure.attachment_type.TEXT)       
#    print('show interface description  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show int descr '
# C помощью магии модуля textFSM сравниваем вывод команды 'show int descr' c шаблоном в файле parse_show_int_descr_pizzabox_me.txt 
#    if (SysType == 'ME5100')^(SysType == 'ME5200'):
    template = open('./templates/parse_show_int_descr_pizzabox_me.txt')
    fsm = textfsm.TextFSM(template)
    processed_result = fsm.ParseTextToDicts(resp)
#    print(processed_result) # Раскомментируй, если хочешь посмотреть результат парсинга

    Top = processed_result[0]['Top']
    port1_name = processed_result[0]['port1_name']
    port1_adm_state = processed_result[0]['port1_adm_state']
    port1_oper_state = processed_result[0]['port1_oper_state']
    port1_desc = processed_result[0]['port1_desc']

    port2_name = processed_result[0]['port2_name']
    port2_adm_state = processed_result[0]['port2_adm_state']
    port2_oper_state = processed_result[0]['port2_oper_state']
    port2_desc = processed_result[0]['port2_desc']

    port3_name = processed_result[0]['port3_name']
    port3_adm_state = processed_result[0]['port3_adm_state']
    port3_oper_state = processed_result[0]['port3_oper_state']
    port3_desc = processed_result[0]['port3_desc']

    conn.send('quit\r')
    conn.close()

    assert_that (Top != '',"Заголовок команды show interface description не соответсвует шаблону")
# Первый порт смотрит на LABR01, второй порт на pizzabox, третий - на корзиину atDR1        
    if router.host_ip == check['DUT1']['host_ip']:
        assert_that(port1_name=='te0/0/11.352',"Ожидаемое имя первого порта на %s не равен ожидаемому te0/0/11.352, вместо этого он равен -%s"%(DUT1['hostname'],port1_name))
        assert_that(port1_adm_state=='up',"Ожидаемый административный статус первого порта на %s не равен UP "%DUT1['hostname'])
        assert_that(port1_oper_state=='up',"Ожидаемый операционный статус первого порта на %s не равен UP "%DUT1['hostname'])
        assert_that(port1_desc=='to_LABR01:ge-0/0/0.352',"Ожидаемый description первого порта на %s не равен  to_LABR01:ge-0/0/0.352"%DUT1['hostname'])

        assert_that(port2_name=='bu2',"Ожидаемое имя второго порта на %s не равен ожидаемому te0/0/2, вместо этого он равен -%s"%(DUT1['hostname'],port2_name))
        assert_that(port2_adm_state=='up',"Ожидаемый административный статус второго порта на %s не равен UP "%DUT1['hostname'])
        assert_that(port2_oper_state=='up',"Ожидаемый операционный статус второго порта на %s не равен UP "%DUT1['hostname'])
        assert_that(port2_desc=='to_atAR2:bundle-ether2',"Ожидаемый description второго порта на %s не равен  to_atAR2:te0/0/2"%DUT1['hostname'])  

        assert_that(port3_name=='bu1',"Ожидаемое имя третьего порта на %s не равен ожидаемому bu1, вместо этого он равен -%s"%(DUT1['hostname'],port3_name))
        assert_that(port3_adm_state=='up',"Ожидаемый административный статус третьего порта на %s не равен UP "%DUT1['hostname'])
        assert_that(port3_oper_state=='up',"Ожидаемый операционный статус третьего порта на %s не равен UP "%DUT1['hostname'])
        assert_that(port3_desc=='to_atDR1:bundle-ether1',"Ожидаемый description третьего порта на %s не равен  to_atDR1:bundle-ether1"%DUT1['hostname'])

    if router.host_ip == check['DUT2']['host_ip']:
        assert_that(port1_name=='te0/0/11.351',"Ожидаемое имя первого порта на %s не равен ожидаемому te0/0/11.351, вместо этого он равен -%s"%(DUT2['hostname'],port1_name))
        assert_that(port1_adm_state=='up',"Ожидаемый административный статус первого порта на %s не равен UP "%DUT2['hostname'])
        assert_that(port1_oper_state=='up',"Ожидаемый операционный статус первого порта на %s не равен UP "%DUT2['hostname'])
        assert_that(port1_desc=='to_LABR01:ge-0/0/0.351',"Ожидаемый description первого порта на %s не равен  to_LABR01:ge-0/0/0.351"%DUT2['hostname'])

        assert_that(port2_name=='bu2',"Ожидаемое имя второго порта на %s не равен ожидаемому te0/0/2, вместо этого он равен -%s"%(DUT2['hostname'],port2_name))
        assert_that(port2_adm_state=='up',"Ожидаемый административный статус второго порта на %s не равен UP "%DUT2['hostname'])
        assert_that(port2_oper_state=='up',"Ожидаемый операционный статус второго порта на %s не равен UP "%DUT2['hostname'])
        assert_that(port2_desc=='to_atAR1:bundle-ether2',"Ожидаемый description второго порта на %s не равен  to_atAR1:te0/0/2"%DUT2['hostname'])  

        assert_that(port3_name=='bu1',"Ожидаемое имя третьего порта на %s не равен ожидаемому bu1, вместо этого он равен -%s"%(DUT2['hostname'],port3_name))
        assert_that(port3_adm_state=='up',"Ожидаемый административный статус третьего порта на %s не равен UP "%DUT2['hostname'])
        assert_that(port3_oper_state=='up',"Ожидаемый операционный статус третьего порта на %s не равен UP "%DUT2['hostname'])
        assert_that(port3_desc=='to_atDR1:bundle-ether1',"Ожидаемый description третьего порта на %s не равен  to_atDR1:bundle-ether2"%DUT2['hostname'])

    if router.host_ip == check['DUT3']['host_ip']:
        assert_that(port1_name=='te0/1/5.350',"Ожидаемое имя первого порта на %s не равен ожидаемому te0/1/5.350, вместо этого он равен -%s"%(DUT3['hostname'],port1_name))
        assert_that(port1_adm_state=='up',"Ожидаемый административный статус первого порта на %s не равен UP "%DUT3['hostname'])
        assert_that(port1_oper_state=='up',"Ожидаемый операционный статус первого порта на %s не равен UP "%DUT3['hostname'])
        assert_that(port1_desc=='to_LABR01:ge-0/0/0.350',"Ожидаемый description первого порта на %s не равен  to_LABR01:ge-0/0/0.350"%DUT3['hostname'])

        assert_that(port2_name=='bu2',"Ожидаемое имя второго порта на %s не равен ожидаемому bu2, вместо этого он равен -%s"%(DUT3['hostname'],port2_name))
        assert_that(port2_adm_state=='up',"Ожидаемый административный статус второго порта на %s не равен UP "%DUT3['hostname'])
        assert_that(port2_oper_state=='up',"Ожидаемый операционный статус второго порта на %s не равен UP "%DUT3['hostname'])
        assert_that(port2_desc=='to_atAR2:bundle-ether2',"Ожидаемый description второго порта на %s не равен  to_AR2:bundle-ether2"%DUT3['hostname'])  

        assert_that(port3_name=='bu1',"Ожидаемое имя третьего порта на %s не равен ожидаемому bu1, вместо этого он равен -%s"%(DUT3['hostname'],port3_name))
        assert_that(port3_adm_state=='up',"Ожидаемый административный статус третьего порта на %s не равен UP "%DUT3['hostname'])
        assert_that(port3_oper_state=='up',"Ожидаемый операционный статус третьего порта на %s не равен UP "%DUT3['hostname'])
        assert_that(port3_desc=='to_atAR1:bundle-ether1',"Ожидаемый description третьего порта на %s не равен  to_atAR1:bundle-ether1"%DUT3['hostname'])
