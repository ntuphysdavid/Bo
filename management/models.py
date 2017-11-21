from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username


class Inventory(models.Model):
    name = models.CharField('Part_number',max_length=128)
    price = models.CharField('Location',max_length=128)
    author = models.CharField('Product_Line',max_length=128)
    publish_date = models.DateField('Record Date')
    category = models.CharField('Category',max_length=128)
    description = models.CharField('Description',max_length=256)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField('name',max_length=128)
    description = models.TextField('description')
    img = models.ImageField('img',upload_to='image/%Y/%m/%d/')
    inventory = models.ForeignKey(Inventory)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class FA(models.Model):
    bugzilla = models.CharField(max_length=128)
    field_failure = models.CharField(max_length=128)
    date_of_received = models.DateField()
    part_description = models.CharField(max_length=128)
    part_number = models.CharField(max_length=128)
    rma_number = models.CharField(max_length=128)
    CT_number = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    comment = models.CharField(max_length=128)

    class META:
        ordering = ['bugzilla']

    def __unicode__(self):
        return self.Serial_Number
