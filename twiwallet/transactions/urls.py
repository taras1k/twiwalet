# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^post_trans_ajax/', 
            'transactions.views.add_transaction_ajax', name='add_transaction_ajax'),
)

