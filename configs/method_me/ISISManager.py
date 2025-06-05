class ISISManager:
    """Управление протоколами маршрутизации"""
    def __init__(self, connection, isis_config, loopback):
        self.conn = connection
        self.isis_config = isis_config
        self.loopback = loopback

    def configure_isis(self):
        """Базовая настройка ISIS"""
        self.conn.config_mode()
        self.conn.execute(b"router isis test", b"(config-isis)#")
        
        # Конфигурация интерфейсов
        # ...
        
        self.conn.execute(f"net {self.isis_config}".encode())
        self.conn.execute(b"exit")
        self.conn.commit()
        self.conn.exit_config()

    # Методы для BGP, статических маршрутов и т.д.
    # ...
