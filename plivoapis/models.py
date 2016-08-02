# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    auth_id = models.CharField(max_length=40, blank=True)
    username = models.CharField(max_length=30, blank=True)
    class Meta:
        managed = False
        db_table = 'account'

class PhoneNumber(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.CharField(max_length=40, blank=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'phone_number'


