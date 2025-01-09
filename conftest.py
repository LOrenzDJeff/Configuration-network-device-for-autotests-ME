from configs.old_config_me import *
from configs.old_config_jun import *
from configs.old_config_mes import *
from all_lib import *

LOGGER = logging.getLogger(__name__)

global templates
global tftp_dir

remote_ip = '192.168.192.1' # Удалённый ip адрес связность до которого нужно проверить в тесте
ntp_server_ip = '192.168.16.89'


with open ('./configs/config.json') as f:
    templates = json.load(f)
    DUT1 = setting_ME("DUT1",templates)
    DUT2 = setting_ME("DUT2",templates)
    DUT3 = setting_ME("DUT3",templates)
    DUT4 = setting_vMX("DUT4",templates)
    DUT5 = setting_MES("DUT5",templates)
    DUT6 = templates['DUT6']
    DUT7 = templates['DUT7']
    DUT9 = templates['DUT9']
    hardware_set_id = templates['hardware_set_id']

if hardware_set_id == "1":
    tftp_dir = "Init_configs"
elif hardware_set_id == "3":
    tftp_dir = "Init_configs_3"

#********* from Mr. Khutoryansky***********************
# from autotests.__init__ import (
#     CONFIG,
#     DynamicInterfaces,
#     Connection
# )
# @pytest.fixture(scope='function', autouse=True)
# def RemoveThatObjects():
#     yield
#     for intf in list(DynamicInterfaces):
#         intf.remove()
#     for conn in Connection.connections:
#         conn.remove()
#*************end**************************************

class thread_with_trace(threading.Thread):  # Данный класс нужен для генерации параллельных потоков с возможностью килла по таймауту
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

