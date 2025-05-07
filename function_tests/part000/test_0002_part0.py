from conftest import *

# Определяем устройства для обновления
devices = [DUT1, DUT2, DUT3]

# Группируем устройства по hardware, чтобы загружать файлы только один раз
hardware_versions = {}
for dut in devices:
    hardware = dut.hardware
    if hardware not in hardware_versions:
        hardware_versions[hardware] = dut.software


@allure.feature('Обновление ПО на МЕ маршрутизаторах')
@pytest.mark.part0
@pytest.mark.upgrade_software
def test_upgrade_me():
    # Запускаем обновление в потоках
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for dut in devices:
            path_version = '/tftp/'
            futures[dut.hostname] = executor.submit(me_software_upgrade, dut.host_ip, dut.login, dut.password,
                                                       dut.hostname, hardware_versions[dut.hardware], path_version,
                                                       int(dut.boot))

        # Ожидаем завершения всех обновлений
        for hostname, future in futures.items():
            future.result()
