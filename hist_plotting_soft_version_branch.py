import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from conftest import *

params = read_logs()  # Вызов процедуры которая читает логи из файла function_test_cron.log

software_version = params['soft_version']
soft_version_branch = re.search(r'\d+.\d+.\d+', software_version).group(0)
print(f'Ветка ПО - {soft_version_branch}\r')

mydb = mysql.connector.connect(  # Подключаемся к mysql базе function_test_stat_db
    host='192.168.16.89',
    user='alex',
    password='!QAZ2wsx4',
    database='function_test_stat_db'
)

# Код который заполняет таблицу function_tests_summary_info результатами проведенного тестирования
with open('hardware_set.json') as f:
    templates = json.load(f)
    hardware_set_id = templates['hardware_set_id']
mycursor = mydb.cursor()
sql = "select soft_version, avg(success_percent), count(soft_version), max(date) from function_tests_summary_info where soft_version LIKE '%" + soft_version_branch + "%' and hardware_set_id=" + hardware_set_id + " group by soft_version order by max(date) desc limit 20"
mycursor.execute(sql)
myresult = mycursor.fetchall()
version_list = []
success_percent_list = []
number_test_list = []
for x in myresult:
    version_list.append(x[0])
    success_percent_list.append(int(x[1]))
    number_test_list.append(x[2])

fig, ax = plt.subplots()
width = 0.75  # the width of the bars
ind = np.arange(len(success_percent_list))  # the x locations for the groups
ax.barh(ind, success_percent_list, width, color="blue")
ax.set_yticks(ind + width / 2)
ax.set_yticklabels(version_list, minor=False)
plt.title('Стенд Group № 2. Ветка %s, 20 тестируемых версий ' % soft_version_branch)
plt.xlabel('(кол-во тестов) средний % успешного выполнения')
plt.ylabel('Версии ПО')
# plt.show()

for i, v in enumerate(success_percent_list):
    plt.text(v - 5, i + .25, str(v) + '%', color='black', fontweight='bold')
#    plt.text(str(v) + 3, str(i) + .25, str(v), color='blue', fontweight='bold')
# plt.savefig(os.path.join('soft_version_branch.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures

for i, v in enumerate(number_test_list):
    plt.text(4, i - .2, '(' + str(v) + ')', color='red', fontweight='bold')
#    plt.text(str(v) + 3, str(i) + .25, str(v), color='blue', fontweight='bold')
plt.savefig(os.path.join('soft_version_branch.png'), dpi=300, format='png',
            bbox_inches='tight')  # use format='svg' or 'pdf' for vectorial pictures


def sendImage():
    Token = '7599542685:AAHaZn7wNbR1N5xt3oMFmfRArpE5sbaJ12w'
    url = "https://api.telegram.org/bot7599542685:AAHaZn7wNbR1N5xt3oMFmfRArpE5sbaJ12w/sendPhoto"
    #	files = {'photo': open('/home/pryakhin-alex/git/me5k/soft_version_branch.png', 'rb')}
    files = {'photo': open('./soft_version_branch.png', 'rb')}
    data = {'chat_id': "-4746074596"}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)


sendImage()
