from configs.config_me import *
from configs.config_cisco import *
from configs.config_jun import *
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
from driver import ME5000CliDriver
from driver import MES5324CliDriver

with open ('./hardware_set.json') as f:
    templates = json.load(f)
    hardware_set_id = templates["hardware_set_id"]
    other_vendor = templates["other_vendor"]

if other_vendor == "cisco":
    with open (f'./tftpd/{hardware_set_id}/config.json') as f:
        templates = json.load(f)
        DUT1 = setting_ME("DUT1",templates,hardware_set_id)
        DUT2 = setting_ME("DUT2",templates,hardware_set_id)
        DUT3 = setting_ME("DUT3",templates,hardware_set_id)
        DUT4 = setting_Cisco("DUT4",templates,hardware_set_id)
elif other_vendor == "vmx":
    with open (f'./tftpd/{hardware_set_id}/config.json') as f:
        templates = json.load(f)
        DUT1 = setting_ME("DUT1",templates,hardware_set_id)
        DUT2 = setting_ME("DUT2",templates,hardware_set_id)
        DUT3 = setting_ME("DUT3",templates,hardware_set_id)
        DUT4 = setting_vMX("DUT4",templates,hardware_set_id)

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