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
import telnetlib
from Exscript import Host, Account
from Exscript.protocols import Telnet, SSH2
from Exscript.protocols.exception import TimeoutException, InvalidCommandException
from easysnmp import Session
from threading import Thread
from hamcrest import *
from scapy.all import *
from pytest import approx
from driver import ME5000CliDriver
from driver import MES5324CliDriver
from jinja2 import Environment, FileSystemLoader


with open ('./hardware_set_G3.json') as f:
    templates = json.load(f)
    DUT1 = templates['DUT1']
    DUT2 = templates['DUT2']
    DUT3 = templates['DUT3']
    DUT4 = templates['DUT4']
    DUT5 = templates['DUT5']
    DUT6 = templates['DUT6']
    DUT7 = templates['DUT7']

ntp_server_ip = '192.168.16.89'

def locate_index_in_ListOfDict(ListOfDict, Searched_Key, Searched_Value, located_index): # ListOfDict это processed_result; Serched_Key - это имя ключа по которому будем искать(Например lsp_name); Searched_Value это значение у Searched_Key   
    i = 0
    located_index = 999 # Если это значение вернётся в вызывающий процедуру тест, то в тесте появится возможность обработки ситуации когда по ключу не удалось найти индекс 
    while i < len(ListOfDict):
        if ListOfDict[i][Searched_Key] == Searched_Value:
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
     conn.set_driver(ME5000CliDriver())
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

def new_config(DUT,part):
    env = Environment(loader=FileSystemLoader(f'./jinja/{part}/{DUT}/'))
    template = env.get_template('startup-cfg-cli.j2')
    if DUT == DUT1['dir_hostname']:
        output = template.render(DUT1)
    elif DUT == DUT2['dir_hostname']:
        output = template.render(DUT2)
    elif DUT == DUT3['dir_hostname']:
        output = template.render(DUT3)
    elif DUT == DUT4['dir_hostname']:
        output = template.render(DUT4)
        with open(f'../tftp/{DUT}/startup-cfg-cli.txt', 'w') as f:
          f.write(output)
        return
    with open(f'../tftp/{DUT}/startup-cfg-cli', 'w') as f:
          f.write(output)

def me_reboot(ip,login,password,hostname):
    def ping_device(ip, event):
        while not event.is_set():
            response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE)
            #print(response) #Информация о пинге
            if response.returncode == 0:
                event.set()
            time.sleep(1)

    def reboot_device(ip, login, password, hostname, event):
        tn = telnetlib.Telnet(ip)

        tn.read_until(b"login: ", timeout=10)
        tn.write(login.encode('ascii') + b"\n")
        tn.read_until(b"Password: ", timeout=10)
        tn.write(password.encode('ascii') + b"\n")

        tn.read_until(b"#: ", timeout=10)
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
            print(f"{hostname} успешно перезагрузился за {elapsed_time:.2f} +- 90 секунд")
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
    reboot_thread = threading.Thread(target=reboot_device, args=(ip, login, password, hostname, event))
    reboot_thread.start()
    reboot_thread.join()

@pytest.fixture()
def cisco_init_configuration(ip, hostname, login, password, part):
    new_config(hostname,part)
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"login: ", timeout=10)
    tn.write(login.encode('ascii') + b"\n")
    tn.read_until(b"Password: ", timeout=10)
    tn.write(password.encode('ascii') + b"\n")
    tn.read_until(b"#", timeout=120)
    tn.write(b"config\n")
    tn.read_until(b"#", timeout=120)
    tn.write(b"load tftp://%s/%s/startup-cfg-cli.txt\n"%(DUT7['ip'].encode('ascii'), hostname.encode('ascii')))
    tn.read_until(b"#", timeout=120)
    tn.write(b'commit replace\n')
    tn.read_until(b'Do you wish to proceed? [no]:', timeout=120)
    tn.write(b'yes\n')
    tn.read_until(b"#", timeout=120)
    tn.close

