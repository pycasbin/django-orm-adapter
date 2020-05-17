from django.conf import settings
from casbin import Enforcer
from .adapter import Adapter


class ProxyEnforcer(Enforcer):
    _initialized = False

    def __init__(self, *args, **kwargs):
        if self._initialized:
            super().__init__(*args, **kwargs)

    def _load(self):
        if self._initialized == False:
            self._initialized = True
            model = getattr(settings, 'CASBIN_MODEL')
            enable_log = getattr(settings, 'CASBIN_LOG_ENABLED', False)
            adapter = Adapter()

            super().__init__(model, adapter, enable_log)

            watcher = getattr(settings, 'CASBIN_WATCHER', None)
            if watcher:
                self.set_watcher(watcher)

            role_manager = getattr(settings, 'CASBIN_ROLE_MANAGER', None)
            if role_manager:
                self.set_role_manager(role_manager)

    def __getattribute__(self, name):
        safe_methods = ['__init__', '_load', '_initialized']
        if not super().__getattribute__('_initialized') and name not in safe_methods:
            raise Exception((
                "Calling enforcer attributes before django registry is ready. "
                "Prevent making any calls to the enforcer on import/startup"
            ))

        return super().__getattribute__(name)


enforcer = ProxyEnforcer()

