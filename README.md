[![ru](https://img.shields.io/badge/lang-ru-red.svg)](https://github.com/debugger1979/host_vm_lib/README.ru.md)

# The library for working with the HOSTVM VDI API (OpenUDS)
## Is designed to automate the process of configuring the parameters of the HOSTVM virtualization platform

Using this library, you can perform the following operations:
- Working with the configuration of the HOSTVM VDI application itself (changing parameters)
- Account administration (changing the superuser password)
- Work with authenticators (creation, reading, modification, deletion)
- Working with access groups, inside the authenticator (creation, reading, modification, deletion)
- Work with service providers, services (creation, reading, modification, deletion)
- Working with transports (creating, reading, modifying, deleting)
- Work with OS managers (create, read, modify, delete)
- Work with service pools (creation, reading, modification, deletion, binding of access groups, transports, OS managers, providers)

**Examples of working with the library:**

_Note:_
1. _ To create objects (authenticators, groups, service providers, etc.), certain parameters are required, formatted in a dictionary format. The recommendation is to initially create these objects "by hand" in the application itself, and then read them using the methods of this library. Then use the resulting structures in your scripts. The parameter templates will be posted later._
2. _ The library has the ability to access objects by their name (as indicated in the application itself), and not by id_
3. _**Important!** A superuser account is required to change the settings in the application._

- Authorization in the application. This operation is required only once for the entire session of working with the application.

```
from host_vm_lib import HostVMAPI

# The base address for accessing application methods
rest_url = 'http://URL-HOSTVM/rest/'
# The line for authorization in the application
parameters = '{"auth": "admin", "username": "user", "password": "password"}'

hostvm = HostVMAPI()

if hostvm.login(rest_url=rest_url, parameters=parameters) == 0:
    # Authorization in the application was successful
    # ... (performing the necessary manipulations with applications)
else:
    # Возникли проблемы при авторизации. Сообщение об ошибке можно получить в свойстве класса - status_msg
    print(hostvm.status_msg)
```

- Creating a service provider. A dictionary containing the parameters of the service provider being created is used.

```
    data = {
        "id": "",
        "name": "cloud.ru",
        "tags": [],
        "comments": "",
        "type": "openNebulaPlatform",
        "host": "the host name of the virtualization server",
        "port": "2633",
        "ssl": False,
        "username": "user",
        "password": "password",
        "maxPreparingServices": "10",
        "maxRemovingServices": "5",
        "timeout": "10"
        }
    hostvm.create_provider(data)
    print(hostvm.status_msg)
```# host_vm_lib
