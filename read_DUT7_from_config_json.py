from conftest import *


# Данная функция нужна чтобы прочитать параметры определённого Device Under Test из файла config.json
def read_DUT_from_config_json(dut):
	with open ('hardware_set.json') as f:
		templates = json.load(f)
		DUT = templates[dut] # Сохраняем парамертры DUT из config.json в структуру
	return(DUT['ip'])



located_ip=read_DUT_from_config_json('DUT7') # Читаем параметры DUT7 чтобы узнать ip сервера на котором потом нужно будет запустить allure-отчет
print(located_ip) # таким образом в cron-файле не нужно будет явно указывать ip адрес где запускать отчет

