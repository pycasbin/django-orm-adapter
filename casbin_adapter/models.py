# Copied from: https://github.com/pycasbin/django-orm-adapter
# as it lacks a setup.py file atm
from django.db import models


class CasbinRule(models.Model):
    ptype = models.CharField(max_length=255)
    v0 = models.CharField(max_length=255)
    v1 = models.CharField(max_length=255)
    v2 = models.CharField(max_length=255)
    v3 = models.CharField(max_length=255)
    v4 = models.CharField(max_length=255)
    v5 = models.CharField(max_length=255)

    class Meta:
        db_table = 'casbin_rule'

    def __str__(self):
        text = self.ptype

        if self.v0:
            text = text + ', ' + self.v0
        if self.v1:
            text = text + ', ' + self.v1
        if self.v2:
            text = text + ', ' + self.v2
        if self.v3:
            text = text + ', ' + self.v3
        if self.v4:
            text = text + ', ' + self.v4
        if self.v5:
            text = text + ', ' + self.v5
        return text

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))