def me_reboot(ip,login,password):
    def ping_device(ip, event):
        while not event.is_set():
            response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE)
            #print(response) #Информация о пинге
            if response.returncode == 0:
                event.set()
            time.sleep(1)

    def reboot_device(ip, login, password, event):
        tn = telnetlib.Telnet(ip)

        tn.read_until(b"login: ")
        tn.write(login.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        tn.read_until(b'#')
        tn.write(b"reload system\n")
        tn.read_until(b'Do you really want to reload system? (y/n):')
        tn.write(b"y\n")

        time.sleep(90)
        ping_thread = threading.Thread(target=ping_device, args=(ip, event))
        ping_thread.start()

        start_time = time.time()
        event.wait(400)  # Ждем сигнала или истечения времени ожидания
        elapsed_time = time.time() - start_time

        if event.is_set():
            print(f"Маршрутизатор успешно перезагрузился за {elapsed_time:.2f} +- 90 секунд")
            time.sleep(90)
            conn1 = Telnet()
            acc1 = Account(login, password)
            conn1.connect(ip)
            conn1.login(acc1)
            conn1.set_prompt('#')
            conn1.execute('show version')
            conn1.send('quit\r')
            conn1.close()
        else:
            print("Превышено время ожидания перезагрузки коммутатора")
            pytest.fail("Превышено время ожидания перезагрузки коммутатора")

        ping_thread.join()

    event = threading.Event()
    reboot_thread = threading.Thread(target=reboot_device, args=(ip, login, password, event))
    reboot_thread.start()
    reboot_thread.join()


@pytest.fixture(scope='function')
def run_iperf():
    time.sleep(80)
    with allure.step('Запускаем iperf'):
        services = subprocess.Popen(f'docker-compose -f tools/docker/iperf/docker-compose.yaml up ',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    time.sleep(21)
    yield
    with allure.step('Останавливаем сервисы'):
        subprocess.check_call(f'docker-compose -f tools/docker/iperf/docker-compose.yaml down',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result, _ = services.communicate()
        allure.attach(result.decode(), 'Логи работы сервера iperf')

    
@pytest.fixture(scope='function')
def run_tacacs_server():
    with allure.step('Запускаем сервер tacacs'):
        services = subprocess.Popen(f'docker-compose -f tools/docker/tacacs/docker-compose.yaml up ',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    time.sleep(25)
    yield
    with allure.step('Останавливаем сервисы'):
        subprocess.check_call(f'docker-compose -f tools/docker/tacacs/docker-compose.yaml down',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result, _ = services.communicate()
        allure.attach(result.decode(), 'Логи работы сервера tacacs')   
        
@pytest.fixture(scope='function')
def run_radius_server():
    with allure.step('Запускаем сервер radius'):
        services = subprocess.Popen(f'docker-compose -f tools/docker/FreeRadius/docker-compose.yaml up ',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    time.sleep(25)
    yield
    with allure.step('Останавливаем сервисы'):
        subprocess.check_call(f'docker-compose -f tools/docker/FreeRadius/docker-compose.yaml down',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result, _ = services.communicate()
        allure.attach(result.decode(), 'Логи работы сервера radius')
def labr02_bgp_on(host_ip,login,password,as_number):
     conn =Telnet()
     acc = Account(login, password)
     conn.connect(host_ip)
     conn.login(acc)
     conn.execute('configure')
     conn.execute('router bgp %s'%(as_number))
     conn.execute('enable')
     conn.execute('do commit')
     conn.execute('do confirm')
     conn.execute('end')
# def ping_from_esr(host_ip,login,password,vrf_name,dst_ip,num_pack):
#     conn = Telnet()
#     acc = Account(login,password)
#     conn.connect(host_ip)
#     conn.login(acc) 
#     conn.execute('ping vrf %s %s packets %s'%(vrf_name,dst_ip,num_pack))

def connection_test(host_ip, login, password, part):
     conn = Telnet()
     conn.set_driver(ME5000CliDriver())
     acc = Account(login, password)
     conn.connect(host_ip)
     if part == 'part2':
        conn.waitfor('Username:')
        resp = conn.response
        conn.login(acc)
        resp = resp + conn.response
     if part == 'part18':
        conn.login(acc)
        resp = conn.response
     return resp

def connection_test_ssh(host_ip,login,password):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host_ip,username=login, password=password, look_for_keys=False,allow_agent=False)
    res=c._transport.get_banner().decode("utf-8")
    with c.invoke_shell() as ssh:
         time.sleep(3)
         res1 = ssh.recv(3000).decode("utf-8")
         res = res + res1
         return res
def clear_bgp_neighbors(host_ip, login, password):
     conn = Telnet()
     acc = Account(login,password)
     conn.connect(host_ip)
     conn.login(acc)
     if host_ip == DUT4['host_ip']:
        conn.execute('clear bgp')
     else:
        conn.execute('clear bgp neighbor all')
          
def radius_auth_change_mode_to_off(host_ip, login, password):
     conn = Telnet()
     acc = Account(login,password)
     conn.connect(host_ip)
     conn.login(acc)
     conn.execute('config')
     conn.execute('no line ssh login authentication AAA-Radius')
     conn.execute('no line telnet login authentication AAA-Radius')
     conn.execute('commit')
     conn.execute('end')


def change_int(conn, change_inter, del_ip):
    
    cmd='config'
    conn.execute(cmd)
    cmd='interface bu1'
    conn.execute(cmd)
    cmd='no ipv4 address '+ del_ip
    conn.execute(cmd)
    cmd='ipv4 address '+ change_inter
    conn.execute(cmd)
    cmd='commit'
    conn.execute(cmd)
    cmd='end'
    conn.execute(cmd)
    
def clear_arp(conn):
    cmd='clear arp'
    conn.execute(cmd)
    #print('Очистили arp-cache на Всех интерфейсах\r')

def arp_proxy_on(host_ip, hostname, login, password, int1, int2):
     conn = Telnet()
     acc = Account(login, password)
     conn.connect(host_ip)
     conn.login(acc)
     conn.set_prompt('#')
     #print('Начинаем включать proxy arp\r')
     cmd='config'
     conn.execute(cmd)
#     allure.attach(conn.response,'Переход в режим кофигурирования', attachment_type=allure.attachment_type.TEXT) 
     cmd='interface '+int1
     conn.execute(cmd)
#     allure.attach(conn.response,'Переход в режим конфигурирования первого интерфейса', attachment_type=allure.attachment_type.TEXT) 
     cmd='arp proxy'
     conn.execute(cmd)
#     allure.attach(conn.response,'Включение arp proxy', attachment_type=allure.attachment_type.TEXT) 
     cmd='commit'
     conn.execute(cmd)
#     allure.attach(conn.response,'Применение изменений', attachment_type=allure.attachment_type.TEXT) 
     cmd='exit'
     conn.execute(cmd)
#     allure.attach(conn.response, 'Выход', attachment_type=allure.attachment_type.TEXT) 
     cmd='interface '+int2
     conn.execute(cmd)
#     allure.attach(conn.response,'Переход в режим конфигурирования второго интерфейса', attachment_type=allure.attachment_type.TEXT) 
     cmd='arp proxy'
     conn.execute(cmd)
#     allure.attach(conn.response,'Включение arp proxy', attachment_type=allure.attachment_type.TEXT)  
     cmd='commit'
     conn.execute(cmd)
#     allure.attach(conn.response,'Применение изменений', attachment_type=allure.attachment_type.TEXT) 
     cmd='end'
     conn.execute(cmd)
#     allure.attach(conn.response,'Выход', attachment_type=allure.attachment_type.TEXT) 
     #print('Включили proxy arp\r')
    # conn.close()

def arp_proxy_off(host_ip, hostname, login, password, int1, int2):
     conn = Telnet()
     acc = Account(login, password)
     conn.connect(host_ip)
     conn.login(acc)
     conn.set_prompt('#')
     #print('Начинаем выключать proxy arp\r')
     cmd='config'
     conn.execute(cmd)
#     allure.attach(conn.response,'Переход в режим кофигурирования', attachment_type=allure.attachment_type.TEXT) 
     cmd='interface '+ int1
     conn.execute(cmd)
#     allure.attach(conn.response,'Переход в режим конфигурирования первого интерфейса',attachment_type=allure.attachment_type.TEXT)
     cmd='no ipv4 address 192.168.55.2/30'
     conn.execute(cmd)
#     allure.attach(conn.response,'Удаление старого ip-адреса', attachment_type=allure.attachment_type.TEXT) 
     cmd='ipv4 address 192.168.60.2/30'
     conn.execute(cmd)
#     allure.attach(conn.response,'Назначение нового ip-адреса', attachment_type=allure.attachment_type.TEXT)  
     cmd='no arp proxy'
     conn.execute(cmd)
#     allure.attach(conn.response,'Выключение arp proxy',  attachment_type=allure.attachment_type.TEXT) 
     cmd='interface '+int2
     conn.execute(cmd)
#     allure.attach(conn.response,'Переход в режим конфигурирования второго интерфейса', attachment_type=allure.attachment_type.TEXT)
     cmd='no ipv4 address 192.168.55.5/30'
     conn.execute(cmd)
#     allure.attach(conn.response,'Удаление старого ip-адреса', attachment_type=allure.attachment_type.TEXT) 
     cmd='ipv4 address 192.168.60.253/30'
     conn.execute(cmd)
#     allure.attach(conn.response,'Назначение нового ip-адреса', attachment_type=allure.attachment_type.TEXT)  
     cmd='no arp proxy'
     conn.execute(cmd)
#     allure.attach(conn.response,'Выключение arp proxy', attachment_type=allure.attachment_type.TEXT)  
     cmd='commit'
     conn.execute(cmd)
#     allure.attach(conn.response,'Применение изменений',attachment_type=allure.attachment_type.TEXT) 
     cmd='end'
     conn.execute(cmd)
#     allure.attach(conn.response,'Выход', attachment_type=allure.attachment_type.TEXT) 
     #print('Выключили proxy arp\r')
    # conn.close()


@pytest.fixture(scope='function', autouse=True)
def generate_pytest_log(request):
    yield
    report_call = getattr(request.node, "rep_call", None)
    if report_call:
        if report_call.failed:
            LOGGER.info(
                f"Тест 123Z{request.node.location[2]}123Z провалился. Причина: '{report_call.longrepr.reprcrash.message}'")
        elif report_call.skipped:
            LOGGER.info(
                f"Тест 123Z{request.node.location[2]}123Z был пропущен. Причина: '{report_call.longrepr.reprcrash.message}'")
        elif report_call.passed:
            LOGGER.info(f"Тест 123Z{request.node.location[2]}123Z выполнен успешно.")

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session):
    if (
        hasattr(session.config, 'workerinput') or
        session.config.option.collectonly or
        session.exitstatus == 6
    ):
        return
    terminalreporter = session.config.pluginmanager.get_plugin("terminalreporter")
    total = terminalreporter._numcollected
    deselected = len(terminalreporter.stats.get("deselected", []))
    failed = len(terminalreporter.stats.get('failed', []))
    passed = len(terminalreporter.stats.get('passed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    error = len(terminalreporter.stats.get('error', []))
    xfailed = len(terminalreporter.stats.get("xfailed", []))
    xpassed = len(terminalreporter.stats.get("xpassed", []))
    selected = total - deselected
    time.sleep(40)
# Пишем в файл эти параметры, чтобы другие скрипты смогли ими воспользоваться для формироавания отчетов в e-mail, telegramm и сохранения в БД
    file = open('./test_results.txt','w')     
    print("\rОбщее количество тестов - %s.\r"%total)
    file.write("Общее количество тестов - %s\r"%total)
    print("\rОбщее количество PASSED тестов - %s.\r"%passed)
    file.write("Общее количество PASSED тестов - %s\r"%passed)
    print("\rОбщее количество SELECTED тестов - %s.\r"%selected)
    file.write("Общее количество SELECTED тестов - %s\r"%selected)
    print("\rОбщее количество FAILED тестов - %s.\r"%failed)
    file.write("Общее количество FAILED тестов - %s\r"%failed)
    print("\rОбщее количество SKIPPED тестов - %s.\r"%skipped)
    file.write("Общее количество SKIPPED тестов - %s\r"%skipped)
    print("\rОбщее количество ERROR тестов - %s.\r"%error)    
    file.write("Общее количество ERROR тестов - %s\r"%error)

# Читать.... https://docs.pytest.org/en/7.2.x/reference.html?highlight=api#testreport


    failed_test_index=0
    failed_test_list=terminalreporter.stats.get('failed', [])

# Запишем в файл  test_results.txt все FAILED тесты, чтобы потом иметь возможность сохранить их в БД
    while failed_test_index<len(failed_test_list):
        failed_test_name_str1=failed_test_list[failed_test_index].nodeid.partition('::')
#        failed_test_longrepr.reprcrash.message=failed_test_list[failed_test_index].longrepr.reprcrash.message
        failed_test_assert_message=failed_test_list[failed_test_index].longrepr.reprcrash.message
        failed_test_name=failed_test_name_str1[2].partition('[')
        failed_test_param=failed_test_name[2].partition(']')
        print('failed_test_name - %s, failed_test_param - %s, Assert-message - %s'%(failed_test_name[0],failed_test_param[0], failed_test_assert_message))
        file.write("failed_test_name - %s, failed_test_param - %s, Assert-message - %s\r"%(failed_test_name[0],failed_test_param[0], failed_test_assert_message))
        failed_test_index=failed_test_index+1


    passed_test_index=0
    passed_test_list=terminalreporter.stats.get('passed', [])

# Запишем в файл  test_results.txt все PASSED тесты, чтобы потом иметь возможность сохранить их в БД
    while passed_test_index<len(passed_test_list):
        passed_test_name_str1=passed_test_list[passed_test_index].nodeid.partition('::')
        passed_test_duration=passed_test_list[passed_test_index].duration
        passed_test_name=passed_test_name_str1[2].partition('[')
        passed_test_param=passed_test_name[2].partition(']')
        print('passed_test_name - %s, passed_test_param - %s, passed_test_duration - %d'%(passed_test_name[0],passed_test_param[0], passed_test_duration))
        file.write("passed_test_name - %s, passed_test_param - %s, passed_test_duration - %d\r"%(passed_test_name[0],passed_test_param[0],passed_test_duration))
        passed_test_index=passed_test_index+1



    skipped_test_index=0
    skipped_test_list=terminalreporter.stats.get('skipped', [])

# Запишем в файл  test_results.txt все SKIPPED тесты, чтобы потом иметь возможность сохранить их в БД
    while skipped_test_index<len(skipped_test_list):
        skipped_test_name_str1=skipped_test_list[skipped_test_index].nodeid.partition('::')
        skipped_test_longrepr=skipped_test_list[skipped_test_index].longrepr
        skipped_test_name=skipped_test_name_str1[2].partition('[')
        skipped_test_param=skipped_test_name[2].partition(']')
        print('skipped_test_name - %s, skipped_test_param - %s, skipped_test_longrepr - %s'%(skipped_test_name[0],skipped_test_param[0],skipped_test_longrepr))
        file.write("skipped_test_name - %s, skipped_test_param - %s, skipped_test_longrepr - %s\r"%(skipped_test_name[0],skipped_test_param[0],skipped_test_longrepr))
        skipped_test_index=skipped_test_index+1
    file.close()

def locate_download_link(version, platform):
    n1=version.find('.')
    v1=version[0:n1]
    v1_last=version[n1+1:len(version)]
#       print(v1)     # Первая цифра из номера версии
    n2=v1_last.find('.')
    v2=v1_last[0:n2]
    v2_last=v1_last[n2+1:len(v1_last)]
#       print(v2)    # Вторая цифра из номера версии
    n3=v2_last.find('.')
    v3=v2_last[0:n3]
#       print(v3)    # Третья цифра из номера версии
#    located_link=('http://lab2.eltex.loc:8585/%s.%s.%s/firmware_%s.%s'%(v1,v2,v3,version,platform))
# Для версии 3.10 ссылка изменилась на такую:
    located_link=('https://validator.eltex.loc/checkerusers/me5k.jenkins/files/%s.%s.%s/firmware_%s.%s'%(v1,v2,v3,version,platform))
    return(located_link)


def show_version (ip, login, password):
# Подключаемся к маршрутизатору 'ip'    
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')        
    conn.execute('show version') 
    resp = conn.response 
    allure.attach(resp, 'Вывод команды show version', attachment_type=allure.attachment_type.TEXT)           
#    print('show version  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show version '
# C помощью магии модуля textFSM сравниваем вывод команды 'show system environment' c шаблоном в файле parse_show_version.txt    
    template = open('./templates/parse_show_version.txt')
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
#    print(result)    # Раскомментируй, если хочешь посмотреть результат парсинга    
    conn.send('quit\r')
    conn.close()
#    print('Router %s has version %s\r end_of_version'%(ip,result[0][0]))
    return(result[0][0])


# Передаём в функцию параметры: ip - адрес куда подключаемся; hostname -имя узла куда подключаемся; software_version - версия ПО
# В процедуре me_software_upgrade четвёртый (последний) аргумент обозначает версию ПО на которую необходимо сделать обновление  
# Если версия ПО указана как "", то будет осуществлён поиск самого свежего ПО (на момент запуска скрипта) на странице http://red.eltex.loc/projects/me5000/wiki/2-3-0
def me_software_upgrade(ip, login, password, hostname,software_version, software_path, booting_timer):
    print('Начинаем процедуру обновления ПО на маршрутизаторе %s\r'%hostname)
    # Проверим текущую версию ПО
    current_version=show_version(ip,login,password) 
#    print('Используемая версия ПО на маршрутизаторе %s - %s'%(hostname,current_version)) 
    if (current_version.find(software_version)!=-1)&(software_version!=''):
        print('Версия %s уже используется'%(software_version))
        exit_message=('Версия уже используется')
        exit(exit_message)
    conn = Telnet()
    acc = Account(login, password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.set_timeout(60)
    
    if (current_version != software_version)&(hostname==DUT2['hostname']):
        if (software_version==''):
            download_link=locate_download_link('', 'me5200')
            soft_ver=download_link.partition('firmware_')
            soft_version=soft_ver[2].rpartition('.')
            software_version=soft_version[0]
            if (current_version.find(software_version)!=-1):  #Проверим, а не используется ли уже, найденная "свежая" версия ПО на маршрутизаторе  
                exit_message=('Версия уже используется')
                sys.exit(exit_message)
            print('Для маршрутизатора %s обнаружена свежая версия ПО -%s'%(hostname,software_version))
        else:
            download_link=locate_download_link(software_version, 'me5200')  
        try:
            print("\nПытаемся выполнить команду wget -q -N --no-check-certificate %s -P %s\n"%(download_link,software_path))
            subprocess.call(["wget", download_link, "-q", "-N", "--no-check-certificate", "-P", software_path])
        except Exception as err:
            print("Произошла ошибка - %s, type - %s"%(err,type(err)))
            rise
        conn.execute('copy tftp://%s/firmware_%s.me5200 fs://firmware'%(DUT7['host_ip'],software_version))
#        booting_timer=460
    elif (current_version != software_version)&(hostname==DUT1['hostname']):
        if (software_version==''):
            download_link=locate_download_link('', 'me2001')
            soft_ver=download_link.partition('firmware_')
            soft_version=soft_ver[2].rpartition('.')
            software_version=soft_version[0]
            if (current_version.find(software_version)!=-1):  #Проверим, а не используется ли уже, найденная "свежая" версия ПО на маршрутизаторе  
                exit_message=('Версия уже используется')
                sys.exit(exit_message)
            print('Для маршрутизатора %s обнаружена свежая версия ПО -%s'%(hostname,software_version))
        else:
            download_link=locate_download_link(software_version, 'me2001')      
        try:
            print("\nПытаемся выполнить команду wget -q -N --no-check-certificate %s -P %s\n"%(download_link,software_path))
            subprocess.call(["wget", download_link, "-q", "-N", "--no-check-certificate", "-P", software_path])
        except Exception as err:
            print("Произошла ошибка - %s, type - %s"%(err,type(err)))
            rise
        conn.execute('copy tftp://%s/firmware_%s.me2001 fs://firmware vrf MGN'%(DUT7['host_ip'],software_version))
#        booting_timer=360
    elif (current_version != software_version)&(hostname==DUT3['hostname']):
        if (software_version==''):
            download_link=locate_download_link('', 'fmc32')
            soft_ver=download_link.partition('firmware_')
            soft_version=soft_ver[2].rpartition('.')
            software_version=soft_version[0]
            if (current_version.find(software_version)!=-1):  #Проверим, а не используется ли уже, найденная "свежая" версия ПО на маршрутизаторе  
                exit_message=('Версия уже используется')
                sys.exit(exit_message)
            print('Для маршрутизатора %s обнаружена свежая версия ПО -%s'%(hostname,software_version))
        else:
            download_link=locate_download_link(software_version, 'fmc32')   
        try:
            print("\nПытаемся выполнить команду wget -q -N --no-check-certificate %s -P %s\n"%(download_link,software_path))
            subprocess.call(["wget", download_link, "-q", "-N", "--no-check-certificate", "-P", software_path])
        except Exception as err:
            print("Произошла ошибка - %s, type - %s"%(err,type(err)))
            rise
        conn.execute('copy tftp://%s/firmware_%s.fmc32 fs://firmware vrf mgmt-intf'%(DUT7['host_ip'],software_version))
#        booting_timer=430
    else:
        exit_message=('Имя %s указано не верно'%hostname)
        sys.exit(exit_message)

    conn.execute('firmware select alternate')
    conn.set_prompt('[n]')
    conn.execute('reload system')
    conn.execute('y\r')
    print ('Маршрутизатор %s отправлен в перезагрузку стартовая версия ПО -%s'%(hostname,software_version))
    conn.close()
    print('Ждем %d секунд и пытаемся подключиться к маршрутизатору %s для завершения upgrade-a'%(booting_timer,hostname))
    time.sleep(booting_timer)
    conn2 = Telnet()
    acc2 = Account(login, password)
    conn2.connect(ip)
    conn2.login(acc2)
    conn2.set_prompt('#')
    conn2.execute('firmware confirm')
    conn2.execute('show version')
    if (conn2.response).find(software_version) != -1:
        print('Обновление ПО до версии %s успешно завершено на маршрутизаторе %s'%(software_version,hostname))
    else:
        print('Обновление ПО до версии %s НЕуспешно завершено на маршрутизаторе %s'%(software_version,hostname))
    #print('Обновление ПО до версии %s завершено на маршрутизаторе %s'%(software_version,hostname))
    conn2.close()
    DUT1.connection()
    DUT2.connection()
    DUT3.connection()
    return(software_version)

# Функция поиска ipv4 адреса соседа на интерфейсе
def locate_ipv4_neighbor(conn,interface):
    conn.execute('terminal datadump')
    conn.execute('show interface %s'%interface)
    resp = conn.response
    template = open('./templates/parse_show_interface.txt')
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
    ipv4_int_addr=processed_result[0]['ipv4_addr']
#    print('Обнаруженный ipv4 адрес на интерфейсе -%s\r'%ipv4_int_addr)
    int1 = ipaddress.ip_interface(ipv4_int_addr)
    subnet=ipaddress.ip_network(int1.network)
#    list(subnet.hosts())
#    for ip in subnet:
#        print(ip)
    if subnet[1] == int1.ip:
        return(subnet[2])
    else :
        return(subnet[1])

def locate_neighbor(conn,type, interface): # Функция будет определять соседа на P2P интерфейсе. Тип соседа может быть ipv4 либо ipv6
    if type == 'ipv4':
        conn.execute('show arp interface %s'%interface)
        resp = conn.response 
#        print('show arp interface  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show arp interface'
# C помощью магии модуля textFSM сравниваем вывод команды 'show route isis' c шаблоном в файле parse_show_route_isis_lfa_protect_disable.txt 
        template = open('./templates/parse_show_arp_interface.txt')
    elif type == 'ipv6':
        conn.execute('show ipv6 neighbor interface %s'%interface)
        resp = conn.response 
#        print('show ipv6 neighbor interface  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show ipv6 neighbor interface'
# C помощью магии модуля textFSM сравниваем вывод команды 'show ipv6 neighbor interface' c шаблоном в файле parse_show_ipv6_neighbor_interface.txt 
        resp = conn.response 
        template = open('./templates/parse_show_ipv6_neighbor_interface.txt')
    else:
        return False
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(resp)
#    print(result) # Хочешь посмотреть результат парсинга - раскомментируй
    neighbor_addr = result[0][0]     
    return(neighbor_addr)

def locate_if_index(conn, interface): # Функция будет определять if_index переданного ей интерфейса
    conn.execute('show interface %s'%interface)
    resp = conn.response 
#    print('show interface  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interface'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interface' c шаблоном в файле parse_show_interface_ifindex.txt 
    template = open('./templates/parse_show_interface_ifindex.txt')
    fsm = textfsm.TextFSM(template)
    result=fsm.ParseText(resp)
    if_index=result[0][0]
    return(if_index)


def me_alarm_check(conn, alarm_pattern): # Передаём в фикстуру параметры: ip - адрес куда подключаемся; hostname -имя узла куда подключаемся;
    # conn = Telnet()
    # acc = Account(login, password)
    # conn.connect(ip)
    # conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('show alarm')
    resp=conn.response
    print(resp)
    alarm_index=resp.find(alarm_pattern)
    if alarm_index != -1:
        print('Авария %s обнаружена в выводе show alarm\r'%alarm_pattern)
    else:
        print('Аварии %s  НЕТ в выводе show alarm\r'%alarm_pattern)
    return(alarm_index)


#Данная процедура нужна для того чтобы переносить ip управления из mgmt-intf в MGN или GRT (в зависимости от устройства)
# Это необходимо делать в случае если до запуска автотестов на рутерах были конфигурации где управление идет исключительно через mgmt-intf
@pytest.fixture(scope='function')
def move_mgmt_int_from_mgmt_intf(ip, hostname, login, password):
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.execute('terminal datadump')
    conn.execute('show interfaces  mgmt 0/fmc0/1')
    resp=conn.response
    mgmt_ipv4_addr_flag =resp.find('IPv4 address is')
    if (mgmt_ipv4_addr_flag != -1) and (hostname!=DUT3['hostname']):
        conn.execute('configure')
        conn.execute('interface mgmt 0/fmc0/1')
        conn.execute('no ipv4 address %s/23'%ip)
#        conn.execute('vrf mgmt-intf')
        conn.execute('exit')
        conn.execute('interface tengigabitethernet 0/0/11.4040')
        conn.execute('encapsulation outer-vid 4040')
        conn.execute('ipv4 address %s/23'%ip)
        if (hostname==DUT1['hostname']):
            conn.execute('vrf MGN')
            conn.execute('exit')
            conn.execute('vrf MGN')
            conn.execute('rd 1:1')
            conn.execute('exit')
            conn.execute('telnet server vrf MGN')
        elif (hostname==DUT2['hostname']):
            conn.execute('telnet server vrf default')
        conn.send('commit\r')
        time.sleep(2)
        conn.send('y\r')
        time.sleep(20) # Подождем пока переключится управление с одного интерфейса на другой

    conn.close()

@pytest.fixture(scope='function')
def me_open_debug_collect_logs(request, ip, hostname, login, password, debug_cmd_list):
 #   print('Включаем отладку')
    conn1 = Telnet()
    acc1 = Account(login, password)
    conn1.connect(ip)
    conn1.login(acc1)
    conn1.set_prompt('#')
    for i in debug_cmd_list: # Улучшайзинг унд оптимайзинг фром Хуторянский
        print(i)
        conn1.execute(i)
    yield
    if request.node.rep_call.failed:  # Данная структура с полями создается hook-ом  hookimpl в файле conftest.py 
    # Данный код выполняется если тест из которого вызвана эта фикстура, зафэйлился...
        # conn1 = Telnet()
        # acc1 = Account(login, password)
        # conn1.connect(ip)
        # conn1.login(acc1)
        # conn1.set_prompt('#')
        dir_path =('./tftpd/logs/%s/'%request.node.nodeid)                               # это унифицированный путь и для рабочей машины и для виртуальной
#        dir_path =('/var/lib/tftpboot/logs/%s/'%request.node.nodeid)              #этот путь нужен в случае когда тесты запускаются на моей рабочей машине
#        dir_path =('/home/pryahin/me5k/tftpd/logs/%s/'%request.node.nodeid)       #этот путь нужен в случае когда тесты запускаются на виртуальной машине
        if os.path.exists(dir_path) != True:
#            print('\rПытаемся создать папку - %s\r'%dir_path)
            try:
                os.makedirs(dir_path,exist_ok=True)
#                os.mkdir(dir_path, 0o777)
            except OSError as error:
                print('\rВозникла ошибка при создании папки для сбора логов -%s\r'%error)
            os.chmod(dir_path, 0o777)

        conn1.set_timeout(120)
        conn1.execute('show tech-support')
        if hostname=='atAR2':
            conn1.execute('copy fs://logs tftp://%s/logs/%s/'%(DUT7['host_ip'],request.node.nodeid))            
        elif hostname=='atDR1':
            conn1.execute('copy fs://logs tftp://%s/logs/%s/ vrf mgmt-intf'%(DUT7['host_ip'],request.node.nodeid))            
        elif hostname=='atAR1':
            conn1.execute('copy fs://logs tftp://%s/logs/%s/ vrf MGN'%(DUT7['host_ip'],request.node.nodeid))            
        conn1.execute('no debug all')
    else:
        conn1.execute('no debug all')
        conn1.close()


@pytest.fixture()
def run_dhcp_service():
    with allure.step('Запускаем сервер DHCP'):
        services = subprocess.Popen('docker-compose -f tools/docker/DHCP/docker-compose.yaml up',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    time.sleep(8)
    yield
    with allure.step('Останавливаем сервер DHCP'):
        subprocess.check_call('docker-compose -f tools/docker/DHCP/docker-compose.yaml down -t 1',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result, _ = services.communicate()
        allure.attach(result.decode(), 'Логи работы сервера DHCP')


@pytest.fixture()
def run_dhcpv6_service():
    with allure.step('Запускаем сервер DHCPv6'):
        services = subprocess.Popen('docker-compose -f tools/docker/DHCPv6/docker-compose.yaml up',
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
    time.sleep(8)
    yield
    with allure.step('Останавливаем сервер DHCPv6'):
        subprocess.check_call('docker-compose -f tools/docker/DHCPv6/docker-compose.yaml down -t 1',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result, _ = services.communicate()
        allure.attach(result.decode(), 'Логи работы сервера DHCPv6')


#Вспомогательная функция для генерации  трафика со стороны LABR02 (используется в тесте test_unknown_unicast_flood)
def generate_uu_trafic_from_labr02(ip, packets_count,login, password, dst_ip, vrf_name, result_loss):
#    try:
    print('Старт процедуры генерации трафика\r') # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    allure.step('Подключаемся к маршрутизатору LABR02 по протоколу telnet')
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    if (vrf_name=='None') or (vrf_name==''):
        cmd=('ping  %s packets 10 flood size 1400'%dst_ip)
        conn.execute(cmd) # Генерим тестовые 10 пакетов в сторону dst_ip, если связь отсутсвует, то завершаем процедуру
        resp1=conn.response
#        print(resp1)
        template = open('./templates/parse_ping_from_esr.txt') 
        fsm1 = textfsm.TextFSM(template)
        processed_result1=fsm1.ParseTextToDicts(resp1)
#        print(processed_result1)   # Раскомментируй, если хочешь посмотреть результат парсинга
        net_unreachable = processed_result1[0]['network_unreachable']
        if net_unreachable !='':
            result1_loss = '100'
            result1_pkt_sent = '0'
            result1_pkt_recv ='0'
        else:
            result1_loss = processed_result1[0]['loss']
            result1_pkt_sent = processed_result1[0]['pkt_sent']
            result1_pkt_recv = processed_result1[0]['pkt_recv']        

        
        if result1_loss=='100' or result1_loss=='':
            print('Обнаружена потеря связности на первых 10 пингах')
#            sys.exit('Нет IP связности в первых 10 пингах')
            return(result1_loss,result1_pkt_sent,result1_pkt_recv,net_unreachable)
        cmd=('ping  %s packets %s flood size 1400'%(dst_ip,packets_count))
        conn.execute(cmd) # Генерим 'packets_count' в сторону dst_ip 
    else :
        cmd=('ping vrf %s %s packets 10 flood size 1400'%(vrf_name,dst_ip))
        conn.execute(cmd) # Генерим тестовые 10 пакетов в сторону dst_ip, если связь отсутсвует, то завершаем процедуру
        resp1=conn.response
#        print(resp1)
        template = open('./templates/parse_ping_from_esr.txt') 
        fsm1 = textfsm.TextFSM(template)
        processed_result1=fsm1.ParseTextToDicts(resp1)
#        print(processed_result1)   # Раскомментируй, если хочешь посмотреть результат парсинга
        net_unreachable = processed_result1[0]['network_unreachable']
        if net_unreachable !='':
            result1_loss = '100'
            result1_pkt_sent = '0'
            result1_pkt_recv ='0'
        else:
            result1_loss = processed_result1[0]['loss']
            result1_pkt_sent = processed_result1[0]['pkt_sent']
            result1_pkt_recv = processed_result1[0]['pkt_recv']

        if result1_loss=='100' or result1_loss=='':
            print('Обнаружена потеря связности на первых 10 пингах')
            return(result1_loss,result1_pkt_sent,result1_pkt_recv,net_unreachable)

        cmd=('ping  vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count))
        conn.execute(cmd) # Генерим 'packets_count' в сторону dst_ip


    resp = conn.response
#    resp_output=resp.partition('ping  vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count)) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    resp_output=resp.partition(cmd)
    allure.attach(resp_output[2], 'Вывод команды: %s'%cmd, attachment_type=allure.attachment_type.TEXT)    

#    print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'ping' c шаблоном в файле parse__ping_from_esr.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    net_unreachable = processed_result[0]['network_unreachable']
    if net_unreachable !='':
        result_loss = '100'
        result_pkt_sent = '0'
        result_pkt_recv ='0'
    else:
        result_loss = processed_result[0]['loss']
        result_pkt_sent = processed_result[0]['pkt_sent']
        result_pkt_recv = processed_result[0]['pkt_recv']

    print('Процедура генерации трафика окончена')
    conn.close()
    return(result_loss,result_pkt_sent,result_pkt_recv,net_unreachable)

#Вспомогательная функция для генерации не flood трафика со стороны LABR02 (пришлось задуматься о её создании когда vMX2 перестал справляться с потоком ICMP в режиме flood)
def generate_slow_trafic_from_labr02(ip, packets_count,login, password, dst_ip, vrf_name, send_interval,result_loss):
#    try:
    print('Старт процедуры генерации трафика\r') # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    allure.step('Подключаемся к маршрутизатору LABR02 по протоколу telnet')
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    if (vrf_name=='None') or (vrf_name==''):
        conn.execute('ping  %s packets 10 interval %d size 1400'%(dst_ip,send_interval)) # Генерим тестовые 10 пакетов в сторону dst_ip, если связь отсутсвует, то завершаем процедуру
        resp1=conn.response
#        print(resp1)
        template = open('./templates/parse_ping_from_esr.txt') 
        fsm1 = textfsm.TextFSM(template)
#        result1 = fsm1.ParseText(resp1)
        processed_result1=fsm1.ParseTextToDicts(resp1)
#        print(processed_result1)   # Раскомментируй, если хочешь посмотреть результат парсинга
        net_unreachable = processed_result1[0]['network_unreachable']
        if net_unreachable !='':
            result1_loss = '100'
            result1_pkt_sent = '0'
            result1_pkt_recv ='0'
        else:
            result1_loss = processed_result1[0]['loss']
            result1_pkt_sent = processed_result1[0]['pkt_sent']
            result1_pkt_recv = processed_result1[0]['pkt_recv']        

        
        if result1_loss=='100' or result1_loss=='':
            print('Обнаружена потеря связности на первых 10 пингах')
#            sys.exit('Нет IP связности в первых 10 пингах')
            return(result1_loss,result1_pkt_sent,result1_pkt_recv,net_unreachable)
        conn.execute('ping  %s packets %s interval %d size 1400'%(dst_ip,packets_count,send_interval)) # Генерим 'packets_count' в сторону dst_ip 
    else :
        conn.execute('ping vrf %s %s packets 10 interval %d size 1400'%(vrf_name,dst_ip, send_interval)) # Генерим тестовые 10 пакетов в сторону dst_ip, если связь отсутсвует, то завершаем процедуру
        resp1=conn.response
#        print(resp1)
        template = open('./templates/parse_ping_from_esr.txt') 
        fsm1 = textfsm.TextFSM(template)
        processed_result1=fsm1.ParseTextToDicts(resp1)
#        result1 = fsm1.ParseText(resp1)
#        print(processed_result1)   # Раскомментируй, если хочешь посмотреть результат парсинга
        net_unreachable = processed_result1[0]['network_unreachable']
        if net_unreachable !='':
            result1_loss = '100'
            result1_pkt_sent = '0'
            result1_pkt_recv ='0'
        else:
            result1_loss = processed_result1[0]['loss']
            result1_pkt_sent = processed_result1[0]['pkt_sent']
            result1_pkt_recv = processed_result1[0]['pkt_recv']

        if result1_loss=='100' or result1_loss=='':
            print('Обнаружена потеря связности на первых 10 пингах')
            return(result1_loss,result1_pkt_sent,result1_pkt_recv,net_unreachable)

        conn.execute('ping  vrf %s %s packets %s interval %d size 1400'%(vrf_name,dst_ip,packets_count,send_interval)) # Генерим 'packets_count' в сторону dst_ip


    resp = conn.response
    resp_output=resp.partition('ping  vrf %s %s packets %s interval %d size 1400'%(vrf_name,dst_ip,packets_count,send_interval)) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
    allure.attach(resp_output[2], 'Вывод команды: ping  vrf %s %s packets %s interval %d size 1400'%(vrf_name,dst_ip,packets_count,send_interval), attachment_type=allure.attachment_type.TEXT)    
#    allure.attach(resp)
#    print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'ping' c шаблоном в файле parse__ping_from_esr.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    net_unreachable = processed_result[0]['network_unreachable']
    if net_unreachable !='':
        result_loss = '100'
        result_pkt_sent = '0'
        result_pkt_recv ='0'
    else:
        result_loss = processed_result[0]['loss']
        result_pkt_sent = processed_result[0]['pkt_sent']
        result_pkt_recv = processed_result[0]['pkt_recv']

    print('Процедура генерации трафика окончена')
    conn.send('exit\r')
    conn.close()
    return(result_loss,result_pkt_sent,result_pkt_recv,net_unreachable)



#Вспомогательная функция для генерации  трафика со стороны LABR02 (используется в тесте test_unknown_unicast_flood)
def generate1_uu_trafic_from_labr02(ip, packets_count,login, password, dst_ip, vrf_name, result_loss):
    try:
        print('Старт процедуры генерации трафика\r') # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
        resp = ''
        conn = Telnet()
        acc = Account(login , password)
        allure.step('Подключаемся к маршрутизатору LABR02 по протоколу telnet')
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        if (vrf_name=='None') or (vrf_name==''):
            conn.execute('ping  %s packets %s flood size 1400'%(dst_ip,packets_count)) # Генерим 'packets_count' в сторону dst_ip 
        else :
            conn.execute('ping  vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count)) # Генерим 'packets_count' в сторону dst_ip

        resp = conn.response
        resp_output=resp.partition('ping  vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count)) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
        allure.attach(resp_output[2], 'Вывод команды: ping  vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count), attachment_type=allure.attachment_type.TEXT)    

#        allure.attach(resp)
#        print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'ping' c шаблоном в файле parse__ping_from_esr.txt 
        template = open('./templates/parse_ping_from_esr.txt') 
        fsm = textfsm.TextFSM(template)
        processed_result=fsm.ParseTextToDicts(resp)
        result_loss = processed_result[0]['loss']
        print('Процедура генерации трафика окончена')
        conn.close()
        return(result_loss)
    except:
        sys.exit('Получен сигнал')




#Вспомогательная функция для генерации  трафика со стороны LABR02 (используется в тесте test_unknown_unicast_flood) параметры передаются через queue
def generate2_uu_trafic_from_labr02(ip, packets_count,login, password, dst_ip, vrf_name, result_loss,q):
    print('Старт процедуры генерации трафика\r') # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
    q.put(0)
    q.put(0)
    q.put(0)
    q.put('')
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    if (vrf_name=='None') or (vrf_name==''):
        conn.execute('ping  %s packets %s flood size 1400'%(dst_ip,packets_count)) # Генерим 'packets_count' в сторону dst_ip 
    else:
        conn.execute('ping vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count)) # Генерим 'packets_count' в сторону dst_ip 

    resp = conn.response
    resp_output=resp.partition('ping  vrf %s %s packets %s flood size 1400'%(vrf_name,dst_ip,packets_count)) # Данное действие необходимо чтобы избавиться от 'мусора' в выводе
#    print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'ping' c шаблоном в файле parse__ping_from_esr.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    net_unreachable = processed_result[0]['network_unreachable']
    if net_unreachable !='':
        result_loss = '100'
        result_pkt_sent = '0'
        result_pkt_recv ='0'
    else:
        result_loss = processed_result[0]['loss']
        result_pkt_sent = processed_result[0]['pkt_sent']
        result_pkt_recv = processed_result[0]['pkt_recv']

    print('Процедура генерации трафика окончена')
    conn.close()
    q.get()
    q.get()
    q.get()
    q.get()
    q.put(result_loss)
    q.put(result_pkt_sent)
    q.put(result_pkt_recv)
    q.put(net_unreachable)


#Функция для генерации 4 попыток по 10 ICMP пакетов со стороны LABR02 до первой успешной попытки
# Между первой и второй попыткой interval секунд
# Между второй и третьей попыткой 2*interval секунд
# Между третьей и четвертой попыткой 3*interval секунд

def four_attempts_ping_from_labr02(conn,cmd,interval,packet_loss,resp):
    conn.execute(cmd)  # Проверяем связность впервый раз!
    resp = conn.response    
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/1/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
    template = open('./templates/parse_ping_from_esr.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    net_unreachable=processed_result[0]['network_unreachable']
    if net_unreachable=='': # Если есть признак network unreachable, его надо учитывать
        packet_loss = processed_result[0]['loss']
    else:
        packet_loss='100'
        print('\nОбнаружен признак network_unreachable\n')

    i=1
    while i<4:
        if (int(packet_loss)!=0):
            print("\nС %s-го раза потери пинга - %s %%. Ждем %d секунд\n"%(i,packet_loss,i*interval))
            time.sleep(i*interval)
            conn.execute(cmd)
            resp=conn.response
#            fsm = textfsm.TextFSM(template) # без этой команды, success_rate будет всегда равен значению, присвоенному переменной до входа в цикл 
# Я разобрался как работает парсинг, если textfsm.TextFSM(template) вызывать, только один раз - вне цикла
# Команда  processed_result=fsm.ParseTextToDicts(resp) добавляет к списку словарей processed_result новый словарь, поэтому для доступа к переменным нужно увеличивать индекс
# а не обращаться с индексом 0
            processed_result=fsm.ParseTextToDicts(resp)
#            print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
            net_unreachable=processed_result[0]['network_unreachable']
            if net_unreachable=='': # Если есть признак network unreachable, его надо учитывать
                packet_loss=processed_result[i]['loss'] # i, а не 0 т.к fsm = textfsm.TextFSM(template) только один раз исполняется
            else:
                packet_loss='100'
                print('\nОбнаружен признак network_unreachable\n')
        else:
            print("\nС %s-го раза потери пинга - %s %%.\n"%(i,packet_loss))
            i=3
        i=i+1
    print("\nИтоговая успешность пинга составила - %s потерь %%\n"%packet_loss)
    return(packet_loss,resp)


# def four_attempts_ping_from_labr02(conn,cmd,interval,packet_loss,resp):
#     conn.execute(cmd)  # Проверяем связность впервый раз!
#     resp = conn.response    
# # C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/1/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
#     template = open('./templates/parse_ping_from_esr.txt') 
#     fsm = textfsm.TextFSM(template)
#     processed_result=fsm.ParseTextToDicts(resp)
# #    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
#     net_unreachable=processed_result[0]['network_unreachable']
#     if net_unreachable=='': # Если есть признак network unreachable, его надо учитывать
#         packet_loss = processed_result[0]['loss']
#     else:
#         packet_loss='100'
#         print('\rОбнаружен признак network_unreachable\r')

#     if (int(packet_loss)>10):
#         print("\rС первого раза пинг был не успешен. Потери - %s %%. Ждем %d секунд\r"%(packet_loss, interval))
#         time.sleep(interval)
#         conn.execute(cmd)  # Проверяем связность второй раз
#         resp = conn.response
#         template = open('./templates/parse_ping_from_esr.txt')
#         fsm = textfsm.TextFSM(template)
#         processed_result=fsm.ParseTextToDicts(resp)
# #        print(processed_result)
#         net_unreachable=processed_result[0]['network_unreachable']
#         if net_unreachable=='': # Если есть признак network unreachable, его надо учитывать
#             packet_loss = processed_result[0]['loss']
#         else:
#             packet_loss='100'
#             print('\rОбнаружен признак network_unreachable\r')

#         if int(packet_loss)>10:
#             print("Со второго раза пинг был не успешен.Потери - %s %%. Ждем %d секунд\r"%(packet_loss, 2*interval))
#             time.sleep(2*interval)
#             conn.execute(cmd)  # Проверяем связность тертий раз
#             resp = conn.response
#             template = open('./templates/parse_ping_from_esr.txt')
#             fsm = textfsm.TextFSM(template)
#             processed_result=fsm.ParseTextToDicts(resp)
#             net_unreachable=processed_result[0]['network_unreachable']
# #            print(processed_result)
#             if net_unreachable=='': # Если есть признак network unreachable, его надо учитывать
#                 packet_loss = processed_result[0]['loss']                
#             else:
#                 packet_loss='100'
#                 print('\rОбнаружен признак network_unreachable\r')

#             if int(packet_loss)>10:
#                 print("С третьего раза пинг был не успешен. Потери - %s %%. Ждем %d секунд\r"%(packet_loss,3*interval))
#                 time.sleep(3*interval)
#                 conn.execute(cmd)  # Проверяем связность четвертый (заключительный) раз 
#                 resp = conn.response
#                 template = open('./templates/parse_ping_from_esr.txt')
#                 fsm = textfsm.TextFSM(template)
#                 processed_result=fsm.ParseTextToDicts(resp)
# #                print(processed_result)
#                 net_unreachable=processed_result[0]['network_unreachable']
#                 if net_unreachable=='': # Если есть признак network unreachable, его надо учитывать
#                     packet_loss = processed_result[0]['loss']
#                 else:
#                     packet_loss='100'
#                     print('\rОбнаружен признак network_unreachable\r')
#     return(packet_loss,resp)



#Функция для генерации 4 попыток отправки ICMP пакетов со стороны ME до первой успешной 
# Между первой и второй попыткой interval секунд
# Между второй и третьей попыткой 2*interval секунд
# Между третьей и четвертой попыткой 3*interval секунд

def four_attempts_ping_from_me(conn,cmd,interval,success_rate,resp):
    conn.execute(cmd)  # Проверяем связность
    resp = conn.response    
    template = open('./templates/parse_ping_from_me.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    success_rate=processed_result[0]['success_rate']
    
    i=1
    while i<4:

        if (float(success_rate)!=100):
            print("\nС %s-го раза успешность пинга - %s %%. Ждем %d секунд\n"%(i,success_rate, i*interval))
            time.sleep(i*interval)
            cmd_in_circule=cmd+(' count %d'%(4*i)) # С каждой итерацей увеличиваем кол-во, отправленных ICMP пакетов в i-раз
            conn.execute(cmd_in_circule)  # Проверяем связность
            resp = conn.response
#            fsm = textfsm.TextFSM(template) # без этой команды, success_rate будет всегда равен значению, присвоенному переменной до входа в цикл 
# Я разобрался как работает парсинг, если textfsm.TextFSM(template) вызывать, только один раз - вне цикла
# Команда  processed_result=fsm.ParseTextToDicts(resp) добавляет к списку словарей processed_result новый словарь, поэтому для доступа к переменным нужно увеличивать индекс
# а не обращаться с индексом 0
            processed_result=fsm.ParseTextToDicts(resp)
#            print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
            success_rate=processed_result[i]['success_rate'] # i, а не 0 т.к fsm = textfsm.TextFSM(template) только один раз исполняется
        else:
            print("\nС %s-го раза успешность пинга - %s %%.\n"%(i,success_rate))
            i=3
        i=i+1
    print("\nИтоговая успешность пинга составила - %s %%\n"%success_rate)    
    return(success_rate,resp)

#Вспомогательная функция для проверки параметров pps на SUB-интерфейсе (используется в тесте test_unknown_unicast_flood)
def check_subint_rate_pps(ip,login,password,int1,int2,int3):
#    print('Старт процедуры проверки check_subint_rate_pps на %s %s %s\r'%(int1,int2,int3)) # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
    time.sleep(20)   # Ждем пока накопится статистика на интерфейсах чем больше ждем тем больше вероятность того что assert условие выполнится
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
#    allure.step('Подключаемся к маршрутизатору ME по протоколу telnet')
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    cmd =('show interface %s'%int1)
    conn.execute(cmd) # Смотрим счетчики интерфейса int1 
    resp = conn.response

    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)
#    print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces ....'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces' c шаблоном в файле parse_show_subinterface_counters.txt 
    template = open('./templates/parse_show_subinterface_counters.txt') 
    fsm = textfsm.TextFSM(template)
#    result = fsm.ParseText(resp)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    int1_input_pps = processed_result[0]['pps_input']
    cmd =('show interface %s'%int2)    
    conn.execute(cmd) # Смотрим счетчики интерфейса int2 
    resp = conn.response

    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)    
#    print('Output of command  - %s'%resp1)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces ....'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces' c шаблоном в файле parse_show_subinterface_counters.txt 
    template = open('./templates/parse_show_subinterface_counters.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
#    print(processed_result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    int2_output_pps = processed_result[0]['pps_output']
    cmd = ('show interface %s'%int3)    
    conn.execute(cmd) # Смотрим счетчики интерфейса int3 
    resp = conn.response
    allure.attach(resp, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT) 
#    print('Output of command  - %s'%resp1)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces ....'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces' c шаблоном в файле parse_show_subinterface_counters.txt 
    template = open('./templates/parse_show_subinterface_counters.txt') 
    fsm = textfsm.TextFSM(template)
    processed_result=fsm.ParseTextToDicts(resp)
    conn.send('quit\r')
    conn.close()
#    print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
    int3_output_pps = processed_result[0]['pps_output']    
# раскомментируй 3 принта ниже, если хочешь увидеть результаты входящего pps и исходящих pps в бридж домене    
    print('%s input_pps - %s'%(int1,int1_input_pps))
    print('%s output_pps - %s'%(int2,int2_output_pps))
    print('%s output_pps - %s'%(int3,int3_output_pps))
    return(int1_input_pps,int2_output_pps, int3_output_pps)

#Вспомогательная функция для проверки параметров input_bitrate и output_bitrate на интерфейсе (используется в тесте test_flooding_mac_learn_disable)
def check_int_bitrate(ip,login,password,int1,int2,int3):
#    print('Старт процедуры проверки check_int_rate на %s %s %s\r'%(int1,int2,int3)) # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
    time.sleep(30)   # Ждем пока накопится статистика на интерфейсах чем больше ждем тем больше вероятность того что assert условие выполнится
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    cmd=('show interface %s'%int1)
    conn.execute(cmd) # Смотрим счетчики интерфейса int1 
    resp1 = conn.response
    allure.attach(resp1, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)     
#    print('Output of command  - %s'%resp1)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces ....'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces' c шаблоном в файле parse_show_subinterface_counters.txt 
    template1 = open('./templates/parse_show_subinterface_counters.txt') 
    fsm1 = textfsm.TextFSM(template1)
    processed_result1=fsm1.ParseTextToDicts(resp1)
#    result1 = fsm1.ParseText(resp1)
#    print(processed_result1)   # Раскомментируй, если хочешь посмотреть результат парсинга
    if len(processed_result1) != 0:
        if 'input_rate' in processed_result1[0]: # Это обработка исключения - list index out of range
            int1_input_bitrate = processed_result1[0]['input_rate']
        else:
            int1_input_bitrate = 0

        if 'output_rate' in processed_result1[0]:
            int1_output_bitrate = processed_result1[0]['output_rate']
        else:
            int1_output_bitrate = 0
    else:
        int1_input_bitrate = 0
        int1_output_bitrate = 0


    cmd =('show interface %s'%int2)
    conn.execute(cmd) # Смотрим счетчики интерфейса int2 
    resp2 = conn.response
    allure.attach(resp2, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)     
#    print('Output of command  - %s'%resp1)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces ....'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces' c шаблоном в файле parse_show_subinterface_counters.txt 
    template2 = open('./templates/parse_show_subinterface_counters.txt') 
    fsm2 = textfsm.TextFSM(template2)
#    result2 = fsm2.ParseText(resp2)
    processed_result2=fsm2.ParseTextToDicts(resp2)
#    print(processed_result2)   # Раскомментируй, если хочешь посмотреть результат парсинга

    if len(processed_result2) != 0:
        if 'input_rate' in processed_result2[0]: # Это обработка исключения - list index out of range
            int2_input_bitrate = processed_result2[0]['input_rate']
        else:
            int2_input_bitrate = 0

        if 'output_rate' in processed_result2[0]:
            int2_output_bitrate = processed_result2[0]['output_rate']
        else:
            int2_output_bitrate = 0
    else:
        int2_input_bitrate = 0
        int2_output_bitrate = 0


    cmd =('show interface %s'%int3)
    conn.execute(cmd) # Смотрим счетчики интерфейса int3 
    resp3 = conn.response
    allure.attach(resp3, 'Вывод команды %s'%cmd, attachment_type=allure.attachment_type.TEXT)     
#    print('Output of command  - %s'%resp1)  # Раскомментируй, если хочешь посмотреть вывод команды 'show interfaces ....'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces' c шаблоном в файле parse_show_subinterface_counters.txt 
    template3 = open('./templates/parse_show_subinterface_counters.txt') 
    fsm3 = textfsm.TextFSM(template3)
#    result3 = fsm3.ParseText(resp3)
    processed_result3=fsm3.ParseTextToDicts(resp3)

    if len(processed_result3) != 0:
        if 'input_rate' in processed_result3[0]: # Это обработка исключения - list index out of range
            int3_input_bitrate = processed_result3[0]['input_rate']
        else:
            int3_input_bitrate = 0

        if 'output_rate' in processed_result3[0]:
            int3_output_bitrate = processed_result3[0]['output_rate']
        else:
            int3_output_bitrate = 0
    else:
        int3_output_bitrate = 0
        int3_input_bitrate = 0
#    print(processed_result3)   # Раскомментируй, если хочешь посмотреть результат парсинга


# раскомментируй 3 принта ниже, если хочешь увидеть результаты входящего и исходящего bitrate-a интерфейсов в бридж домене    
    # print('%s input_bitrate - %s ,output_bitrate - %s'%(int1,int1_input_bitrate,int1_output_bitrate))
    # print('%s input_bitrate - %s ,output_bitrate - %s'%(int2,int2_input_bitrate,int2_output_bitrate))
    # print('%s input_bitrate - %s ,output_bitrate - %s'%(int3,int3_input_bitrate,int3_output_bitrate))
    conn.send('quit\r')
    conn.close()
    return(int1_input_bitrate,int1_output_bitrate,int2_input_bitrate,int2_output_bitrate,int3_input_bitrate, int3_output_bitrate)




def estimate_time_Full_View_loading(ip, login, password, bgp_neighbor, uptime):
# Данная процедура используются в тест-кейсах для оценки времени загрузки BGP Full View    
    print('Старт процедуры оценки времени на %s\r'%ip) # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
    resp = ''
    conn = Telnet()
    acc = Account(login , password)
    allure.step('Подключаемся к маршрутизатору ME по протоколу telnet')
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('clear bgp neighbor %s'%bgp_neighbor)
    conn.execute('terminal datadump')
    #time.sleep(120)
    time.sleep(60) # Временно для решения задчи 239019 уменьшил время со 120 до 60 сек 
    prfx1=0
    delta=11
    while (delta > 1) :

        conn.execute('show bgp neighbors %s'%bgp_neighbor)
        resp=conn.response
        template = open('./templates/parse_show_bgp_neighbors.txt') 
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
#        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        neighbor_state=result[0][3]
        if neighbor_state == 'established':    
            uptime2=int(result[0][6])
            uptime3=int(result[0][7])
            uptime = (uptime2*60)+uptime3  #Вычисляем uptime в секундах, чтобы передать его в родительский процесс 
            prfx2 = int(result[0][8])
            delta = prfx2-prfx1  # Вычисляем на сколько увеличилось кол-во полученных маршрутов через bgp peer    
            print('Уже получено префиксов - %d, прирост - %d Uptime - %d\r'%(prfx2, delta, uptime))
            prfx1=prfx2
            time.sleep(5)
        else :
            uptime = 999  # Если neighbor_state не имеет статус 'established', то делаем uptime = 999 сек чтобы гарантировано вызвать assert
            delta =0  # Надо выходить из бесконечного цикла..... :) 
    if (prfx1 < 796000)&(neighbor_state == 'established'):
        uptime = 1000  # Если количество полученных маршрутов меньше чем приблизительно BGP Full View, сделаем uptime 1000 сек чтобы гарантированно вызвать assert 
    print('Завершение процедуры оценки времени загрузки\r')
    conn.send('quit\r')        
    conn.close()
    return(uptime,prfx1)

def generate_trafic_from_labs01(ip, packets_count,packets_size,login, password, dst_ip, result_loss):
    try:
        print('Старт процедуры генерации трафика\r') # раскомментируй если нужно убедиться, что функция запускается параллельно с другими 
        resp = ''
        conn = Telnet()
        acc = Account(login , password)
        allure.step('Подключаемся к коммутатору LABS01 по протоколу telnet')
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('ping %s timeout 50 size %s count %s'%(dst_ip,packets_size,packets_count)) # Генерим 'packets_count' в сторону dst_ip 
        resp = conn.response
        allure.attach(resp)
#        print('Output of command  - %s'%resp)  # Раскомментируй, если хочешь посмотреть вывод команды 'ping'
# C помощью магии модуля textFSM сравниваем вывод команды 'show interfaces tengigabitethernet 0/1/5.20010' c шаблоном в файле parse_show_inerface_counters.txt 
        template = open('./templates/parse_ping_from_mes.txt') 
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(resp)
        print(result)   # Раскомментируй, если хочешь посмотреть результат парсинга
        result_loss = result[0][0]
        print('Процедура генерации трафика окончена')
        conn.close()
        return(result_loss)
    except:
        sys.exit('Получен сигнал')




#Функция запускающая iperf сервер и клиент в контейнерах

def start_docker_iperf3_server_client(server_ip, duration, bandwidth,  result_loss, packet_send, packet_recv, docker_compose_file):
    with allure.step('Запускаем сервер iperf'):
        services = subprocess.Popen(f'arg1=%s arg2=%s arg3=%s docker-compose -f tools/docker/iperf/%s up'%(server_ip,duration,bandwidth,docker_compose_file),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    time.sleep(duration)
    return(100,100,0)



def start_docker_iperf3_server_client_queue(server_ip, duration, bandwidth,  result_loss, packet_send, packet_recv, docker_compose_file,q):
    q.put(0)
    q.put(0)
    q.put(0)
#    q.put('')
    try: 
        start_traffic_time=time.time()  # Фиксируем время начала генерации трафика
        start_traffic_time_struct=time.localtime(start_traffic_time)
        print("\r %s Пытаемся запустить docker c iperf-ом \r"%(time.strftime('%H:%M:%S',start_traffic_time_struct)))
        services = subprocess.Popen(f'arg1=%s arg2=%s arg3=%s docker-compose -f tools/docker/iperf/%s up'%(server_ip,duration,bandwidth,docker_compose_file),            
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        time.sleep(duration) # Обязательно нужна эта задержка чтобы долждаться завершения работы iperf-a в параллельном процессе
        output, error = services.communicate()
    except subprocess.CalledProcessError as error:
        print("\rВ docker-compose что-то пошло не так! Код завершения -%d %s %s\r"%(services.returncode, output, error))
        self.isCommandExecutionSuccessful = False
        errorMessage = ">>> Error while executing:\n"\
                       + command\
                       + "\n>>> Returned with error:\n"\
                       + str(error.output)
        self.textEdit_CommandLineOutput.append(errorMessage)

        QMessageBox.critical(None,
                             "ERROR",
                             errorMessage)
        print("Error: " + errorMessage)
    stop_traffic_time=time.time()  # Фиксируем время начала генерации трафика
    stop_traffic_time_struct=time.localtime(stop_traffic_time)

    print("\r %s Завершение работы процедуры iperf c кодом - %d\r"%(time.strftime('%H:%M:%S',stop_traffic_time_struct),services.returncode))
    q.get()
    q.get()
    q.get()
#    q.get()
    q.put(services.returncode)
    q.put(start_traffic_time)
    q.put(stop_traffic_time)
#    q.put(net_unreachable)


# Вспомогательная функция в которой локализуется индекс словаря в списке словарей образованных после парсинга с помощью метода ParseTextToDicts()
def locate_index_in_ListOfDict(ListOfDict, Searched_Key, Searched_Value, located_index): # ListOfDict это processed_result; Serched_Key - это имя ключа по которому будем искать(Например lsp_name); Searched_Value это значение у Searched_Key   
    i = 0
    located_index = 999 # Если это значение вернётся в вызывающий процедуру тест, то в тесте появится возможность обработки ситуации когда по ключу не удалось найти индекс 
    while i < len(ListOfDict):
        if ListOfDict[i][Searched_Key] == Searched_Value:
            print ('Ура! Нашлось в %s-м словаре парсинга'%i)
            located_index=i
        i = i + 1
    return(located_index)


# Вспомогательная функция в которой локализуется индекс словаря в списке словарей образованных после парсинга с помощью метода ParseTextToDicts() ПО двум параметрам
# ListOfDict это processed_result; Serched_Key1 - это имя ключа по которому будем искать(Например lsp_name); Searched_Value1 это значение у Searched_Key1
# Serched_Key2 - это имя ключа по которому будем искать(Например lsp_name); Searched_Value2 это значение у Searched_Key2  
def locate2_index_in_ListOfDict(ListOfDict, Searched_Key1, Searched_Value1, Searched_Key2, Searched_Value2, located_index_list): 
    i = 0
    located_index = 999 # Если это значение вернётся в вызывающий процедуру тест, то в тесте появится возможность обработки ситуации когда по ключу не удалось найти индекс
    while i < len(ListOfDict):
        if (ListOfDict[i][Searched_Key1] == Searched_Value1) and (ListOfDict[i][Searched_Key2] == Searched_Value2):
            print ('Ура! Нашлось в %s-м словаре парсинга'%i)
            located_index=i
        i = i + 1
    return(located_index)


def read_logs ():
    with open ('./function_test_cron.log','r') as f:
        data = f.read()
        selected_tests='0'
# Ищем в файле количество собранных тестов (collecting ... collected 303 items) перед выполнением тестов
        str1=data.partition('Общее количество тестов - ')
        str2=str1[2].partition('.')
        total_tests=str2[0]
        print('Общее количество обнаруженных тестов  - %s\r'%total_tests)
# Ищем в файле количество успешных тестов
        str1=data.partition('Общее количество PASSED тестов - ')
        str2=str1[2].partition('.')
        passed_tests=str2[0]
# Ищем в файле количество выбранных тестов
        str1=data.partition('Общее количество SELECTED тестов - ')
        str2=str1[2].partition('.')
        selected_tests=str2[0]
# Ищем в файле количество НЕ успешных тестов
        str1=data.partition('Общее количество FAILED тестов - ')
        str2=str1[2].partition('.')
        failed_tests=str2[0]
# Ищем в файле количество пропущенных тестов
        str1=data.partition('Общее количество SKIPPED тестов - ')
        str2=str1[2].partition('.')
        skipped_tests=str2[0]
# Ищем в файле количество сломанных тестов
        str1=data.partition('Общее количество ERROR тестов - ')
        str2=str1[2].partition('.')
        error_tests=str2[0]

        
        print('Количество выбранных тестов - %s\r'%selected_tests)
        print('Количество успешных тестов в логах - %s\r'%passed_tests)
#Ищем в файле версию ПО
# Ищем в файле версию ПО на atDR1
        #str1=data.partition('Eltex ME5000 carrier router running Network OS for ME5k ver. ')
        str1=data.partition('Eltex ME5000 ')
        #str2=str1[2].partition('(')
        str2=(str1[2].partition('ver.'))[2].partition('(')
        Router_version_me5000=str2[0]
        str1=data.partition('Eltex ME2001 ')
        str2=(str1[2].partition('ver.'))[2].partition('(')
        Router_version_ME2001=str2[0]
        str1=data.partition('Eltex ME5200 ')
        str2=(str1[2].partition('ver.'))[2].partition('(')
        Router_version_me5200=str2[0]  
      
        str1=data.partition(' успешно завершено на маршрутизаторе')
        str2=str1[0].partition('версии')
        SOFT_version=str2[2]
        if SOFT_version=='':
           str1=data.partition(' уже')
           str2=str1[0].partition('Версия ')
           SOFT_version=str2[2]  







# Ищем в файле uptime маршуртизатора atDR1
        str1=data.partition('Router 192.168.17.146 has system Uptime:')
        str2=str1[2].partition('end_of_uptime')
        Router_SysUptime=str2[0]

        if Router_SysUptime=='':
            str1=data.partition('Router 192.168.17.138 has system Uptime:')
            str2=str1[2].partition('end_of_uptime')
            Router_SysUptime=str2[0]

        if Router_SysUptime=='':
            str1=data.partition('Router 192.168.17.139 has system Uptime:')
            str2=str1[2].partition('end_of_uptime')
            Router_SysUptime=str2[0]

        #return(total_tests, passed_tests, selected_tests, Router_version, Router_SysUptime, skipped_tests)
        return(total_tests, passed_tests, selected_tests, Router_version_me5000, Router_version_ME2001, Router_version_me5200, SOFT_version, Router_SysUptime, skipped_tests, error_tests)



# Процедура по оптимизации перезагрузок DUT-ов при необходимости сменить конфигурацию hw-module
def check_alarm_then_reload(ip, hostname, login, password, booting_timer):
    conn = Telnet()
    acc = Account(login , password)
    conn.connect(ip)
    conn.login(acc)
    conn.set_prompt('#')
    conn.execute('terminal datadump')
    conn.execute('show alarm')
    resp=conn.response
    alarm = resp.find('System has an unapplied configuration')    
    if (alarm != -1):
        conn.set_prompt('[n]')
        conn.execute('reload system')
        conn.execute('y\r')
        print ('\nМаршрутизатор %s отправлен в перезагрузку для примения параметров hw-module'%hostname)
        conn.close()
        print('\nЖдем %d секунд и пытаемся подключиться к маршрутизатору %s для проверки hw-module параметров'%(booting_timer,hostname))
        time.sleep(booting_timer)
        conn2 = Telnet()
        acc2 = Account(login, password)
        conn2.connect(ip)
        conn2.login(acc2)
        conn2.set_prompt('#')
        conn2.execute('terminal datadump')
        conn2.execute('show alarm')
        resp2=conn2.response
        print("\n*************Вывод команды show alarm после перезагрузки*********************")
        print(resp2)
        print("\n*****************************************************************************")
        conn2.close()


def clean_output(output, sub):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    output = ansi_escape.sub('', output)

    start_index = output.rfind(sub)
    if start_index != -1:
        return output[start_index:]
    else:
        return 'Подстрока не найдена'
