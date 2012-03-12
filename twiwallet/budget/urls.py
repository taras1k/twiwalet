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
    url(r'^post_trans_ajax/', 
            'budget.views.add_transaction_ajax', name='add_transaction_ajax'),
)

