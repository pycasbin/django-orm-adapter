from django.apps import AppConfig


class CasbinAdapterConfig(AppConfig):
    name = "casbin_adapter"

    def ready(self):
        from .enforcer import initialize_enforcer

        initialize_enforcer()
