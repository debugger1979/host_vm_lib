from httplib2 import Http
import json

class HostVMAPI:

    def login(self, rest_url:str, parameters:str):
        """
        Метод - Авторизации в HOSTVM.
        
        Вход:
            rest_url - базовый URL rest-запроса.
            parameters - словарь параметров авторизации.
        
        Выход:
            0 - авторизация произошла успешно
           -1 - ошибка аторизации
            status_msg - сообщение о статусе выполнения метода
        """
        client = Http()
        self.rest_url = rest_url
        self.headers = {}
        self.status_msg = ''

        response_data, content = client.request(rest_url + 'auth/login',
                                  method='POST', body=parameters)

        if response_data['status'] != '200':
            self.status_msg = 'Authentication error!'
            return -1

        response_content = json.loads(content)
        if response_content['result'] != 'ok':
            self.status_msg = 'Authentication error!'
            return -1

        self.headers['X-Auth-Token'] = response_content['token']
        self.headers['content-type'] = 'application/json'
        self.status_msg = 'Authentication Ok!'
        return 0
    
    def logout(self):
        """
        Метод - Завершение сеанса HOSTVM.\n
        Вход:
            Ничего\n
        Выход:\n
            0 - авторизация произошла успешно\n
           -1 - ошибка аторизации\n
            status_msg - сообщение о статусе выполнения метода
        """

        client = Http()

        response_data, content = client.request(
            self.rest_url + 'auth/logout', headers=self.headers)

        if response_data['status'] != '200':
            self.status_msg = 'Error requesting logout'
            return -1

        return 0
    
    def get_list_supported_auths(self):
        """
        Метод - Вывод списка поддерживаемых аутентификаторов и их полей.
        од - Авторизации в HOSTVM.\n
        Вход:
            rest_url - базовый URL rest-запроса.\n
            parameters - словарь параметров авторизации.\n
        
        Выход:\n
            0 - авторизация произошла успешно\n
           -1 - ошибка аторизации\n
            status_msg - сообщение о статусе выполнения метода
        """
        client = Http()
        self.list_supported_auth = []

        response_data, content = client.request(
            self.rest_url + 'authenticators/types', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = content
            return -1

        r = json.loads(content)

        # Тому, кто придумал хранить иконки в структруре данных, надо забить гвоздь в голову.
        for res in r:
            del res['icon']
        
        self.list_supported_auth = r

        return 0

        # for auth in r:
        #     print('* {}'.format(auth['name']))
        #     for fld in auth:  # every auth is converted to a dictionary in python by json.load
        #         # Skip icon
        #         if fld != 'icon':
        #             print(" > {}: {}".format(fld, auth[fld]))
        #     response_data, content = client.request(
        #         self.rest_url + 'authenticators/gui/{}'.format(auth['type']), headers=self.headers)
        #     if response_data['status'] != '200':
        #         self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
        #         sys.exit(1)

        #     print(" > GUI")
        #     rr = json.loads(content)
        #     for field in rr:
        #         print("   - Name: {}".format(field['name']))
        #         print("   - Value: {}".format(field['value']))
        #         print("   - GUI: ")
        #         for gui in field['gui']:
        #             print("     + {}: {}".format(gui, field['gui'][gui]))
        #     print(" > Simplified fields:")
        #     for field in rr:
        #         print("   - Name: {}, Type: {}, is Required?: {}".format(
        #             field['name'], field['gui']['type'], field['gui']['required']))

    def auth_name2id(self, auth_name):
        """
        Метод - Преобразование имени коннектора в его Id

        auth_name - имя коннектора

        результат - Id коннектора
        """
        self.get_list_current_auth()
        for auth in self.list_current_auth:
            if auth['name'] == auth_name:
                return auth['id']
        return ''
    
    def group_name2id(self, auth_name, group_name):
        """
        Метод - Преобразование имени группы в его Id

        group_name - имя группы

        результат - Id группы
        """
        self.get_list_current_groups(auth_name)
        for group in self.list_current_groups:
            if group['name'] == group_name:
                return group['id']
        return ''

    def provider_name2id(self, provider_name):
        """
        Метод - Преобразование имени провайдера в его Id

        provider_name - имя провайдера

        Результат - Id провайдера
        """
        if self.get_list_current_providers() == 0 and (self.list_current_providers != []):
            for provider in self.list_current_providers:
                if provider_name == provider['name']:
                    return provider['id']
        return ''

    def service_name2id(self, SP_name, svc_name):
        """
        Метод - Преобразование имени сервиса в его Id

        SP_name - имя сервис-провайдера

        svc_name - имя сервиса

        Результат - Id сервиса
        """
        self.get_list_services_in_SP(SP_name)

        for service in self.list_services_in_SP:
            if service['name'] == svc_name:
                return service['id']
        return ''

    def OSmanager_name2id(self, OSmanager_name):
        """
        Метод - преобразование имени менеджера в его id

        OSmanager_name - наименование менеджера ОС

        Результат - id менеджера ОС
        """
        if self.get_list_OSmanagers() == 0:
            for group in self.status_msg:
                if group['name'] == OSmanager_name:
                    return group['id']
        return ''

    def transport_name2id(self, transport_name):
        """
        Метод - Преобразование наименование транспорта в его id
        """
        if self.get_transport_list() == 0:
            for transport in self.status_msg:
                if transport['name'] == transport_name:
                    return transport['id']
        return ""

    def get_list_current_auth(self):
        """
        Метод вывода списка существующих коннекторов и их полей
        """
        client = Http()
        self.list_current_auth = []

        response_data, content = client.request(
            self.rest_url + 'authenticators', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(
                response_data, content)
            return -1

        self.list_current_auth = json.loads(content)
        return 0
    
    def get_auth_info(self, auth_name):
        """
        Метод - Получение информации о коннекторе
        
        auth_name - имя коннектора
        """
        client = Http()
        auth_id = self.auth_name2id(auth_name)
        response_data, content = client.request(
            self.rest_url + 'authenticators/' + auth_id, headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(
                response_data, content)
            return {}
        r = json.loads(content)
        return r

    def create_auth(self, data):
        """
        Метод - Создание коннектора. 

        data - структура данных, описывающая создаваемый коннектор.
        
        Тип и поля можно взять из list_supported_auths_and_fields()
        """

        client = Http()

        response_data, content = client.request(
            self.rest_url + 'authenticators', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(
                response_data, content)
            return -1

        r = json.loads(content)
        self.status_msg = "Correctly created {} with id {}".format(
            r['name'], r['id'])
        return 0

    def delete_auth(self, auth_name):
        """
        Метод - Удаление существующего коннектора

        auth_id - идентификатор коннектора. 
        
        Можно получить из list_existing_auth()
        """
        client = Http()

        auth_id = self.auth_name2id(auth_name)

        response_data, content = client.request(
            self.rest_url + 'authenticators/{}'.format(auth_id), 'DELETE', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        self.status_msg = "Correctly deleted {}".format(auth_id)
        return 0

    def get_list_current_groups(self, auth_name):
        """
        Метод - Получить список групп внутри коннектора.

        auth_id - идентификатор коннектора. Можно получить из list_existing_auth()
        """
        client = Http()

        auth_id = self.auth_name2id(auth_name)
        response_data, content = client.request(
            self.rest_url + 'authenticators/{}/groups'.format(auth_id), 'GET', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        self.list_current_groups = json.loads(content)

        return 0

    def create_internal_group(self, auth_name, data):
        """
        Сздание группы внутри коннектора.

        auth_name - имя коннектора
        data - структура данных, описывающая создаваемую группу

        """
        client = Http()

        auth_id = self.auth_name2id(auth_name)
        response_data, content = client.request(self.rest_url + 'authenticators/{}/groups'.format(
            auth_id), 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        r = json.loads(content)
        self.status_msg = "Correctly created {} with id {}".format(r['name'], r['id'])
        return 0

    def get_config_info(self):
        """
        Метод - Запрос информации о конфигурации приложения
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'config', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return {}

        return json.loads(content)

    def get_superuser_passw(self):
        """
        Метод - Получить пароль суперпользователя
        """
        system_config = self.get_config_info()
        if system_config != {}:
            return system_config['Security']['rootPass']['value']
        return ''

    def set_superuser_pass(self, newPassword: str):
        """
        Метод - Установка пароля суперпользователе
        """
        client = Http()
        # Запрос списка параметров конфигурации приложения
        data = self.get_config_info()
        if data != '':
            # Меняем поле пароля Суперпользователя
            data['Security']['rootPass']['value'] = newPassword
            # Отправляем обновленный список параметров конфигурации в приложение
            response_data, content = client.request(
                self.rest_url + 'config', method='PUT', headers=self.headers, body=json.dumps(data))
            if response_data['status'] != '200':
                self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
                return -1
            self.status_msg = json.loads(content)
            return 0
        else:
            self.status_msg = 'Error: Config is empty'
            return -1

    def get_list_supported_providers(self):
        """
        Метод - Получить список поддерживаемых сервис-провайдеров
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'providers/types', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        r = json.loads(content)

        # Тому, кто придумал хранить иконки в структруре данных, надо забить гвоздь в голову
        for res in r:
            del res['icon']
        
        self.list_supported_providers = r 
        return 0

    def get_list_current_providers(self):
        """
        Метод - Получить список текущих сервис-провайдеров
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'providers', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        r = json.loads(content)
    
        self.list_current_providers = r 
        return 0

    def get_info_provider(self, SP_name):
        """
        Метод - Запрос информации о параметрах сервис-провайдера по ID
        """
        client = Http()
        SP_id = self.provider_name2id(SP_name)
        response_data, content = client.request(self.rest_url + 'providers/' + SP_id, headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return {}

        r = json.loads(content)
                
        return r 
    
    def create_provider(self, data):
        """
        Метод - Создание сервис-провайдера
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'providers',
                                'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        self.status_msg = json.loads(content)
        self.get_list_current_providers()

        return 0

    def get_list_services_in_SP(self, SP_name):
        """
        Метод - Список сервисов внутри сервис-провайдера
        """
        client = Http()
        SP_id = self.provider_name2id(SP_name)
        response_data, content = client.request(
            self.rest_url + 'providers/' + SP_id + '/services', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        
        self.list_services_in_SP = json.loads(content)
        return 0
       
    def create_service_in_provider(self, SP_name, data):
        """
        Метод - Создание сервиса в сервис-провайдере
        """
        client = Http()
        SP_id = self.provider_name2id(SP_name)

        response_data, content = client.request(self.rest_url + 'providers/' + SP_id +
                                '/services', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        r = json.loads(content)
        self.status_msg = "Correctly created {} with id {}".format(r['name'], r['id'])
        return 0

    def get_service_info_in_SP(self, SP_name, svc_name):
        """
        Метод - Получить информацию о конкретном сервисе конкретного провайдера

        SP_name - имя сервис провайдера

        svc_name - имя сервиса

        Результат - информация о сервисе
        """
        client = Http()

        SP_id = self.provider_name2id(SP_name)
        svc_id = self.service_name2id(SP_name, svc_name)

        response_data, content = client.request(
            self.rest_url + 'providers/' + SP_id + '/services/' + svc_id, headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return {}
        r = json.loads(content)

        return r
    
    def get_transport_list(self, typeBool=False):
        """
        Метод - Получить список транспортов

        True - Получить список всех поддерживаемых трансопортов

        False|Ничего - Получить список существующих транспортов
        """
        result = []
        client = Http()

        types = ''
        if typeBool:
            types = '/types'
        response_data, content = client.request(
            self.rest_url + 'transports' + types, headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        r = json.loads(content)

        if not typeBool:
            for item_r in r:
                client = Http()
                response_data, content = client.request(
                    self.rest_url + 'transports/' + item_r['id'], headers=self.headers)
                if response_data['status'] != '200':
                    self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
                    return -1
                result.append(json.loads(content))
        else:
            result = r

        # Тому, кто придумал хранить иконки в структруре данных, надо забить гвоздь в голову
        if typeBool:
            for res in result:
                del res['icon']
        self.status_msg = result
        return 0

    def create_transport(self, data):
        """
        Метод - Создание транспорта

        data - структура данных необходимая для создания транспорта
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'transports', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        
        self.status_msg = json.loads(content)
        return 0

    def get_list_OSmanagers(self, typeBool=False):
        """
        Метод - Получить список менеджеров ОС

        True - Список типов поддерживаемых менеджеров ОС

        False|Ничего - Список существующих менеджеров ОС

        """
        client = Http()
        result = []

        types = ''
        if typeBool:
            types = '/types'

        response_data, content = client.request(self.rest_url + 'osmanagers' + types, headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        r = json.loads(content)

        if not typeBool:
            for item_r in r:
                client = Http()
                response_data, content = client.request(
                    self.rest_url + 'osmanagers/' + item_r['id'], headers=self.headers)
                if response_data['status'] != '200':
                    self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
                    return -1
                result.append(content)

        # Кто додумался до хранения иконок внутри структур данных???
        if typeBool:
            for osmanager_item in r:
                del osmanager_item['icon']

        self.status_msg = r
        return 0
    
    def create_osmanager(self, data):
        """
        Метод - Создание менеджера ОС

        data - структура данных описывающая создаваемый менеджер ОС
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'osmanagers', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        self.status_msg = json.loads(content)
        return 0

    def get_servicepool_list(self):
        """
        Метод - Получить список существующих сервис-пулов
        """
        client = Http()

        response_data, content = client.request(
            self.rest_url + 'servicespools', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        
        self.status_msg = json.loads(content)
        return 0

    def create_servicepool(self, data):
        """
        Метод - Создание сервис-пула

        data - структура данных, описывающая создаваемый сервис-пул
        """
        client = Http()

        response_data, content = client.request(self.rest_url + 'servicespools', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        self.status_msg = json.loads(content)
        return 0

    def srvcpool_name2id(self, srvcpool_name):
        """
        Метод - Преобразование наименование сервис-пула в id
        """
        if self.get_servicepool_list() == 0:
            for servicepool in self.status_msg:
                if servicepool['name'] == srvcpool_name:
                    return servicepool['id']
        return ''

    def get_list_group_in_servicepool(self, svcpool_name):
        """
        Метод - Получить список групп доступа в сервис-пуле
        """
        client = Http()

        svcpool_id = self.srvcpool_name2id(svcpool_name)
        response_data, content = client.request(
            self.rest_url + 'servicespools/' + svcpool_id + '/groups', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        self.status_msg = json.loads(content)
        return 0

    def add_group_to_servicepool(self, svcpool_name, data):
        """
        Метод - Добавить группу доступа в сервис-пул
        
        SP_id - id скрвис-пула
        
        data: структура данных JSON - id группы доступа
        """
        client = Http()

        svcpool_id = self.srvcpool_name2id(svcpool_name)
        response_data, content = client.request(self.rest_url + 'servicespools/' + svcpool_id + '/groups', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        self.status_msg = json.loads(content)
        return 0

    def get_list_transport_in_servicepool(self, svcpool_name):
        """
        Метод - Получить список транспортов добавлденных в сервис-пул

        svcpool_name - наименование сервис-пула
        """
        client = Http()
        svcpool_id = self.srvcpool_name2id(svcpool_name)
        response_data, content = client.request(
            self.rest_url + 'servicespools/' + svcpool_id + '/transports', headers=self.headers)
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1
        
        self.status_msg = json.loads(content)
        return 0

    def add_transport_to_servicepool(self, svcpool_name, data):
        """
        Метод - Добавить группу доступа в сервис-пул
        
        svcpool_name: наименование скрвис-пула

        data: структура данных, описывающих добавляемый транспорт
        """
        client = Http()

        svcpool_id = self.srvcpool_name2id(svcpool_name)
        response_data, content = client.request(self.rest_url + 'servicespools/' + svcpool_id + '/transports', 'PUT', headers=self.headers, body=json.dumps(data))
        if response_data['status'] != '200':
            self.status_msg = "Error in request: \n-------------------\n{}\n{}\n----------------".format(response_data, content)
            return -1

        self.status_msg = json.loads(content)
        return 0
