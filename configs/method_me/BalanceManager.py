#Настройка балансировки
class BalanceManager:
    #Инициализация необходимых переменных
    def __init__(self, connection):
        self.tn = connection
    
    #Установка hasg-fields
    def hash_field(self,type,direction):
        self.tn.write(b"config\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"load-balancing hash-fields " + type.encode('ascii') + b"-" + direction.encode('ascii') + b"\n")
        self.tn.write(b"commit\n")
        self.tn.read_until(b"(config)#", timeout=30)
        self.tn.write(b"end\n")
        self.tn.read_until(b"#", timeout=30)