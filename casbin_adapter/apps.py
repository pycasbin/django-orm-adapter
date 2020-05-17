from django.apps import AppConfig
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError


class CasbinAdapterConfig(AppConfig):
    name = 'casbin_adapter'

    def ready(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT app, name applied FROM django_migrations
                    WHERE app = 'casbin_adapter' AND name = '0001_initial';
                    """
                )
                row = cursor.fetchone()
                if row:
                    from .enforcer import enforcer
                    enforcer._load()
        except (OperationalError, ProgrammingError):
            pass

