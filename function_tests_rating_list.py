import smtplib
import textwrap
from conftest import *
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from dateutil.relativedelta import relativedelta
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

mydb = mysql.connector.connect(   # Подключаемся к mysql базе function_test_stat_db
    host='192.168.16.89',
	user='alex',
	password='!QAZ2wsx4',
	database='function_test_stat_db'
)

month_ago = datetime.now() - relativedelta(months=1)

mycursor = mydb.cursor()
sql = (
            "select  row_number() over (order by avg(test_result)) id,test_name,  avg(test_result)*100,count(*), SUBSTRING_INDEX(SUBSTRING_INDEX(param_list, ',', 1), '/tftpd/', -1) from function_tests_detail_info where date>'%s' and hardware_set_id=%s group by SUBSTRING_INDEX(SUBSTRING_INDEX(param_list, ',', 1), '/tftpd/', -1), test_name  order by avg(test_result) asc;" % (
        month_ago, hardware_set_id))
mycursor.execute(sql)
myresult = mycursor.fetchall()

column_width = [10, 70, 25, 25, 45]
headers = ["№", "Имя теста", "% успешности", "Тестирований за 30 дней", "Параметры"]


# Функция для переноса текста внутри ячейки
def wrap_text(text, width):
    return "\n".join(textwrap.wrap(str(text), width, break_long_words=True, break_on_hyphens=True))


wrapped_data = [[wrap_text(str(cell), width) for cell, width in zip(row, column_width)] for row in myresult]
wrapped_headers = [wrap_text(header, width) for header, width in zip(headers, column_width)]
e_mail_body_text = tabulate(wrapped_data, headers=wrapped_headers, tablefmt="simple")

txt_filename = "test_rating.txt"
with open(txt_filename, "w", encoding="utf-8") as f:
    f.write(e_mail_body_text)

# Столбчатая диаграмма статистики тестов за последние 10 дней
query_10 = """
    SELECT rating_date, green_tests, yellow_tests, red_tests
    FROM function_tests_rating_info
    WHERE hardware_set_id = 52
    ORDER BY rating_date DESC
    LIMIT 10
"""
mycursor.execute(query_10)
data = mycursor.fetchall()
df = pd.DataFrame(data, columns=['rating_date', 'green_tests', 'yellow_tests', 'red_tests'])
df['rating_date'] = pd.to_datetime(df['rating_date'])
df.set_index('rating_date', inplace=True)

# Построение столбчатой диаграммы
ax_10 = df.plot(kind='barh', stacked=True, figsize=(11, 6), color=['green', 'yellow', 'red'])
plt.ylabel('Дата')
plt.xlabel('Количество тестов')
plt.title('Статистика успешности выполнения тестов за последние 10 дней')
plt.xticks(rotation=45)
plt.legend(loc='best', title='Тип тестов')
plt.grid(axis='y', linestyle='--', alpha=0.7)

for container in ax_10.containers:
    ax_10.bar_label(container, fmt='%.0f', label_type='center', fontsize=10, color='black')

plt.savefig("bar_chart_10.png", dpi=300, bbox_inches='tight')

# Линейный график статистики тестов за последние 30 дней
query_30 = """
    SELECT rating_date, green_tests, yellow_tests, red_tests
    FROM function_tests_rating_info
    WHERE hardware_set_id = 52
    ORDER BY rating_date DESC
    LIMIT 30
"""
mycursor.execute(query_30)
data = mycursor.fetchall()
df = pd.DataFrame(data, columns=['rating_date', 'green_tests', 'yellow_tests', 'red_tests'])
df['rating_date'] = pd.to_datetime(df['rating_date'])
df.set_index('rating_date', inplace=True)

# Построение линейного графика
ax_30 = df.plot(figsize=(12, 6), color=['green', 'yellow', 'red'], marker='o')
plt.xlabel('Дата')
plt.ylabel('Количество тестов')
plt.title('Статистика успешности выполнения тестов за последний месяц')
plt.xticks(rotation=45)
plt.legend(loc='best', title='Тип тестов')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig("linear_graph_30.png", dpi=300, bbox_inches='tight')

mycursor.close()
mydb.close()

fromaddr = 'information@avtotest.loc'
toaddr = 'information@avtotest.loc'
cc = "a.pryahin@avtotest.loc,d.babenko@avtotest.loc,a.dolmatova@avtotest.loc,i.makarenko@avtotest.loc,y.nikulina@avtotest.loc"
rcpt = cc.split(",") + [toaddr]

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Рейтинг выполнения тестов на стенде Group 2 за 30 дней"

files = ['linear_graph_30.png', 'bar_chart_10.png', 'test_rating.txt']

for filename in files:
    if os.path.isfile(f'{filename}'):
        attachment = open(f'{filename}', "rb")
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
