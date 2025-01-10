from configs.old_config_me import *
from configs.old_config_jun import *
from configs.old_config_mes import *
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
