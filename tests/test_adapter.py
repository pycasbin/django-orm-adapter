import os
import casbin
import simpleeval

from django.test import TestCase
from casbin_adapter.models import CasbinRule
from casbin_adapter.adapter import Adapter


def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


def get_enforcer():
    adapter = Adapter()

    CasbinRule.objects.bulk_create(
        [
            CasbinRule(ptype="p", v0="alice", v1="data1", v2="read"),
            CasbinRule(ptype="p", v0="bob", v1="data2", v2="write"),
            CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="read"),
            CasbinRule(ptype="p", v0="data2_admin", v1="data2", v2="write"),
            CasbinRule(ptype="g", v0="alice", v1="data2_admin"),
        ]
    )

    return casbin.Enforcer(get_fixture("rbac_model.conf"), adapter)


class TestConfig(TestCase):
    def test_enforcer_basic(self):
        e = get_enforcer()
        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))

    def test_add_policy(self):
        adapter = Adapter()
        e = casbin.Enforcer(get_fixture("rbac_model.conf"), adapter)

        try:
            self.assertFalse(e.enforce("alice", "data1", "read"))
            self.assertFalse(e.enforce("bob", "data1", "read"))
            self.assertFalse(e.enforce("bob", "data2", "write"))
            self.assertFalse(e.enforce("alice", "data2", "read"))
            self.assertFalse(e.enforce("alice", "data2", "write"))
        except simpleeval.NameNotDefined:
            # This is caused by an upstream bug when there is no policy loaded
            # Should be resolved in pycasbin >= 0.3
            pass

        adapter.add_policy(sec=None, ptype="p", rule=["alice", "data1", "read"])
        adapter.add_policy(sec=None, ptype="p", rule=["bob", "data2", "write"])
        adapter.add_policy(sec=None, ptype="p", rule=["data2_admin", "data2", "read"])
        adapter.add_policy(sec=None, ptype="p", rule=["data2_admin", "data2", "write"])
        adapter.add_policy(sec=None, ptype="g", rule=["alice", "data2_admin"])

        e.load_policy()

        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))
        self.assertFalse(e.enforce("bogus", "data2", "write"))

    def test_save_policy(self):
        model = casbin.Enforcer(get_fixture("rbac_model.conf"), get_fixture("rbac_policy.csv")).model
        adapter = Adapter()
        adapter.save_policy(model)
        e = casbin.Enforcer(get_fixture("rbac_model.conf"), adapter)

        self.assertTrue(e.enforce("alice", "data1", "read"))
        self.assertFalse(e.enforce("bob", "data1", "read"))
        self.assertTrue(e.enforce("bob", "data2", "write"))
        self.assertTrue(e.enforce("alice", "data2", "read"))
        self.assertTrue(e.enforce("alice", "data2", "write"))

    def test_autosave_off_doesnt_persist_to_db(self):
        adapter = Adapter()
        e = casbin.Enforcer(get_fixture("rbac_model.conf"), adapter)

        e.enable_auto_save(False)
        e.add_policy("alice", "data1", "write")
        e.load_policy()
        policies = e.get_policy()
        self.assertListEqual(policies, [])

    def test_autosave_on_persists_to_db(self):
        adapter = Adapter()
        e = casbin.Enforcer(get_fixture("rbac_model.conf"), adapter)

        e.enable_auto_save(True)
        e.add_policy("alice", "data1", "write")
        e.load_policy()
        policies = e.get_policy()
        self.assertListEqual(policies, [["alice", "data1", "write"]])

    def test_autosave_on_persists_remove_action_to_db(self):
        adapter = Adapter()
        e = casbin.Enforcer(get_fixture("rbac_model.conf"), adapter)
        e.add_policy("alice", "data1", "write")
        e.load_policy()
        self.assertListEqual(e.get_policy(), [["alice", "data1", "write"]])

        e.enable_auto_save(True)
        e.remove_policy("alice", "data1", "write")
        e.load_policy()
        self.assertListEqual(e.get_policy(), [])

    def test_remove_filtered_policy(self):
        e = get_enforcer()

        e.remove_filtered_policy(0, "data2_admin")
        e.load_policy()
        self.assertListEqual(e.get_policy(), [["alice", "data1", "read"], ["bob", "data2", "write"]])

    def test_str(self):
        rule = CasbinRule(ptype="p", v0="alice", v1="data1", v2="read")
        self.assertEqual(str(rule), "p, alice, data1, read")

    def test_repr(self):
        rule = CasbinRule(ptype="p", v0="alice", v1="data1", v2="read")
        self.assertEqual(repr(rule), '<CasbinRule None: "p, alice, data1, read">')
        rule.save()
        self.assertRegex(repr(rule), r'<CasbinRule \d+: "p, alice, data1, read">')
