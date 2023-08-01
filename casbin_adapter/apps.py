from django.apps import AppConfig
from django.conf import settings


class CasbinAdapterConfig(AppConfig):
    name = "casbin_adapter"

    def ready(self):
        from .enforcer import initialize_enforcer

        db_alias = getattr(settings, "CASBIN_DB_ALIAS", "default")
        initialize_enforcer(db_alias)
