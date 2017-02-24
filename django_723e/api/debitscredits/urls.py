"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from django_723e import settings
from django_723e.api.debitscredits.views import ApiDebitscredits

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiDebitscredits, base_name='debitscredits')

urlpatterns = ROUTER.urls
