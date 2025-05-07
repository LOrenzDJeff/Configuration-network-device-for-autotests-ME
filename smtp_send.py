import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from conftest import *

params = read_logs()  # процедура находится в conftest.py

fromaddr = 'information@avtotest.loc'
toaddr = 'information@avtotest.loc'
cc = "a.pryahin@avtotest.loc,d.babenko@avtotest.loc,a.dolmatova@avtotest.loc,i.makarenko@avtotest.loc,y.nikulina@avtotest.loc"
rcpt = cc.split(",") + [toaddr]

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Результаты выполнения автотестов Group №2"

success_percent = round((int(params['passed_tests']) / int(params['total_tests'])) * 100, 2)
body = (f"Выполнены функциональные тесты релиза {params['soft_version']}\r "
        f"Тесты выполнены на основе метода конфигурирования OOP\r "
        f"Версия ПО и Uptime на R1 - {params['R1v']}, {params['R1upt']}\r "
        f"Версия ПО и Uptime на R2 - {params['R2v']}, {params['R2upt']}\r "
        f"Версия ПО и Uptime на R4 - {params['R4v']}, {params['R4upt']}\r "
        f"Всего тестов - {params['total_tests']}\r "  
        f"Количество PASSED тестов - {params['passed_tests']}\r "
        f"Количество SELECTED тестов - {params['selected_tests']}\r "             
        f"Количество FAILED тестов - {params['failed_tests']}\r "             
        f"Количество SKIPPED тестов - {params['skipped_tests']}\r "
        f"Количество ERROR тестов - {params['error_tests']}\r "
        f"Доля успешного выполнения функционального тестирования - {success_percent}%\r"
        f"Отчет о тестировании функционала можно посмотреть по этой ссылке: - http://{DUT1.server['ip']}:33929\r"
        "Отчеты о тестировании за неделю:\r"
        f"Понедельник: http://{DUT1.server['ip']}:33921\r"
        f"Вторник:     http://{DUT1.server['ip']}:33922\r"
        f"Среда:       http://{DUT1.server['ip']}:33923\r"
        f"Четверг:     http://{DUT1.server['ip']}:33924\r"
        f"Пятница:     http://{DUT1.server['ip']}:33925\r"
        f"Суббота:     http://{DUT1.server['ip']}:33926\r"
        f"Воскресенье: http://{DUT1.server['ip']}:33927\r"
        "С уважением, система автотестов маршрутизаторов ME")

msg.attach(MIMEText(body, 'plain'))

files = ['function_test_cron.log', 'atAR1_console_output.log', 'atAR2_console_output.log', 'atDR1_console_output.log',
         'monitor_report_atAR1.txt', 'monitor_report_atAR2.txt', 'monitor_report_atDR1.txt']

# Прикладываем файлы логов выполнения автотестов и консольные логи с 3-х рутеров
for filename in files:
    if os.path.isfile(f'reports/{filename}'):
        attachment = open(f'reports/{filename}', "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

server = smtplib.SMTP('192.168.16.89', 587)
server.starttls()
server.login("information@avtotest.loc", "8D#2k473ej")
text = msg.as_string()
server.sendmail(fromaddr, rcpt, text)
server.quit()
