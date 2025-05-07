from conftest import *

now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

params = read_logs()  # Вызов процедуры которая читает логи из файла function_test_cron.log
print(f"Soft version is {params['soft_version']}\r")
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


# Отправляем данные по тестированию в Телеграм-канал
def telegram_bot_send_text(bot_message, bot_chat_id):
    bot_token = '7599542685:AAHaZn7wNbR1N5xt3oMFmfRArpE5sbaJ12w'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


""" 
	Уберём из сообщения информацию о Uptime т.к. по факту сейчас во время прогона тестов в разделе тестирования PBR 
    происходит перезагрузка рутеров чтобы применить изменённую конфигурацию
"""
bot_text = ("Функциональное тестирование завершено (OOP).\n"
f"Версия ПО на маршрутизаторах стенда №{hardware_set_id} - {params['soft_version']}\n"
f"Успешно выполнено тестов - {success_percent}% ({params['passed_tests']} из {params['total_tests']})\n"
"atDR1 содержит платы FMC32/LC20\n"
f"Отчет - http://{DUT1.server['ip']}:33929\n"
f"SKIPPED тестов - {params['skipped_tests']}\n"
f"FAILED тестов - {params['failed_tests']}\n"
f"ERROR тестов - {params['error_tests']}")


#   bot_chatID = '-453239384'  # Это chat-id группы ME-Avtotest
test = telegram_bot_send_text(bot_text, "-4746074596")
print(test)
