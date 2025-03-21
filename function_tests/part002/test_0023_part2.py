from conftest import *
from Exscript.util.start import start
from tabulate import tabulate

gl_response = None


def show_proc_mem(job, host, conn):
    conn.execute('terminal datadump')
    conn.execute('show processes memory')
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
@allure.title('В данном тесте проверяется show processes memory')
@pytest.mark.dependency(depends=["load_config002_dut1", "load_config002_dut2", "load_config002_dut3"], scope='session')
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1), 
 			 pytest.param(DUT2), 
 			 pytest.param(DUT3)
			]
			)
def test_show_processes_memory_part2(DUT):
    connect_DUT(DUT.host_ip, DUT.login, DUT.password, show_proc_mem)
    output = gl_response
    assert output is not None, 'Пустой вывод команды show processes memory'
    allure.attach(output, 'Вывод команды show processes memory', attachment_type=allure.attachment_type.TEXT)

    with open('./templates/parse_show_processes_memory.txt') as template:
        fsm = textfsm.TextFSM(template)
        result = fsm.ParseText(output)
    # print('\n', tabulate(result, headers=fsm.header)) # Полученный вывод команды после парсинга
    assert len(result) > 0, 'Парсинг вывода команды вернул пустой результат'

    clean_result = [[item.strip() for item in sublist] for sublist in result]
    for row in clean_result:
        if row[1] == 'pp-manager' or row[1] == 'dcsi':
            assert float(row[-1]) <= 25, f'Процесс {row[1]} вышел за пределы границы 25% со значением {row[-1]}'
        else:
            assert float(row[-1]) <= 5, f'Процесс {row[1]} вышел за пределы границы 5% со значением {row[-1]}'
