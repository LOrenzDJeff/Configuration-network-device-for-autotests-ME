import telnetlib
import time

#Управление Telnet-соединением
class TelnetManager:
    #Инициализация необходимых переменных
    def __init__(self, host, port, login, password):
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.tn = telnetlib.Telnet(self.host, self.port)

    #Установка соединения с устройством
    def connect(self):
        self.tn.write(b"\n")
        self.tn.read_until(b"login: ", timeout=30)
        self.tn.write(self.login.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ", timeout=30)
        self.tn.write(self.password.encode('ascii') + b"\n")
        self.tn.read_until(b"#", timeout=30)

    #Закрытие соединения
    def close(self):
        if self.tn:
            self.tn.write(b"quit\n")
            self.tn.close()