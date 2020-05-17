from django.shortcuts import render

from casbin_adapter.adapter import Enforcer

print('views init')
e = Enforcer()

print('views.py enforcer', e, id(e))

# Create your views here.
