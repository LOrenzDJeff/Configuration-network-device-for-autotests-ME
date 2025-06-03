from conftest import *


@allure.epic('00:Загрузка начальной конфигурации')
@allure.feature('Часть 4.7')
@allure.story('Загрузка конфигурации на ME маршрутизатор')
@allure.title('Загрузка конфигурации на ME маршрутизатор')
@pytest.mark.part4_7
@pytest.mark.init_config4_7
@pytest.mark.parametrize("DUT",
			[
			 pytest.param(DUT1, marks=pytest.mark.dependency(name="load_config047_dut1",scope="session")) 
 			# pytest.param(DUT2, marks=pytest.mark.dependency(name="load_config047_dut2",scope="session")), 
 			 #pytest.param(DUT3, marks=pytest.mark.dependency(name="load_config047_dut3",scope="session"))
			]
			)

def test_me_init_config_upload_part4_7(DUT): 
	DUT.connection()
	DUT.startup()
	DUT.lacp()
	DUT.ipv4()
	DUT.loopback_ipv4()
	DUT.add_vrf("VRF40","100:40","100:40","100:40")
	DUT.lldp_agent_add()
	if DUT.hostname == DUT1.hostname:
		DUT.add_double_subint('te 0/0/11.10047', '100', '47', '192.168.47.1/24', 'VRF40')
		DUT.add_static("ipv4", "unicast", "192.168.168.47/32", "192.168.47.2", "VRF40")
		DUT.mpls_custom(DUT.neighor1['int_name'])
		DUT.ldp_add_custom(DUT.neighor1['int_name'])
		DUT.bgp_add_custom("65100", DUT.neighor2["loopback"], "ipv4 unicast", "VRF40")
		DUT.bgp_add_custom("65100", DUT.neighor2["loopback"], "vpnv4 unicast", "VRF40")
		DUT.bgp_add_redistribution("65100", "ipv4", "unicast", "1", "static", "redist_static", "VRF40")
		DUT.isis_add_custom(DUT.neighor1['int_name'])
	elif DUT.hostname == DUT2.hostname:
		DUT.add_double_subint('te 0/0/11.10042', '100', '42', '192.168.42.1/24', 'VRF40')
		DUT.add_static("ipv4", "unicast", "192.168.168.42/32", "192.168.42.2", "VRF40")
		DUT.mpls_custom(DUT.neighor3['int_name'])
		DUT.ldp_add_custom(DUT.neighor3['int_name'])
		DUT.bgp_add_custom("65100", DUT.neighor2["loopback"], "ipv4 unicast", "VRF40")
		DUT.bgp_add_custom("65100", DUT.neighor2["loopback"], "vpnv4 unicast", "VRF40")
		DUT.bgp_add_redistribution("65100", "ipv4", "unicast", "1", "static", "redist_static", "VRF40")
		DUT.isis_add_custom(DUT.neighor3['int_name'])
	DUT.close()