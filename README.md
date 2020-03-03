# Django ORM Adapter for PyCasbin

[![Build Status](https://www.travis-ci.org/pycasbin/django-orm-adapter.svg?branch=master)](https://www.travis-ci.org/pycasbin/django-orm-adapter)
[![Coverage Status](https://coveralls.io/repos/github/pycasbin/django-orm-adapter/badge.svg)](https://coveralls.io/github/pycasbin/django-orm-adapter)
[![Version](https://img.shields.io/pypi/v/casbin_django_orm_adapter.svg)](https://pypi.org/project/casbin_django_orm_adapter/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/casbin_django_orm_adapter.svg)](https://pypi.org/project/casbin_django_orm_adapter/)
[![Pyversions](https://img.shields.io/pypi/pyversions/casbin_django_orm_adapter.svg)](https://pypi.org/project/casbin_django_orm_adapter/)
[![Download](https://img.shields.io/pypi/dm/casbin_django_orm_adapter.svg)](https://pypi.org/project/casbin_django_orm_adapter/)
[![License](https://img.shields.io/pypi/l/casbin_django_orm_adapter.svg)](https://pypi.org/project/casbin_django_orm_adapter/)

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
pip install casbin_django_orm_adapter
```

Add `casbin_adapter` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'casbin_adapter',
    ...
]
```

## Simple Example

```python
import casbin
from casbin_adapter.adapter import Adapter

adapter = Adapter()

e = casbin.Enforcer('path/to/model.conf', adapter, True)

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

### Getting Help

- [PyCasbin](https://github.com/casbin/pycasbin)

### License

This project is licensed under the [Apache 2.0 license](LICENSE).
