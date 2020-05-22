from django.apps import AppConfig
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError


class CasbinAdapterConfig(AppConfig):
    name = 'casbin_adapter'

    def ready(self):
        from .enforcer import initialize_enforcer
        initialize_enforcer()

