import logging
from django.conf import settings
from django.db import connection, connections
from django.db.utils import OperationalError, ProgrammingError

from casbin import Enforcer

from .utils import import_class

logger = logging.getLogger(__name__)


class ProxyEnforcer(Enforcer):
    _initialized = False
    db_alias = "default"

    def __init__(self, *args, **kwargs):
        if self._initialized:
            super().__init__(*args, **kwargs)
        else:
            logger.info("Deferring casbin enforcer initialisation until django is ready")

    def _load(self):
        if self._initialized is False:
            logger.info("Performing deferred casbin enforcer initialisation")
            self._initialized = True
            model = getattr(settings, "CASBIN_MODEL")
            adapter_loc = getattr(settings, "CASBIN_ADAPTER", "casbin_adapter.adapter.Adapter")
            adapter_args = getattr(settings, "CASBIN_ADAPTER_ARGS", tuple())
            self.db_alias = getattr(settings, "CASBIN_DB_ALIAS", "default")
            Adapter = import_class(adapter_loc)
            adapter = Adapter(self.db_alias, *adapter_args)

            super().__init__(model, adapter)
            logger.debug("Casbin enforcer initialised")

            watcher = getattr(settings, "CASBIN_WATCHER", None)
            if watcher:
                self.set_watcher(watcher)

            role_manager = getattr(settings, "CASBIN_ROLE_MANAGER", None)
            if role_manager:
                self.set_role_manager(role_manager)

    def __getattribute__(self, name):
        safe_methods = ["__init__", "_load", "_initialized"]
        if not super().__getattribute__("_initialized") and name not in safe_methods:
            initialize_enforcer(self.db_alias)
            if not super().__getattribute__("_initialized"):
                raise Exception(
                    (
                        "Calling enforcer attributes before django registry is ready. "
                        "Prevent making any calls to the enforcer on import/startup"
                    )
                )

        return super().__getattribute__(name)


enforcer = ProxyEnforcer()


def initialize_enforcer(db_alias=None):
    try:
        row = None
        connect = connections[db_alias] if db_alias else connection
        with connect.cursor() as cursor:
            cursor.execute(
                """
                SELECT app, name applied FROM django_migrations
                WHERE app = 'casbin_adapter' AND name = '0001_initial';
                """
            )
            row = cursor.fetchone()

        if row:
            enforcer._load()
    except (OperationalError, ProgrammingError):
        pass
