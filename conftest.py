from configs.config_me import *
from configs.config_jun import *
from configs.config_mes import *
import ipaddress
import json
import time
import pytest
import datetime
import requests
import urllib
import re
import subprocess
from bs4 import BeautifulSoup
import sys
import textfsm
from ttp import ttp
import allure
import time
import threading, queue
import concurrent.futures
import signal
import asn1
import os
import docker
import dockerpty
import logging
import paramiko
from Exscript import Host, Account
from Exscript.protocols import Telnet, SSH2
from Exscript.protocols.exception import TimeoutException
from easysnmp import Session
from threading import Thread
from hamcrest import *
from scapy.all import *
from pytest import approx

with open (f'hardware_set.json') as f:
     templates = json.load(f)
     DUT1 = setting_ME("DUT1",templates)
     DUT2 = setting_ME("DUT2",templates)
     DUT3 = setting_ME("DUT3",templates)
     DUT4 = setting_vMX("DUT4",templates)
     DUT5 = setting_MES("DUT5",templates)
     DUT6 = templates["DUT6"]
     hardware_set_id = templates['hardware_set_id']


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

def locate_index_in_ListOfDict(ListOfDict, Searched_Key, Searched_Value, located_index): # ListOfDict это processed_result; Serched_Key - это имя ключа по которому будем искать(Например lsp_name); Searched_Value это значение у Searched_Key   
    i = 0
    located_index = 999 # Если это значение вернётся в вызывающий процедуру тест, то в тесте появится возможность обработки ситуации когда по ключу не удалось найти индекс 
    while i < len(ListOfDict):
        if ListOfDict[i][Searched_Key] == Searched_Value:
            print ('Ура! Нашлось в %s-м словаре парсинга'%i)
            located_index=i
        i = i + 1
    return(located_index)

def show_version(ip, login, password):
    conn = Telnet()
    acc = Account(login, password)
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('show version')
        resp = conn.response
        conn.send('quit\r')
        allure.attach(resp, 'Вывод команды show version до обновления', attachment_type=allure.attachment_type.TEXT)
        with open('./templates/parse_show_version.txt', ) as template:
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseText(resp)
    except Exception as e:
        pytest.fail(f"Error in show_version: {e}")
    finally:
        if conn is not None:
            conn.close()

    return result[0][0]

def locate_download_link(vers, platform):
    # Формирует ссылку для загрузки ПО в зависимости от версии и платформы
    v_parts = vers.split('.')
    if len(v_parts) < 3:
        raise ValueError("Некорректный формат версии ПО")

    return f'https://validator.eltex.loc/checkerusers/me5k.jenkins/files/{".".join(v_parts[:3])}/firmware_{vers}.{platform}'

def check_software_after_reboot(ip, login, password, hostname, soft_version):
    conn = Telnet()
    acc = Account(login, password)
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_prompt('#')
        conn.execute('firmware confirm')
        conn.execute('show version')
        resp = conn.response
        conn.send('quit\r')
        allure.attach(resp, 'Вывод команды show version после обновления', attachment_type=allure.attachment_type.TEXT)
        assert resp.find(soft_version) != -1, f'Обновление ПО до версии {soft_version} на маршрутизаторе {hostname} не удалось'
        print(f'ПО на маршрутизаторе {hostname} успешно обновлено до версии {soft_version}')
    except OSError as osE:
        pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
    except Exception as e:
        pytest.fail(f"Error in execute_command: {e}")
    finally:
        if conn is not None:
            conn.close()

def download_software(ip, login, password, hostname, soft_version, platform, vrf):
    conn = Telnet()
    acc = Account(login, password)
    try:
        conn.connect(ip)
        conn.login(acc)
        conn.set_timeout(60)
        print(f'На маршрутизаторе {hostname} началась загрузка ПО...')
        conn.execute(f"copy tftp://{DUT1.server['ip']}/firmware_{soft_version}.{platform} fs://firmware {vrf}")
        conn.execute('firmware select alternate')
        conn.set_prompt('[n]')
        conn.execute('reload system')
        conn.execute('y\r')
        print(f'Маршрутизатор {hostname} отправлен в перезагрузку')
    except OSError as osE:
        pytest.fail(f"Failed to connect to the device via Telnet: {osE}")
    except Exception as e:
        pytest.fail(f"Error in download_software: {e}")
    finally:
        if conn is not None:
            conn.close()

