"""
    Accounts models
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django_723e.models.currency.models import Currency

PERMISSIONS = (
    ('W', 'Read/write'), # Can just edit data
    ('R', 'Read'), # Can only access data
)

class Account(models.Model):
    """
        An account is considere as a bank account. Name is just a label for the user interface.
    """
    owner = models.ForeignKey(User, related_name="accounts", null=False, blank=False)
    name = models.CharField(_(u'Name'), max_length=255)
    create = models.DateField(_(u'Creation date'), auto_now_add=True, editable=False)
    currency = models.ForeignKey(Currency, related_name='accounts')
    archived = models.BooleanField(_(u'Is archived'), default=False)
    public = models.BooleanField(_(u'Is public'), default=False)

    class Meta:
        ordering = ('create', 'name')
        verbose_name = _(u'Account')
        verbose_name_plural = _(u'Accounts')

    def save(self, *args, **kwargs):
        # First save to have correct value
        super(Account, self).save(*args, **kwargs) # Call the "real" save() method

    def __unicode__(self):
        return u'%s - %s' % (self.owner, self.name)

class AccountGuests(models.Model):
    """
        Define what a user can do to an account.
    """
    account = models.ForeignKey(Account, related_name="guests")
    user = models.ForeignKey(User, related_name="guests")
    permissions = models.CharField(max_length=1, choices=PERMISSIONS, null=False, blank=False)
    currency = models.ForeignKey(Currency, related_name="guests", null=True, blank=True)

    class Meta:
        ordering = ('account', 'user')
        verbose_name_plural = _(u'Guests')
        verbose_name = _(u'Guest')

    def __unicode__(self):
        return u'%s' % (self.permissions)
