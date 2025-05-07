import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta
from conftest import *

mydb = mysql.connector.connect(  # Подключаемся к mysql базе function_test_stat_db
    host='192.168.16.89',
    user='alex',
    password='!QAZ2wsx4',
    database='function_test_stat_db'
)


# Данная функция парсит файл test_results.txt в котором содержатся детальные результаты тестов
def parse_test_results_txt_textfsm():
    with open('./test_results.txt', 'r') as f:
        file_context = f.read()
        # print(file_context)
        template = open('./templates/parse_function_tests_result.txt')
        fsm = textfsm.TextFSM(template)
        processed_result = fsm.ParseTextToDicts(file_context)
        #        print(processed_result)
        i = 0
        while i < len(processed_result):
            if processed_result[i]['passed_test_name'] != '':
                passed_test_name = processed_result[i]['passed_test_name']
                param_list = processed_result[i]['param_list']
                test_duration = processed_result[i]['duration']
                print('Успешный Тест № %d - %s, длительность - %s' % (i, passed_test_name, test_duration))
                sql_success = "insert into function_tests_detail_info (date, soft_version, hardware_set_id,test_name, test_result, param_list, assertion_error, duration) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)"
                #            	print(sql_success)
                value = (dt_string, params['soft_version'], hardware_set_id, passed_test_name, 1, param_list, 'None',
                         test_duration)
                my_cursor.execute(sql_success, value)
            if processed_result[i]['failed_test_name'] != '':
                except_test_name = processed_result[i]['failed_test_name']
                param_list = processed_result[i]['param_list']
                assert_cause = processed_result[i]['fail_test_cause']
                print('Провальный Тест №%d - %s,  Причина - %s' % (i, except_test_name, assert_cause))
                if len(assert_cause) > 254:
                    assert_cause = "UNKOWN: too long"  # Если assert слишком длинный - заменим его на строку "UNKOWN: too long"
                sql_except = "INSERT INTO function_tests_detail_info (date, soft_version,  hardware_set_id, test_name, test_result,  param_list, assertion_error, error_type) VALUES (%s, %s, %s, %s, %s, %s, %s, 'exception')"
                value = (
                dt_string, params['soft_version'], hardware_set_id, except_test_name, 0, param_list, assert_cause)
                my_cursor.execute(sql_except, value)
            if processed_result[i]['skipped_test_name'] != '':
                skipped_test_name = processed_result[i]['skipped_test_name']
                param_list = processed_result[i]['param_list']
                skip_cause = processed_result[i]['skip_test_cause']
                print('Пропущенный Тест №%d - %s. Причина - %s' % (i, skipped_test_name, skip_cause))
                if len(skip_cause) > 254:
                    skip_cause = "UNKOWN: too long"  # Если assert слишком длинный - заменим его на строку "UNKOWN: too long"
                sql_except = "INSERT INTO function_tests_detail_info (date, soft_version,  hardware_set_id, test_name, test_result,  param_list, assertion_error, error_type) VALUES (%s, %s, %s, %s, %s, %s, %s, 'skip')"
                value = (
                dt_string, params['soft_version'], hardware_set_id, skipped_test_name, 0, param_list, skip_cause)
                my_cursor.execute(sql_except, value)
            if processed_result[i]['error_test_name'] != '':
                error_test_name = processed_result[i]['error_test_name']
                param_list = processed_result[i]['param_list']
                error_cause = 'ERROR'
                print('Пропущенный Тест №%d - %s. Причина - %s' % (i, error_test_name, error_cause))
                sql_except = "INSERT INTO function_tests_detail_info (date, soft_version,  hardware_set_id, test_name, test_result,  param_list, assertion_error, error_type) VALUES (%s, %s, %s, %s, %s, %s, %s, 'error')"
                value = (
                dt_string, params['soft_version'], hardware_set_id, error_test_name, 0, param_list, error_cause)
                my_cursor.execute(sql_except, value)
            i = i + 1


now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

params = read_logs()  # Вызов процедуры которая читает логи из файла function_test_cron.log
soft_version = params['soft_version']
if params['R1v'] == params['R2v'] == params['R4v'] and DUT1.software == DUT2.software == DUT3.software:
    print(f"Soft version is {soft_version}\r")
else:
    soft_version = 'Inconsistent'
    print(f"Роутеры имеют разные версии. R1 - {params['R1v']}, R2 - {params['R2v']}, R4 - {params['R4v']}")

success_percent = round((int(params['passed_tests']) / int(params['total_tests'])) * 100, 2)

sys_uptime = params['R1upt']
weeks = days = hours = minutes = 0

find_weeks = re.search(r"(\d+) weeks, ", sys_uptime)
if find_weeks is not None:
    weeks = int(find_weeks.group(1))
find_days = re.search(r"(\d+) days, ", sys_uptime)
if find_days is not None:
    days = int(find_days.group(1))
find_hours = re.search(r"(\d+) hours, ", sys_uptime)
if find_hours is not None:
    hours = int(find_hours.group(1))
find_minutes = re.search(r"(\d+) minutes, ", sys_uptime)
if find_minutes is not None:
    minutes = int(find_minutes.group(1))

print(f'Недели - {weeks}\r')
print(f'Дни - {days}\r')
print(f'Часы - {hours}\r')
print(f'Минуты - {minutes}\r')

total_uptime_in_seconds = weeks * 604800 + days * 86400 + hours * 3600 + minutes * 60

# Заполнение таблицы function_tests_summary_info результатами проведенного тестирования
my_cursor = mydb.cursor()
sql = "INSERT INTO function_tests_summary_info (soft_version,hardware_set_id,total_tests,success_tests,success_percent,uptime,date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = (soft_version, hardware_set_id, params['total_tests'], params['passed_tests'], success_percent,
       total_uptime_in_seconds, dt_string)
my_cursor.execute(sql, val)
mydb.commit()
print(my_cursor.rowcount, "record inserted into table function_tests_summary_info.")

# Заполнение таблицы function_tests_detail_info результатами полученными при парсинге файла pytest.log
parse_test_results_txt_textfsm()
mydb.commit()
print(my_cursor.rowcount, "record inserted into table function_tests_detail_info.")
my_cursor.close()

# Заполнение таблицы function_tests_rating_info
mycursor = mydb.cursor(dictionary=True)
month_ago = datetime.now() - relativedelta(months=1)
sql = (
            "select  row_number() over (order by avg(test_result)) id,test_name,  avg(test_result)*100,count(*), SUBSTRING_INDEX(SUBSTRING_INDEX(param_list, ',', 1), '/tftpd/', -1) from function_tests_detail_info where date>'%s' and hardware_set_id=%s group by SUBSTRING_INDEX(SUBSTRING_INDEX(param_list, ',', 1), '/tftpd/', -1), test_name  order by avg(test_result) asc;" % (
    month_ago, hardware_set_id))
mycursor.execute(sql)
red_tests = 0
yellow_tests = 0
green_tests = 0
for row in mycursor:
    if float(row['avg(test_result)*100']) == 0:
        red_tests += 1
    if 1 <= float(row['avg(test_result)*100']) <= 75:
        yellow_tests += 1
    if float(row['avg(test_result)*100']) > 75:
        green_tests += 1
sql = (
    "INSERT INTO function_tests_rating_info (rating_date, hardware_set_id, green_tests, yellow_tests, red_tests) VALUES (%s, %s, %s, %s, %s);")
val = (datetime.now(), hardware_set_id, green_tests, yellow_tests, red_tests)
mycursor.execute(sql, val)
mydb.commit()
print(my_cursor.rowcount, "record inserted into table function_tests_rating_info.")
mycursor.close()
