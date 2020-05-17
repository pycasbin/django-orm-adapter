from django.apps import AppConfig
from django.db import connection
from django.db.utils import OperationalError


class CasbinAdapterConfig(AppConfig):
    name = 'casbin_adapter'

    def ready(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT app, name applied FROM django_migrations WHERE app = 'casbin_adapter' AND name = '0001_initial';")
                row = cursor.fetchone()
                if row:
                    from .adapter import _mark_ready, _enforcer as enforcer

                    _mark_ready()
                    if enforcer:
                        print('delayed enforcer init')
                        enforcer._init_enforcer()
        except OperationalError:
            pass

