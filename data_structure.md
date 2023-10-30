# Примеры структур данных, для методов библиотеки hostvmlib
###### Все структуры получены путем "ручного" создания объектов в приложении и последующих запросов (GET) методами библиотеки. 

- Создание аутентификатора **hostvmlib.create_auth(data)**
```
data = {
        "tags": [список тэгов],                                 # тэги
        "name": "наименование",                                 # наименование аутентификатора
        "priority": "приоритет",                                # приоритет
        "comments": ""           ,                              # комментарии
        "small_name": "",                                       # метка
        "host": "адрес сервера",                                # адрес сервера контроллера домена
        "port": "389 (636)",                                    # порт (несекурный/секурный)
        "ssl": False (True),                                    # использование шифрования SSL 
        "timeout": "10",                                        # таймаут подключения к серверу в секундах
        "username": "",                                         # "имя пользователя AD (LDAP), в виде uid= ,cn= ,dc= ,dc= ",
        "password": "",                                         # пароль
        "ldapBase": "",                                         # "базовый адрес поиска пользователей в каталоге AD (LDAP) в виде cn= ,dc= ,dc= ",
        "userClass": "posixAccount",                            # класс для пользователей домена
        "userIdAttr": "uid",                                    # аттрибут - идентификатор пользователя
        "userNameAttr": "uid",                                  # атррибут - имени пользователя
        "groupNameAttr": "memberOf",                            # аттрибут - имени группы
        "data_type": "RegexLdapAuthenticator#,                  # (типы аутентификаторов могут быть разные, как и параметры)",
        "altClass": "",                                         # класс для объектов домена, которые будут также проверены для поиска групп
        "visible": "True"                                       # признак видимости транспорта пользователям
}
```

- Создание групп в аутентификаторе **hostvmlib.create_internal_group(auth_name, data)**
```
auth_name = 'наименование аутентификатора'                      # наименование аутентификатора, куда добавляется группа
data = {
        "type": "group",                                        # тип группа
        "name": "наименование группы вида cn= ,dc= ,dc= ",      # наименование группы
        "comments": "комментарии",                              # комментарии
        "state": "A"                                            # статус - Включено (берется из документации или исходников OpenUDS)
} 
```

- Создание сервис-провайдера **hostvmlib.create_provider(data)**
```
data = {
    "id": "",                                                   # id сервис-провайдера (при создании всегда пустое!)
    "name": "наименование",                                     # наименование сервис-провайдера
    "tags": [список тэгов],                                     # тэги
    "comments": "коментарии",                                   # комментарии
    "type": "openNebulaPlatform (тип сервис-провайдера)",       # тип сервис-провайдера (берется из документации или исходников OpenUDS)
    "host": "адрес хоста сервис-провайдера",                    # адрес хоста сервера виртуализации
    "port": "порт",                                             # порт
    "ssl": False,                                               # использовать SSL
    "username": "пользователь",                                 # учетная запись на сервере виртуализации
    "password": "пароль",                                       # пароль
    "maxPreparingServices": "10",                               # максимальное количество одновременно создаваемых ВМ
    "maxRemovingServices": "5",                                 # максимальное количество одновременно удаляемых ВМ
    "timeout": "10"                                             # таймаут подключения к серверу виртуализации
    }
```

- Создание сервиса в сервис-провайдере **hostvmlib.create_service_in_provider(SP_name, data)**
```
SP_name = 'наименование существующего сервис-провайдера'
data = {
        "id": "",                                               # id сервиса (при создании всегда пустое!)
        "name": "наименование сервиса",                         # наименование сервиса
        "comments": "коментарий",                               # комментарии
        "data_type": "openNebulaLiveService (тип сервиса)",     # тип сервиса (берется из документации или исходников OpenUDS)
        "tags": [список тэгов],                                 # тэги
        "proxy_id": "-1",                                       # ???
        "baseName": "базовое имя",                              # имена машин (вида VM-VDI-)
        "lenName": "",                                          # максимальное количесвтво цифр, добавляемое к базовому имени 
                                                                # (если 2, то - VM-VDI-1 ... VM-VDI-99)
        "datastore": "id",                                      # id хранилица данных (в моем случае бралось напрямую из Open Nebula)
        "template": "id"                                        # id шаблона (в моем случае бралось напрямую из Open Nebula)
}
```

