# Django ORM Adapter for PyCasbin

[![GitHub Action](https://github.com/pycasbin/django-orm-adapter/workflows/build/badge.svg?branch=master)](https://github.com/pycasbin/django-orm-adapter/actions)
[![Coverage Status](https://coveralls.io/repos/github/pycasbin/django-orm-adapter/badge.svg)](https://coveralls.io/github/pycasbin/django-orm-adapter)
[![Version](https://img.shields.io/pypi/v/casbin-django-orm-adapter.svg)](https://pypi.org/project/casbin-django-orm-adapter/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/casbin-django-orm-adapter.svg)](https://pypi.org/project/casbin-django-orm-adapter/)
[![Pyversions](https://img.shields.io/pypi/pyversions/casbin-django-orm-adapter.svg)](https://pypi.org/project/casbin-django-orm-adapter/)
[![Download](https://img.shields.io/pypi/dm/casbin-django-orm-adapter.svg)](https://pypi.org/project/casbin-django-orm-adapter/)
[![Discord](https://img.shields.io/discord/1022748306096537660?logo=discord&label=discord&color=5865F2)](https://discord.gg/S5UjpzGZjN)

Django ORM Adapter is the [Django](https://www.djangoproject.com/)'s [ORM](https://docs.djangoproject.com/en/3.0/ref/databases/) adapter for [PyCasbin](https://github.com/pycasbin/django-orm-adapter). With this library, Casbin can load policy from Django ORM supported database or save policy to it.

Based on [Officially Supported Databases](https://docs.djangoproject.com/en/3.0/ref/databases/), The current supported databases are:

- PostgreSQL
- MariaDB
- MySQL
- Oracle
- SQLite
- IBM DB2
- Microsoft SQL Server
- Firebird
- ODBC

## Installation

```
pip install casbin-django-orm-adapter
```

Add `casbin_adapter.apps.CasbinAdapterConfig` to your `INSTALLED_APPS`

```python
# settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    ...
    'casbin_adapter.apps.CasbinAdapterConfig',
    ...
]

CASBIN_MODEL = os.path.join(BASE_DIR, 'casbin.conf')
```

To run schema migration, execute `python manage.py migrate casbin_adapter`

## Simple Example

```python
# views.py
from casbin_adapter.enforcer import enforcer

def hello(request):
    sub = "alice"  # the user that wants to access a resource.
    obj = "data1"  # the resource that is going to be accessed.
    act = "read"  # the operation that the user performs on the resource.

    if e.enforce(sub, obj, act):
        # permit alice to read data1casbin_django_orm_adapter
        pass
    else:
        # deny the request, show an error
        pass
```

## Configuration

### `CASBIN_MODEL`
A string containing the file location of your casbin model.

### `CASBIN_ADAPTER`
A string containing the adapter import path. Default to the django adapter shipped with this package: `casbin_adapter.adapter.Adapter`

### `CASBIN_ADAPTER_ARGS`
A tuple of arguments to be passed into the constructor of the adapter specified
in `CASBIN_ADAPTER`. Refer to adapters to see available arguments. 

E.g. if you wish to use the file adapter 
set the adapter to `casbin.persist.adapters.FileAdapter` and use
`CASBIN_ADAPTER_ARGS = ('path/to/policy_file.csv',)`

### `CASBIN_DB_ALIAS`
The database the adapter uses. Default to "default".

### `CASBIN_WATCHER`
Watcher instance to be set as the watcher on the enforcer instance.

### `CASBIN_ROLE_MANAGER`
Role manager instance to be set as the role manager on the enforcer instance.


### Getting Help

- [PyCasbin](https://github.com/casbin/pycasbin)

### License

This project is licensed under the [Apache 2.0 license](LICENSE).
