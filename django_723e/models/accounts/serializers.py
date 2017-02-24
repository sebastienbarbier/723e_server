"""
    Serializer for accounts module
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from django_723e.models.accounts.models import Account, AccountGuests
from django_723e.models.currency.models import Currency

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    """
        Account serializer
    """
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = Account
        fields = ('id', 'name', 'create', 'currency', 'archived', 'public')

class AccountGuestsSerializer(serializers.ModelSerializer):
    """
        User serializer
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = AccountGuests
        fields = ('account', 'user', 'currency', 'permissions')
