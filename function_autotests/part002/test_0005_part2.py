from conftest import *

@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.006:Проверка SNMP')
@allure.title('В данном тесте будем проверять вывод команды snmpwalk при взаимодействии с маршрутизатором ME')
@pytest.mark.part2
@pytest.mark.snmp
@pytest.mark.dependency(depends=["load_config002_dut1","load_config002_dut2","load_config002_dut3"],scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_snmp_part2(DUT):
    session = Session(hostname = DUT.host_ip , community = 'public' , version = 2)
    system_items = session.walk('SNMPv2-MIB::system')
    str1=''
    str2=''
    for item in system_items:
        str1=('{oid}.{oid_index} {snmp_type} = {value}'.format(oid=item.oid,oid_index=item.oid_index,snmp_type=item.snmp_type,value=item.value))
        str2 = str2 +'\n'+str1 
# Теперь в переменной str2 хранится весь вывод snmpwalk по OID 'systems'
# С помощью модуля textFSM и соответсвующего шаблона сформируем список переменных, которые потом будем анализиорвать в условиях assert
    template = open('./templates/parse_snmpwalk_system.txt')
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(str2)
#    result = fsm.ParseText(str2)
#    print(str2)   # Раскомментируй, если хочешь посмотреть вывод команды 'snmpwalk systems'
    allure.attach(str2,'Вывод команды snmpwalk', attachment_type=allure.attachment_type.TEXT)
# Если надо посмотреть отдельные элементы многомерного списка раскомментируй строки ниже 
#    print('SysDescr - %s\n'%processed_result[0]['SysDescr'])
#    print('SysContact - %s\n'%result[0]['SysContact'])
    SysDescr = processed_result[0]['SysDescr']
    SysContact = processed_result[0]['SysContact']
    SysName = processed_result[0]['SysName']
    SysLocation = processed_result[0]['SysLocation']
    SysUptime = processed_result[0]['SysUptime']
    if DUT.host_ip==DUT1.host_ip:
        assert_that(SysName==DUT1.hostname,"В выводе команды snmpwalk параметр Sysname не равен ожидаемому значению %s, а равен - %s"%(DUT1.hostname,SysName))
    if DUT.host_ip==DUT2.host_ip:
        assert_that(SysName==DUT2.hostname,"В выводе команды snmpwalk параметр Sysname не равен ожидаемому значению %s, а равен - %s"%(DUT2.hostname,SysName))
    if DUT.host_ip==DUT3.host_ip:
        assert_that(SysName==DUT3.hostname,"В выводе команды snmpwalk параметр Sysname не равен ожидаемому значению %s, а равен - %s"%(DUT3.hostname,SysName))

    assert_that(SysDescr !="","В выводе snmpwalk не обнаружен параметр SysDescr") 
    assert_that(SysContact != "","В выводе snmpwalk не обнаружен параметр SysContact")   
    assert_that(SysUptime != "","В выводе snmpwalk не обнаружен параметр SysUptime")
    assert_that(SysLocation == "Eltex","В выводе snmpwalk параметр SysLocation не равен ожидаемому зеачению Eltex, а равен - %s"%SysLocation) # Другие параметры из ветки systems не анализируем   

