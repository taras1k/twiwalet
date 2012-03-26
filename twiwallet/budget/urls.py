# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^budget_autocomplete/', 
            'budget.views.budget_autcomplete', name='budget_autcomplete'),
    url(r'^category_autocomplete/', 
            'budget.views.category_autcomplete', name='category_autcomplete'),
    url(r'^budget_list/', 
            'budget.views.get_budgets_json', name='budget_list'),
            
)