- Создание транспортов **hostvmlib.create_transport(data)**
```
# RDP Direct (классический RDP)
data = {
        "name": "наименование",                                 # наименование транспорта
        "type": "RDPTransport",                                 # тип транспорта
        "priority": 3,                                          # приоритет (чем больше, тем выше)
        "comments": "",                                         # коментарии
        "tags": [],                                             # тэги                          
        "nets_positive": True,                                  # сетевой доступ
        "allowed_oss": [],                                      # разрешенные устройства ???
        "useEmptyCreds": False,                                 # пропускать данные аккаунта
        "fixedName": "",                                        # не пусто - всегда используется как учетные данные
        "fixedPassword": "",                                    # не пусто - всегда используется как учетные данные
        "withoutDomain": False,                                 # без домена
        "fixedDomain": "",                                      # не пусто - всегда используется как учетные данные (DOMAIN\User)
        "allowSmartcards": False,                               # разрешить смарткарты
        "allowPrinters": True,                                  # разрешить принтеры
        "allowDrives": "true",                                  # хитрый параметр (да, именно в кавычках!):
                                                                #    'false'   -> 'Allow none'
                                                                #    'dynamic' -> 'Allow PnP drives'
                                                                #    'true'    -> 'Allow any drive'
        "enforceDrives": "",                                    # принудительное подключение дисков
        "allowSerials": True,                                   # разрешить серийные (serial) порты
        "allowClipboard": True,                                 # разрешить буфер обмена
        "allowAudio": True,                                     # включить звук
        "allowWebcam": True,                                    # включить вебкамеру
        "wallpaper": False,                                     # использовать обои
        "multimon": False,                                      # использовать несколько мониторов
        "aero": False,                                          # разрешить композицию рабочего стола
        "smooth": True,                                         # сглаживание шрифтов
        "showConnectionBar": True,                              # показывать окно подключения
        "credssp": True,                                        # ???
        "screenSize": "-1x-1",                                  # разрешение экрана (H x W), в случае -1x-1 - Full screen
        "colorDepth": "16",                                     # глубина цвета
        "alsa": True,                                           # Linux Client - использовать Alsa
        "multimedia": False,                                    # Linux Client - мультимедийная синхронизация
        "redirectHome": False,                                  # Linux Client - перенаправить домашнюю паку
        "printerString": "",                                    # Linux Client - строка принтера используемая с клиентом xfreerdp (проброс)
        "smartcardString": "",                                  # Linux Client - строка смарткарты, используемая с клиентом freerdp (проброс)
        "customParameters": ""                                  # Linux Client - пользователькие параметры используемые при подключении клиента
    }
```
```
# Структура данных для Tunneled RDP
    data = {
      "name": "наименование",                                   # наименование транспорта
      "priority": 2,                                            # приоритет (чем больше, тем выше)
      "comments": "",                                           # коментарии
      "tags": [],                                               # тэги
      "nets_positive": True,                                    # сетевой доступ
      "allowed_oss": [],                                        # разрешенные устройства ???
      "type": "TSRDPTransport",                                 # тип транспорта
      "tunnelServer": "URL-сервера:порт",                       # туннельный сервер
      "tunnelWait": "10",                                       # время ожидания туннеля
      "useEmptyCreds": False,                                   # пропустить данные аккаунта
      "fixedName": "",                                          # не пусто - всегда используется как учетные данные 
      "fixedPassword": "",                                      # не пусто - всегда используется как учетные данные
      "withoutDomain": False,                                   # без домена
      "fixedDomain": "",                                        # не пусто - всегда используется как учетные данные (DOMAIN/User)
      "allowSmartcards": True,                                  # разрешить смарткарты
      "allowPrinters": True,                                    # разрешить принтеры
      "allowDrives": "true",                                    # см. выше (помни! значение в кавычках!)
      "enforceDrives": "",                                      # принудительное подключение дисков
      "allowSerials": False,                                    # разрешить серийные (serial) порты
      "allowClipboard": True,                                   # разрешить буфер обмена
      "allowAudio": True,                                       # включить звук
      "allowWebcam": True,                                      # включить вебкамеру
      "wallpaper": False,                                       # использовать обои
      "multimon": False,                                        # использовать несколько мониторов
      "aero": False,                                            # разрешить композицию рабочего стола
      "smooth": False,                                          # сглаживание шрифтовразрешение мо
      "showConnectionBar": False,                               # показывать окно подключенияразрешение мо
      "credssp": True,                                          # ???
      "screenSize": "-1x-1",                                    # разрешение экрана (H x W), в случае -1x-1 - Full screen
      "colorDepth": "16",                                       # глубина цвета
      "alsa": False,                                            # Linux Client - использовать Alsa
      "multimedia": False,                                      # Linux Client - мультимедийная синхронизация
      "redirectHome": False,                                    # Linux Client - перенаправить домашнюю папку
      "printerString": "",                                      # Linux Client - строка принтера, используемая с клиентом xfreerdp (проброс)
      "smartcardString": "",                                    # Linux Client - строка смарткарты, используемая с клиентом freerdp (проброс)
      "customParameters": ""                                    # Linux Client - пользовательские параметры используемые при подключении клиента
    }
```
```
# Структура данных HTML5 RDP
    data = {
      "name": "наименование",                                   # наименование транспорта
      "tags": [],                                               # тэги
      "comments": "",                                           # комментарии
      "priority": 10,                                           # приоритет (чем больше, тем выше)
      "nets_positive": True,                                    # сетевой доступ
      "networks": [],                                           # сети, ассоциированные с транспортом. если сети не выбраны, то все сети 
                                                                # (возможно, данный параметр используется в других подключениях)
      "allowed_oss": [],                                        # разрешенные устройства ???
      "type": "HTML5RDPTransport",                              # тип транспорта
      "guacamoleServer": "URL-сервера:порт",                    # адрес туннельного сервера
      "useEmptyCreds": False,                                   # пропустить данные аккаунта
      "fixedName": "",                                          # не пусто - всегда используется как учетные данные
      "fixedPassword": "",                                      # не пусто - всегда используется как учетные данные
      "withoutDomain": False,                                   # без домена
      "fixedDomain": "",                                        # не пусто - всегда используется как учетные данные
      "wallpaper": True,                                        # показать обои
      "desktopComp": True,                                      # разрешить композицию рабочего стола
      "smooth": True,                                           # сглаживание шрифтов
      "enableAudio": True,                                      # включить аудио
      "enablePrinting": True,                                   # включить печать
      "enableFileSharing": True,                                # включить общий доступ к файлам
      "serverLayout": "failsafe",                               # используемая раскладка клавиатуры (типы смотреть в документации и исходниках OpenUDS)
      "security": "rdp",                                        # используемая безопасность подключения (виды смотреть в документации и исходниках OpenUDS)
      "ticketValidity": "60",                                   # срок дейстия тикета (билета) (смотреть в документации и исходниках OpenUDS)
      "forceNewWindow": "false"                                 # открывать в новом окне (смотреть в документации и исходиках OpenUDS)
    }
```

