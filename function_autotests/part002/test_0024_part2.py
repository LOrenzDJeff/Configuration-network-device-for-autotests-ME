from conftest import *
from Exscript.util.start import start
from tabulate import tabulate

gl_response = None


def show_proc_cpu(job, host, conn):
    conn.execute('terminal datadump')
    conn.execute('show process cpu')
    global gl_response
    gl_response = conn.response


def connect_DUT(ip, username, password, job_function):
    try:
        start(Account(username, password), f"telnet://{ip}", job_function)
        return gl_response
    except Exception as e:
        print(e)
        return None


@pytest.mark.part2
@allure.feature('02:Функции управления и базовые show-команды')
@allure.story('2.010:Проверка session-limit для telnet/ssh, show processes memory и show process cpu')
@allure.title('В данном тесте проверяется show process cpu')
@pytest.mark.dependency(depends=["load_config002_dut1", "load_config002_dut2", "load_config002_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_process_cpu_part2(DUT):
    connect_DUT(DUT.host_ip, DUT.login, DUT.password, show_proc_cpu)
    output = gl_response
    assert output is not None, 'Пустой вывод команды show processes memory'
    allure.attach(output, 'Вывод команды show process cpu', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_process_cpu.txt') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(output)
    # print('\n', tabulate(result, headers=fsm.header)) # Полученный вывод команды после парсинга
    assert len(result) > 0, 'Парсинг вывода команды вернул пустой результат'

    clean_result = [[item.strip() for item in sublist] for sublist in result]
    for row in clean_result:
        if row[-1] == 'pp-manager' or row[-1] == 'dcsi':
            assert float((row[0])[:-1]) <= 70, f'Процесс {row[-1]} вышел за пределы границы 70% со значением {row[0]}'
            assert float((row[1])[:-1]) <= 60, f'Процесс {row[-1]} вышел за пределы границы 60% со значением {row[1]}'
            assert float((row[2])[:-1]) <= 50, f'Процесс {row[-1]} вышел за пределы границы 50% со значением {row[2]}'
        else:
            assert float((row[0])[:-1]) <= 20, f'Процесс {row[-1]} вышел за пределы границы 20% со значением {row[0]}'
            assert float((row[1])[:-1]) <= 15, f'Процесс {row[-1]} вышел за пределы границы 15% со значением {row[1]}'
            assert float((row[2])[:-1]) <= 10, f'Процесс {row[-1]} вышел за пределы границы 10% со значением {row[2]}'