@pytest.fixture()
def me_init_configuration(ip, hostname, login, password, part):
     new_config(hostname,part)
     for i in range(2):
        conn = Telnet()
        acc = Account(login, password)
        try:
            conn.connect(ip)
            # Пришлось указать этот драйвер т.к. после обновления ПО с 2.4.0 на 3.0.0 exscript стал принимать ME-шку за циску и пытаться выполнять команду 'enable'
            if DUT2['hostname'] == hostname or DUT3['hostname'] == hostname:
                conn.set_driver(ME5000CliDriver())
            conn.login(acc)
            conn.set_prompt('#')
            # Данная команда помогает избавиться от мусора который иногда переезжает из running-config в candidate-config
            conn.execute('clear candidate-config')
            #if "slave" in conn.response:
            #    con1 = Telnet()
            #    con1.connect(DUT9['host_ip'])
            #    con1.login(acc)
            #    con1.set_prompt('#')
            #    con1.execute('clear candidate-config')
            #    if "slave" in con1.response:
            #        print("DR1 в офлайне")
            #        me_reboot(ip, login, password, hostname)
            #    con1.send('quit\r')
            #    con1.close()
            #    print("FMC0 в офлайне, FMC1 включён")
            #    switchover(DUT9['host_ip'], login, password)
            #    continue
                
            # Копируем начальные конфигурации с tftp сервера для ME маршрутизаторов (Device Under Test - DUT)
            conn.set_prompt('#')
            #if hostname == DUT3['hostname']:
                # Согласно условию теста рутер atDR1 управляется outband, через VRF mgmt-intf
            conn.execute(f"copy tftp://{DUT7['ip']}/{hostname}/startup-cfg-cli fs://candidate-config vrf mgmt-intf")
            #elif hostname == DUT1['hostname']:
                # Согласно условию теста рутер atAR1 управляется inband, через VRF MGN
                #conn.execute(f"copy tftp://{DUT7['host_ip']}/{tftp_dir}/{part}/{hostname}/startup-cfg-cli fs://candidate-config vrf MGN")
            #elif hostname == DUT2['hostname']:
                # Согласно условию теста рутер atAR1 управляется inband, через GRT
                #conn.execute(f"copy tftp://{DUT7['host_ip']}/{tftp_dir}/{part}/{hostname}/startup-cfg-cli fs://candidate-config")

            conn.set_prompt('\[n\]')
            conn.execute('commit replace')
            conn.set_prompt('Commit successfully completed')
            conn.send('y\r')
            try:
                conn.execute('y')
            except:
                print("\rСработал блок except\r")
                resp=conn.response
                print('\rResp на execute y из except: %s\r'%resp)
                raise # Добавил команду чтобы фикстура генерировала Error в случае срабатывания exception
            conn.send('quit\r')
            conn.close()
            break
        except TimeoutException as e:
            if "(offline mode)" in str(e):
                me_reboot(ip, login, password, hostname)
                try:
                    os.makedirs("./tftpd/logs/%s"%part,exist_ok=True)
                    os.chmod("./tftpd/logs/%s"%part, 0o777)
                except OSError as error:
                    print('\rВозникла ошибка при создании папки для сбора логов -%s\r'%error)
                    os.chmod("./tftpd/logs/%s"%part, 0o777)
                con2 = Telnet()
                acc = Account(login, password)
                con2.connect(ip)
                con2.login(acc)
                con2.set_prompt('#')
                con2.execute('show tech-support')
                con2.set_prompt('#')
                if hostname==DUT2["hostname"]:
                    con2.execute('copy fs://logs tftp://%s/logs/%s/'%(DUT7['ip'],part))
                elif hostname==DUT3["hostname"]:
                    con2.execute('copy fs://logs tftp://%s/logs/%s/ vrf mgmt-intf'%(DUT7['ip'],part))
                elif hostname==DUT1["hostname"]:
                    con2.execute('copy fs://logs tftp://%s/logs/%s/ vrf MGN'%(DUT7['ip'],part))
                con2.send('quit\r')
                con2.close()
                if i == 1:
                    pytest.fail("Маршрутизатор был в оффлайн моде")
        except InvalidCommandException as e:
            pytest.fail(f"Ошибка в конфигурации:\n{str(e)}\n")
     yield

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


#new_config("atAR1",'part1')
#new_config("atAR2",'part1')
#new_config("atDR1",'part1')