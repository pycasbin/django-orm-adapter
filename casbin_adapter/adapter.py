from casbin import persist, Enforcer as BaseEnforcer

from .models import CasbinRule

_enforcer = None
_ready = False

def _mark_ready():
    global _ready
    _ready = True

def register(enforcer):
    _enforcer = enforcer

class Enforcer(BaseEnforcer):
    _loaded = False
    _calls = list()

    def __init__(self, *args, **kwargs):
        global _ready
        if _ready == True:
            self._init_enforcer()
        else:
            attr = super().__init__
            self._record_call(attr, *args, **kwargs)

        global _enforcer
        _enforcer = self


    def _init_enforcer(self):
        self._loaded = True
        for call in self._calls:
            attr, args, kwargs = call
            attr(*args, **kwargs)

    def _record_call(self, attr, *args, **kwargs):
        self._calls.append([attr, args, kwargs])

    def __getattribute__(self, name):
        if _ready:
            return super().__getattribute__(name)

        attr = super().__getattribute__(name)
        if name in ['__init__', '_init_enforcer', '_record_call', '_calls', '_loaded']:
            return attr
        else:
            if hasattr(attr, '__call__'):
                def proxy(*args, **kwargs):
                    self._record_call(attr, *args, **kwargs)
                return proxy
            else:
                return attr



class Adapter(persist.Adapter):
    """the interface for Casbin adapters."""

    def load_policy(self, model):
        """loads all policy rules from the storage."""
        lines = CasbinRule.objects.all()

        for line in lines:
            persist.load_policy_line(str(line), model)

    def _create_policy_line(self, ptype, rule):
        line = CasbinRule(ptype=ptype)
        if len(rule) > 0:
            line.v0 = rule[0]
        if len(rule) > 1:
            line.v1 = rule[1]
        if len(rule) > 2:
            line.v2 = rule[2]
        if len(rule) > 3:
            line.v3 = rule[3]
        if len(rule) > 4:
            line.v4 = rule[4]
        if len(rule) > 5:
            line.v5 = rule[5]
        return line

    def save_policy(self, model):
        """saves all policy rules to the storage."""
        # See https://casbin.org/docs/en/adapters#autosave
        # for why this is deleting all rules
        CasbinRule.objects.all().delete()

        lines = []
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    lines.append(self._create_policy_line(ptype, rule))
        CasbinRule.objects.bulk_create(lines)
        return True

    def add_policy(self, sec, ptype, rule):
        """adds a policy rule to the storage."""
        line = self._create_policy_line(ptype, rule)
        line.save()

    def remove_policy(self, sec, ptype, rule):
        """removes a policy rule from the storage."""
        query_params = {'ptype': ptype}
        for i, v in enumerate(rule):
            query_params['v{}'.format(i)] = v
        rows_deleted, _ = CasbinRule.objects.filter(**query_params).delete()
        return True if rows_deleted > 0 else False

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """removes policy rules that match the filter from the storage.
        This is part of the Auto-Save feature.
        """
        query_params = {'ptype': ptype}
        if not(0 <= field_index <= 5):
            return False
        if not (1 <= field_index + len(field_values) <= 6):
            return False
        for i, v in enumerate(field_values):
            query_params['v{}'.format(i + field_index)] = v
        rows_deleted, _ = CasbinRule.objects.filter(**query_params).delete()
        return True if rows_deleted > 0 else False
