from casbin import persist

from .models import CasbinRule


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
        queryParams = {'ptype': ptype}
        for i, v in enumerate(rule):
            queryParams[f'v{i}'] = v
        rows_deleted, _ = CasbinRule.objects.filter(**queryParams).delete()
        return True if rows_deleted > 0 else False

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """removes policy rules that match the filter from the storage.
        This is part of the Auto-Save feature.
        """
        queryParams = {'ptype': ptype}
        if not(0 <= field_index <= 5):
            return False
        if not (1 <= field_index + len(field_values) <= 6):
            return False
        for i, v in enumerate(field_values):
            queryParams[f'v{i + field_index}'] = v
        rows_deleted, _ = CasbinRule.objects.filter(**queryParams).delete()
        return True if rows_deleted > 0 else False