def me_software_upgrade(ip, login, password, hostname, software_version, software_path, booting_timer):
    print(f'\nНачинаем процедуру обновления ПО на маршрутизаторе {hostname}')
    # Проверим текущую версию ПО
    current_version = show_version(ip, login, password)

    # Если версия уже актуальная, пропускаем обновление
    if current_version.find(software_version) != -1:
        print(f'{hostname} уже имеет актуальную версию ПО ({software_version}), обновление не требуется')
        return current_version

    # Определяем ссылку для загрузки
    platform = vrf = ''
    if hostname == DUT1.hostname:
        platform = DUT1.hardware
        vrf = 'vrf MGN'
    elif hostname == DUT2.hostname:
        platform = DUT2.hardware
        vrf = ''
    elif hostname == DUT3.hostname:
        platform = DUT3.hardware
        vrf = 'vrf mgmt-intf'
    download_link = locate_download_link(software_version, platform)

    # Загружаем файл ПО
    try:
        print(f"Скачиваем ПО с {download_link}")
        subprocess.call(["wget", download_link, "-q", "-N", "--no-check-certificate", "-P", software_path])
    except Exception as err:
        print(f"Ошибка при загрузке ПО: {err}")
        raise

    print(f'ПО {software_version} успешно загружено для {hostname}')

    # Загружаем ПО на устройство и перезагружаем
    download_software(ip, login, password, hostname, software_version, platform, vrf)

    # Ожидаем окончания обновления
    print(f'Ждем {booting_timer} секунд для завершения обновления {hostname}')
    time.sleep(booting_timer)

    # Проверяем версию после обновления
    check_software_after_reboot(ip, login, password, hostname, software_version)

    return software_version

def read_logs():
    report_params = [
        {'total_tests': '', 'passed_tests': '', 'selected_tests': '', 'failed_tests': '', 'skipped_tests': '',
         'error_tests': '', 'soft_version': '', 'R2v': '', 'R2upt': '', 'R4v': '', 'R4upt': '',
         'R1v': '', 'R1upt': ''}
    ]
    with open('./reports/function_test_cron.log', 'r', encoding='utf-8', errors='ignore') as log_file:
        data = log_file.read()

        total_tests = re.search(r"\s*Общее количество тестов - (\d+).", data).group(1)
        report_params[0]['total_tests'] = total_tests
        print(f'Общее количество тестов - {total_tests}\n')
        passed_tests = re.search(r"\s*Общее количество PASSED тестов - (\d+).", data).group(1)
        report_params[0]['passed_tests'] = passed_tests
        print(f'Общее количество PASSED тестов - {passed_tests}\n')
        selected_tests = re.search(r"\s*Общее количество SELECTED тестов - (\d+).", data).group(1)
        report_params[0]['selected_tests'] = selected_tests
        print(f'Общее количество SELECTED тестов - {selected_tests}\n')
        failed_tests = re.search(r"\s*Общее количество FAILED тестов - (\d+).", data).group(1)
        report_params[0]['failed_tests'] = failed_tests
        print(f'Общее количество FAILED тестов - {failed_tests}\n')
        skipped_tests = re.search(r"\s*Общее количество SKIPPED тестов - (\d+).", data).group(1)
        report_params[0]['skipped_tests'] = skipped_tests
        print(f'Общее количество SKIPPED тестов - {skipped_tests}\n')
        error_tests = re.search(r"\s*Общее количество ERROR тестов - (\d+).", data).group(1)
        report_params[0]['error_tests'] = error_tests
        print(f'Общее количество ERROR тестов - {error_tests}\n')


    with open('./reports/monitor_report_atAR1.txt', 'r') as mon_rep:
        data = mon_rep.read()
        version_R2 = re.search(r"\s*Версия ПО: (\S+)", data).group(1)
        report_params[0]['R2v'] = version_R2
        uptime_R2 = re.search(r"\s*Uptime: (.+)", data).group(1)
        report_params[0]['R2upt'] = uptime_R2
    with open('./reports/monitor_report_atAR2.txt', 'r') as mon_rep:
        data = mon_rep.read()
        version_R4 = re.search(r"\s*Версия ПО: (\S+)", data).group(1)
        report_params[0]['R4v'] = version_R4
        uptime_R4 = re.search(r"\s*Uptime: (.+)", data).group(1)
        report_params[0]['R4upt'] = uptime_R4
    with open('./reports/monitor_report_atDR1.txt', 'r') as mon_rep:
        data = mon_rep.read()
        version_R1 = re.search(r"\s*Версия ПО: (\S+)", data).group(1)
        report_params[0]['R1v'] = version_R1
        uptime_R1 = re.search(r"\s*Uptime: (.+)", data).group(1)
        report_params[0]['R1upt'] = uptime_R1

    if version_R2 != DUT1.software and version_R4 != DUT2.software and version_R1 != DUT3.software:
        soft_version = version_R2
    else:
        soft_version = DUT1.software
    report_params[0]['soft_version'] = soft_version

    return report_params[0]

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

