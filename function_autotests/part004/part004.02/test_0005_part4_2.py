from conftest import *

@allure.epic('04:Подготовка IS-IS и LDP')
@allure.feature('4.02:Функциональное тестирование IS-IS') 
@allure.title('Проверка вывода команды show isis interface statistic')
@pytest.mark.part4_2
@pytest.mark.show_isis_int_stat
@pytest.mark.dependency(depends=["load_config042_dut1","load_config042_dut2","load_config042_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_isis_interface_stat_part4_2 (DUT): 
# В данном тесте будем проверять вывод команды 'show isis interface'      
#    resp = ''
    allure.attach.file('./network-schemes/part4_show_isis_interface_statistic.png','Схема теста:', attachment_type=allure.attachment_type.PNG) 
    allure.attach.file('./network-schemes/part4_show_isis_interface_statistic1.png','Что анализируется в выводе команды:', attachment_type=allure.attachment_type.PNG)  
    conn = Telnet()
    acc = Account(DUT.login, DUT.password)
    conn.connect(DUT.host_ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('show isis interface statistic') 
    resp = conn.response
    resp_output=resp.partition('show isis interface statistic') # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды show isis interface statistic', attachment_type=allure.attachment_type.TEXT)    
#    print('show isis interface stat  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show isis interface stat'
# C помощью магии модуля textFSM сравниваем вывод команды 'show isis interface' c шаблоном в файле parse_show_isis_interface_statistic.txt 
    template = open('./templates/parse_show_isis_interface_statistic1.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    conn.send('quit\r')
    conn.close()
    int1_name = result[0][0]
    int1_isis_pdu_lvl1_rec = result[0][1]
    int1_isis_pdu_lvl1_sent = result[0][2]
    int1_isis_pdu_lvl2_rec = result[0][3]
    int1_isis_pdu_lvl2_sent = result[0][4]
    int1_esis_pdu_lvl1_rec = result[0][5]
    int1_esis_pdu_lvl1_sent = result[0][6]
    int1_esis_pdu_lvl2_rec = result[0][7]
    int1_esis_pdu_lvl2_sent = result[0][8]
    int1_es_pdu_lvl1_rec = result[0][9]
    int1_es_pdu_lvl1_sent = result[0][10]
    int1_es_pdu_lvl2_rec = result[0][11]
    int1_es_pdu_lvl2_sent = result[0][12]
    int1_lsp_lvl1_rec = result[0][13]
    int1_lsp_lvl1_sent = result[0][14]
    int1_lsp_lvl2_rec = result[0][15]
    int1_lsp_lvl2_sent = result[0][16] 
    int1_csnp_lvl1_rec = result[0][17]
    int1_csnp_lvl1_sent = result[0][18]
    int1_csnp_lvl2_rec = result[0][19]
    int1_csnp_lvl2_sent = result[0][20]
    int1_psnp_lvl1_rec = result[0][21]
    int1_psnp_lvl1_sent = result[0][22]
    int1_psnp_lvl2_rec = result[0][23]
    int1_psnp_lvl2_sent = result[0][24] 
    int1_unknown_lvl1_rec = result[0][25]
    int1_unknown_lvl1_sent = result[0][26]
    int1_unknown_lvl2_rec = result[0][27]
    int1_unknown_lvl2_sent = result[0][28]
    int1_discarded_iih_lvl1_rec = result[0][29]
    int1_discarded_iih_lvl1_sent = result[0][30]
    int1_discarded_iih_lvl2_rec = result[0][31]
    int1_discarded_iih_lvl2_sent = result[0][32]
    int1_discarded_lsp_lvl1_rec = result[0][33]
    int1_discarded_lsp_lvl1_sent = result[0][34]
    int1_discarded_lsp_lvl2_rec = result[0][35]
    int1_discarded_lsp_lvl2_sent = result[0][36]
    int1_discarded_csnp_lvl1_rec = result[0][37]
    int1_discarded_csnp_lvl1_sent = result[0][38]
    int1_discarded_csnp_lvl2_rec = result[0][39]
    int1_discarded_csnp_lvl2_sent = result[0][40]
    int1_discarded_psnp_lvl1_rec = result[0][41]
    int1_discarded_psnp_lvl1_sent = result[0][42]
    int1_discarded_psnp_lvl2_rec = result[0][43]
    int1_discarded_psnp_lvl2_sent = result[0][44]

    int2_name = result[1][0]
    int2_isis_pdu_lvl1_rec = result[1][1]
    int2_isis_pdu_lvl1_sent = result[1][2]
    int2_isis_pdu_lvl2_rec = result[1][3]
    int2_isis_pdu_lvl2_sent = result[1][4]
    int2_esis_pdu_lvl1_rec = result[1][5]
    int2_esis_pdu_lvl1_sent = result[1][6]
    int2_esis_pdu_lvl2_rec = result[1][7]
    int2_esis_pdu_lvl2_sent = result[1][8]
    int2_es_pdu_lvl1_rec = result[1][9]
    int2_es_pdu_lvl1_sent = result[1][10]
    int2_es_pdu_lvl2_rec = result[1][11]
    int2_es_pdu_lvl2_sent = result[1][12]
    int2_lsp_lvl1_rec = result[1][13]
    int2_lsp_lvl1_sent = result[1][14]
    int2_lsp_lvl2_rec = result[1][15]
    int2_lsp_lvl2_sent = result[1][16] 
    int2_csnp_lvl1_rec = result[1][17]
    int2_csnp_lvl1_sent = result[1][18]
    int2_csnp_lvl2_rec = result[1][19]
    int2_csnp_lvl2_sent = result[1][20]
    int2_psnp_lvl1_rec = result[1][21]
    int2_psnp_lvl1_sent = result[1][22]
    int2_psnp_lvl2_rec = result[1][23]
    int2_psnp_lvl2_sent = result[1][24] 
    int2_unknown_lvl1_rec = result[1][25]
    int2_unknown_lvl1_sent = result[1][26]
    int2_unknown_lvl2_rec = result[1][27]
    int2_unknown_lvl2_sent = result[1][28]
    int2_discarded_iih_lvl1_rec = result[1][29]
    int2_discarded_iih_lvl1_sent = result[1][30]
    int2_discarded_iih_lvl2_rec = result[1][31]
    int2_discarded_iih_lvl2_sent = result[1][32]
    int2_discarded_lsp_lvl1_rec = result[1][33]
    int2_discarded_lsp_lvl1_sent = result[1][34]
    int2_discarded_lsp_lvl2_rec = result[1][35]
    int2_discarded_lsp_lvl2_sent = result[1][36]
    int2_discarded_csnp_lvl1_rec = result[1][37]
    int2_discarded_csnp_lvl1_sent = result[1][38]
    int2_discarded_csnp_lvl2_rec = result[1][39]
    int2_discarded_csnp_lvl2_sent = result[1][40]
    int2_discarded_psnp_lvl1_rec = result[1][41]
    int2_discarded_psnp_lvl1_sent = result[1][42]
    int2_discarded_psnp_lvl2_rec = result[1][43]
    int2_discarded_psnp_lvl2_sent = result[1][44]

    int3_name = result[2][0]
    int3_isis_pdu_lvl1_rec = result[2][1]
    int3_isis_pdu_lvl1_sent = result[2][2]
    int3_isis_pdu_lvl2_rec = result[2][3]
    int3_isis_pdu_lvl2_sent = result[2][4]
    int3_esis_pdu_lvl1_rec = result[2][5]
    int3_esis_pdu_lvl1_sent = result[2][6]
    int3_esis_pdu_lvl2_rec = result[2][7]
    int3_esis_pdu_lvl2_sent = result[2][8]
    int3_es_pdu_lvl1_rec = result[2][9]
    int3_es_pdu_lvl1_sent = result[2][10]
    int3_es_pdu_lvl2_rec = result[2][11]
    int3_es_pdu_lvl2_sent = result[2][12]
    int3_lsp_lvl1_rec = result[2][13]
    int3_lsp_lvl1_sent = result[2][14]
    int3_lsp_lvl2_rec = result[2][15]
    int3_lsp_lvl2_sent = result[2][16] 
    int3_csnp_lvl1_rec = result[2][17]
    int3_csnp_lvl1_sent = result[2][18]
    int3_csnp_lvl2_rec = result[2][19]
    int3_csnp_lvl2_sent = result[2][20]
    int3_psnp_lvl1_rec = result[2][21]
    int3_psnp_lvl1_sent = result[2][22]
    int3_psnp_lvl2_rec = result[2][23]
    int3_psnp_lvl2_sent = result[2][24] 
    int3_unknown_lvl1_rec = result[2][25]
    int3_unknown_lvl1_sent = result[2][26]
    int3_unknown_lvl2_rec = result[2][27]
    int3_unknown_lvl2_sent = result[2][28]
    int3_discarded_iih_lvl1_rec = result[2][29]
    int3_discarded_iih_lvl1_sent = result[2][30]
    int3_discarded_iih_lvl2_rec = result[2][31]
    int3_discarded_iih_lvl2_sent = result[2][32]
    int3_discarded_lsp_lvl1_rec = result[2][33]
    int3_discarded_lsp_lvl1_sent = result[2][34]
    int3_discarded_lsp_lvl2_rec = result[2][35]
    int3_discarded_lsp_lvl2_sent = result[2][36]
    int3_discarded_csnp_lvl1_rec = result[2][37]
    int3_discarded_csnp_lvl1_sent = result[2][38]
    int3_discarded_csnp_lvl2_rec = result[2][39]
    int3_discarded_csnp_lvl2_sent = result[2][40]
    int3_discarded_psnp_lvl1_rec = result[2][41]
    int3_discarded_psnp_lvl1_sent = result[2][42]
    int3_discarded_psnp_lvl2_rec = result[2][43]
    int3_discarded_psnp_lvl2_sent = result[2][44]
    assert_that(int1_name != '',"Имя интерфейса %s в выводе команды не соответсвует прописанному в шаблоне"%int1_name)
    assert_that((int(int1_isis_pdu_lvl1_rec)==0) and (int(int1_isis_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS Hello level-1 пакетов"%int1_name)
    assert_that((int(int1_isis_pdu_lvl2_rec)>0) and (int(int1_isis_pdu_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS Hello level-2 пакетов"%int1_name)
    assert_that((int(int1_esis_pdu_lvl2_rec)==0) and (int(int1_esis_pdu_lvl2_sent)==0) and (int(int1_esis_pdu_lvl1_rec)==0) and (int(int1_esis_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка и прием ES-IS Hello пакетов"%int1_name)
    assert_that((int(int1_es_pdu_lvl2_rec)==0) and (int(int1_es_pdu_lvl2_sent)==0) and (int(int1_es_pdu_lvl1_rec)==0) and (int(int1_es_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка и прием ES Hello пакетов"%int1_name)
    assert_that((int(int1_lsp_lvl1_rec)==0) and (int(int1_lsp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS LSP level-1 пакетов"%int1_name)
    assert_that((int(int1_lsp_lvl2_rec)>0) and (int(int1_lsp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS LSP level-2 пакетов"%int1_name)
    assert_that((int(int1_csnp_lvl1_rec)==0) and (int(int1_csnp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS CSNP level-1 пакетов"%int1_name)
    assert_that((int(int1_csnp_lvl2_rec)>0) and (int(int1_csnp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS CSNP level-2 пакетов"%int1_name)
    assert_that((int(int1_psnp_lvl1_rec)==0) and (int(int1_psnp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS PSNP level-1 пакетов"%int1_name)
    assert_that((int(int1_psnp_lvl2_rec)>0) and (int(int1_psnp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS PSNP level-2 пакетов"%int1_name)
    assert_that((int(int1_unknown_lvl2_rec)==0) and (int(int1_unknown_lvl2_sent)==0) and (int(int1_unknown_lvl1_rec)==0) and (int(int1_unknown_lvl1_sent)==0) ," На интерфейсе %s фиксируются ISIS Unknown пакеты"%int1_name)
    assert_that((int(int1_discarded_iih_lvl2_rec)==0) and (int(int1_discarded_iih_lvl2_sent)==0) and (int(int1_discarded_iih_lvl1_rec)==0) and (int(int1_discarded_iih_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED IIH пакеты"%int1_name)
    assert_that((int(int1_discarded_lsp_lvl2_rec)==0) and (int(int1_discarded_lsp_lvl2_sent)==0) and (int(int1_discarded_lsp_lvl1_rec)==0) and (int(int1_discarded_lsp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED LSP пакеты"%int1_name)
    assert_that((int(int1_discarded_csnp_lvl2_rec)==0) and (int(int1_discarded_csnp_lvl2_sent)==0) and (int(int1_discarded_csnp_lvl1_rec)==0) and (int(int1_discarded_csnp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED CSNP пакеты"%int1_name)
    assert_that((int(int1_discarded_psnp_lvl2_rec)==0) and (int(int1_discarded_psnp_lvl2_sent)==0) and (int(int1_discarded_psnp_lvl1_rec)==0) and (int(int1_discarded_psnp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED PSNP пакеты"%int1_name)

    assert_that(int2_name != '',"Имя интерфейса %s в выводе команды не соответсвует прописанному в шаблоне"%int2_name)
    assert_that((int(int2_isis_pdu_lvl1_rec)==0) and (int(int2_isis_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS Hello level-1 пакетов"%int2_name)
    assert_that((int(int2_isis_pdu_lvl2_rec)>0) and (int(int2_isis_pdu_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS Hello level-2 пакетов"%int2_name)
    assert_that((int(int2_esis_pdu_lvl2_rec)==0) and (int(int2_esis_pdu_lvl2_sent)==0) and (int(int2_esis_pdu_lvl1_rec)==0) and (int(int2_esis_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка и прием ES-IS Hello пакетов"%int2_name)
    assert_that((int(int2_es_pdu_lvl2_rec)==0) and (int(int2_es_pdu_lvl2_sent)==0) and (int(int2_es_pdu_lvl1_rec)==0) and (int(int2_es_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка и прием ES Hello пакетов"%int2_name)
    assert_that((int(int2_lsp_lvl1_rec)==0) and (int(int2_lsp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS LSP level-1 пакетов"%int2_name)
    assert_that((int(int2_lsp_lvl2_rec)>0) and (int(int2_lsp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS LSP level-2 пакетов"%int2_name)
    assert_that((int(int2_csnp_lvl1_rec)==0) and (int(int2_csnp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS CSNP level-1 пакетов"%int2_name)
    assert_that((int(int2_csnp_lvl2_rec)>0) and (int(int2_csnp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS CSNP level-2 пакетов"%int2_name)
    assert_that((int(int2_psnp_lvl1_rec)==0) and (int(int2_psnp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS PSNP level-1 пакетов"%int2_name)
    assert_that((int(int2_psnp_lvl2_rec)>0) and (int(int2_psnp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS PSNP level-2 пакетов"%int2_name)
    assert_that((int(int2_unknown_lvl2_rec)==0) and (int(int2_unknown_lvl2_sent)==0) and (int(int2_unknown_lvl1_rec)==0) and (int(int2_unknown_lvl1_sent)==0) ," На интерфейсе %s фиксируются ISIS Unknown пакеты"%int2_name)
    assert_that((int(int2_discarded_iih_lvl2_rec)==0) and (int(int2_discarded_iih_lvl2_sent)==0) and (int(int2_discarded_iih_lvl1_rec)==0) and (int(int2_discarded_iih_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED IIH пакеты"%int2_name)
    assert_that((int(int2_discarded_lsp_lvl2_rec)==0) and (int(int2_discarded_lsp_lvl2_sent)==0) and (int(int2_discarded_lsp_lvl1_rec)==0) and (int(int2_discarded_lsp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED LSP пакеты"%int2_name)
    assert_that((int(int2_discarded_csnp_lvl2_rec)==0) and (int(int2_discarded_csnp_lvl2_sent)==0) and (int(int2_discarded_csnp_lvl1_rec)==0) and (int(int2_discarded_csnp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED CSNP пакеты"%int2_name)
    assert_that((int(int2_discarded_psnp_lvl2_rec)==0) and (int(int2_discarded_psnp_lvl2_sent)==0) and (int(int2_discarded_psnp_lvl1_rec)==0) and (int(int2_discarded_psnp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED PSNP пакеты"%int2_name)

    assert_that(int3_name != '',"Имя интерфейса %s в выводе команды не соответсвует прописанному в шаблоне"%int3_name)
    assert_that((int(int3_isis_pdu_lvl1_rec)==0) and (int(int3_isis_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS Hello level-1 пакетов"%int3_name)
    assert_that((int(int3_isis_pdu_lvl2_rec)>0) and (int(int3_isis_pdu_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS Hello level-2 пакетов"%int3_name)
    assert_that((int(int3_esis_pdu_lvl2_rec)==0) and (int(int3_esis_pdu_lvl2_sent)==0) and (int(int3_esis_pdu_lvl1_rec)==0) and (int(int3_esis_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка и прием ES-IS Hello пакетов"%int3_name)
    assert_that((int(int3_es_pdu_lvl2_rec)==0) and (int(int3_es_pdu_lvl2_sent)==0) and (int(int3_es_pdu_lvl1_rec)==0) and (int(int3_es_pdu_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка и прием ES Hello пакетов"%int3_name)
    assert_that((int(int3_lsp_lvl1_rec)==0) and (int(int3_lsp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS LSP level-1 пакетов"%int3_name)
    assert_that((int(int3_lsp_lvl2_rec)>0) and (int(int3_lsp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS LSP level-2 пакетов"%int3_name)
    assert_that((int(int3_csnp_lvl1_rec)==0) and (int(int3_csnp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS CSNP level-1 пакетов"%int3_name)
    assert_that((int(int3_csnp_lvl2_rec)>0) and (int(int3_csnp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS CSNP level-2 пакетов"%int3_name)
    assert_that((int(int3_psnp_lvl1_rec)==0) and (int(int3_psnp_lvl1_sent)==0)," На интерфейсе %s фиксируется отправка или прием ISIS PSNP level-1 пакетов"%int3_name)
    assert_that((int(int3_psnp_lvl2_rec)>0) and (int(int3_psnp_lvl2_sent)>0)," На интерфейсе %s НЕ фиксируется отправка и прием ISIS PSNP level-2 пакетов"%int3_name)
    assert_that((int(int3_unknown_lvl2_rec)==0) and (int(int3_unknown_lvl2_sent)==0) and (int(int3_unknown_lvl1_rec)==0) and (int(int3_unknown_lvl1_sent)==0) ," На интерфейсе %s фиксируются ISIS Unknown пакеты"%int3_name)
    assert_that((int(int3_discarded_iih_lvl2_rec)==0) and (int(int3_discarded_iih_lvl2_sent)==0) and (int(int3_discarded_iih_lvl1_rec)==0) and (int(int3_discarded_iih_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED IIH пакеты"%int3_name)
    assert_that((int(int3_discarded_lsp_lvl2_rec)==0) and (int(int3_discarded_lsp_lvl2_sent)==0) and (int(int3_discarded_lsp_lvl1_rec)==0) and (int(int3_discarded_lsp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED LSP пакеты"%int3_name)
    assert_that((int(int3_discarded_csnp_lvl2_rec)==0) and (int(int3_discarded_csnp_lvl2_sent)==0) and (int(int3_discarded_csnp_lvl1_rec)==0) and (int(int3_discarded_csnp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED CSNP пакеты"%int3_name)
    assert_that((int(int3_discarded_psnp_lvl2_rec)==0) and (int(int3_discarded_psnp_lvl2_sent)==0) and (int(int3_discarded_psnp_lvl1_rec)==0) and (int(int3_discarded_psnp_lvl1_sent)==0) ," На интерфейсе %s фиксируются DISCARDED PSNP пакеты"%int3_name)