- Создание менеджера ОС **create_osmanager(data)**
```
data = {
        "id": "",                                               # id менеджера ОС (при создании - пустое значение!)
        "name": "наименование",                                 # наименование менеджера ОС
        "type": "LinuxManager",                                 # тип менеджера ОС (смотреть в документации и исходниках OpenUDS)
        "comments": "",                                         # комментарии
        "tags": [''],                                           # тэги
        "onLogout": "keep",                                     # действие при выходе пользователя из системе (keep - сохранить состояние, remove - удалить)
        "idle": -1                                              # максимальное время простоя, перед автоматическим закрытием сессии, в сек. (-1 - бесконечно)
    }
```

- Создание сервис-пула **create_servicepool(data)**
```
# заполенение базовой структуры словаря параметров создаваемого сервис-пула
data = {
        "id": "",                                               # id сервси-пула (при создании - пустое значение!)
        "name": "наименование",                                 # наименование сервис-пула
        "short_name": "короткое наименование",                  # короткое наименование для визуализации сервисов пользователя
        "tags": ["тэги"],                                       # тэги
        "comments": "",                                         # комментарии
        "state": "A",                                           # статус - Включено (смотреть в документации и исходниках OpenUDS)
        "service_id": "",                                       # id сервиса, используемого в данном сервис-пуле, как базового
        "provider_id": "",                                      # id провайдера, в котором располагается вышеуказанный сервис
        "image_id": None,                                       # id образа, привязанный к сервису
        "show_transports": True,                                # показывать транспорты
        "initial_srvs": 2,                                      # первоначально доступные сервисы
        "cache_l1_srvs": 2,                                     # количество сервисов для удержания в кэше
        "cache_l2_srvs": 0,                                     # количество сервисов хранящихся в кэше 2 уровля, для улучшения генерации сервисов
        "max_srvs": 8,                                          # максимальное количество сервисов (L1+L2), которые могут быть созданы для данного сервиса
        "visible": True,                                        # видимость транспорта для пользователей
        "allow_users_remove": False,                            # разрешить удаление пользователями
        "allow_users_reset": True,                              # разрешить сброс пользователями
        "ignores_unused": False,                                # игнорировать неиспользуемые
        "fallbackAccess": "ALLOW",                              # ???
        "meta_member": [],                                      # ???
        "restrained": False,                                    # ???
        "osmanager_id": "",                                     # id менеджера ОС, используемого в данном сервис-пуле, как базовый
        "pool_group_id": None,                                  # группа пулов ???
        "pool_group_name": "",                                  # группа пулов ???
        "pool_group_thumb": "",                                 # группа пулов ???
        "account_id": None,                                     # id учетной записи, связанная с этим пулом услуг
        "calendar_message": ""                                  # сообщение, которое будет показано пользователям, если доступ ограничен правилами календаря
    }

# Заполнение параметров словаря
data["service_id"] = hostvm.service_name_to_id("имя сервис-пула", "имя сервиса")       # id сервиса, используемого в данном сервис-пуле, как базового
data["provider_id"] = hostvm.provider_name_to_id("имя сервис-пула")                    # id провайдера, в котором располагается вышеуказанный сервис
data["osmanager_id"] = hostvm.os_manager_name_to_id("имя менеджера ОС")                # id менеджера ОС, используемого в данном сервис-пуле, как базовый
```

- Добавление групп доступа в сервис-пул **hostvmlib.add_group_to_servicepool(svcpool_name, data)**
```
svcpool_name = 'наименование сервис-пула'
data = {}                                                                       # создаем пустой словарь
data["id"] = hostvm.group_name_to_id("имя аутентификатора", "имя группы")       # заполняем id группы
```

- Добавление транспорта в сервис-пул **hostvm.add_transport_to_servicepool(svcpool_name, data)**
```
svcpool_name = "наименование сервис-пула"
data = {}                                                                       # создаем пустой словарь
data["id"] = hostvm.transport_name_to_id("имя транспорта")                      # заполняем id транспорта
```