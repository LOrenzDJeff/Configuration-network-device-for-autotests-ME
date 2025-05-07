# Подключение к учебным рутерам через консоль
Подключение осуществляется через учебный сервер 192.168.16.115
## Директива ссылок на usb-console
```bash
cd /home/pryahin/console/
pryahin@eve-ng-lab:~/console$ ls -l
total 0
lrwxrwxrwx 1 root root 12 апр 23 15:47 R1-G1 -> /dev/ttyUSB0
lrwxrwxrwx 1 root root 12 апр 23 15:50 R1-G2 -> /dev/ttyUSB4
lrwxrwxrwx 1 root root 12 апр 23 15:51 R1-G3 -> /dev/ttyUSB8
lrwxrwxrwx 1 root root 12 апр 23 15:48 R2-G1 -> /dev/ttyUSB1
lrwxrwxrwx 1 root root 12 апр 23 15:50 R2-G2 -> /dev/ttyUSB5
lrwxrwxrwx 1 root root 12 апр 23 15:51 R2-G3 -> /dev/ttyUSB9
lrwxrwxrwx 1 root root 12 апр 23 15:48 R4-G1 -> /dev/ttyUSB2
lrwxrwxrwx 1 root root 12 апр 23 15:50 R4-G2 -> /dev/ttyUSB6
lrwxrwxrwx 1 root root 13 апр 23 15:51 R4-G3 -> /dev/ttyUSB10
```
## Команда для подключения через minicom
Пример подключения к R1-G1
### Через корневую директиву
```bash
pryahin@eve-ng-lab:~$ sudo minicom -wD ./console/R1-G1
```
### Через репозиторий
```bash
pryahin@eve-ng-lab:~/autotests-v2$ sudo minicom -wD ../console/R1-G1
```