def locate_index_in_ListOfDict(ListOfDict, Searched_Key, Searched_Value, located_index): # ListOfDict это processed_result; Serched_Key - это имя ключа по которому будем искать(Например lsp_name); Searched_Value это значение у Searched_Key   
    i = 0
    located_index = 999 # Если это значение вернётся в вызывающий процедуру тест, то в тесте появится возможность обработки ситуации когда по ключу не удалось найти индекс 
    while i < len(ListOfDict):
        if ListOfDict[i][Searched_Key] == Searched_Value:
            print ('Ура! Нашлось в %s-м словаре парсинга'%i)
            located_index=i
        i = i + 1
    return(located_index)

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

def locate2_index_in_ListOfDict(ListOfDict, Searched_Key1, Searched_Value1, Searched_Key2, Searched_Value2, located_index_list): 
    i = 0
    located_index = 999 # Если это значение вернётся в вызывающий процедуру тест, то в тесте появится возможность обработки ситуации когда по ключу не удалось найти индекс
    while i < len(ListOfDict):
        if (ListOfDict[i][Searched_Key1] == Searched_Value1) and (ListOfDict[i][Searched_Key2] == Searched_Value2):
            print ('Ура! Нашлось в %s-м словаре парсинга'%i)
            located_index=i
        i = i + 1
    return(located_index)

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
    
def connection_test(host_ip, login, password, part):
     conn = Telnet()
     acc = Account(login, password)
     #conn.set_driver(ME5000CliDriver())
     conn.connect(host_ip)
     if part == 'part2':
        conn.waitfor('Username:')
        resp = conn.response
        conn.login(acc)
        return resp + conn.response
     if part == 'part18':
        conn.login(acc)
        return conn.response
     
@pytest.fixture(scope='module')
def run_tacacs_server():
    with allure.step('Запускаем сервер tacacs'):
        services = subprocess.Popen('docker-compose -f tools/docker/tacacs/docker-compose.yaml up',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    time.sleep(25)
    yield
    with allure.step('Останавливаем сервисы'):
        subprocess.check_call('docker-compose -f tools/docker/tacacs/docker-compose.yaml down',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result, _ = services.communicate()
        allure.attach(result.decode(), 'Логи работы сервера tacacs')

def start_udp_esr_iperf3_server_client_queue(server_ip, duration, bandwidth, vrf_client):
    start_traffic_time=time.time()  # Фиксируем время начала генерации трафика
    start_traffic_time_struct=time.localtime(start_traffic_time)
    print("\r %s Пытаемся запустить iperf на esr \r"%(time.strftime('%H:%M:%S',start_traffic_time_struct)))

    tn = telnetlib.Telnet(DUT6["host_ip"])
    tn.read_until(b"login: ", timeout=10)
    tn.write(b"techsupport\n")
    tn.read_until(b"Password: ", timeout=10)
    tn.write(b"password\n")
    tn.read_until(b'$', timeout=10)
    tn.write(b"sudo ip netns exec %s iperf -c %s -u -P 15 -b %s -l 1000 -t %s\n"%(vrf_client.encode('ascii'),server_ip.encode('ascii'), bandwidth.encode('ascii'),str(duration).encode('ascii')))
    tn.read_until(b'Password:', timeout=10)
    tn.write(b"password\n")
    print("\r iperf на esr запустился \r")
    time.sleep(int(duration)) # Обязательно нужна эта задержка чтобы долждаться завершения работы iperf-a в параллельном процессе
    stop_traffic_time=time.time()  # Фиксируем время начала генерации трафика
    stop_traffic_time_struct=time.localtime(stop_traffic_time)

    print("\rЗавершение работы процедуры iperf")