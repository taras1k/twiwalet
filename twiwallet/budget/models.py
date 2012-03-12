# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Budget(models.Model):
    owner = models.ForeignKey(User, related_name='budget_owner')
    name = models.CharField(max_length=255)
    coowners = models.ManyToManyField(User, blank=True, null=True,
                                            related_name='coowners')
                                                
    def __unicode__(self):
        return self.name


class Category(models.Model):
    owner = models.ForeignKey(User, related_name='category_owner')
    name = models.CharField(max_length=255)
    budgets = models.ManyToManyField(Budget, blank=True, null=True,
                                            related_name='budget')
    def __unicode__(self):
        return self.name                                            