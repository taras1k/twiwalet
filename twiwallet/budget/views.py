# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, HttpResponse
from helpers.autocomplete import search
from models import Budget, Category
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from transactions.helpers import Transaction
import simplejson



def budget_autcomplete(request):    
    name = request.GET.get('budget','')
    result = {}
    user = request.user
    if user.is_authenticated() and len(name)>2:
        elements = Budget.objects.filter(name__icontains=name, owner = user)
        result = search(elements)
    return HttpResponse(result, mimetype = 'application/javascript')


def category_autcomplete(request):    
    name = request.GET.get('category','')
    result = {}
    user = request.user
    if user.is_authenticated() and len(name)>2:
        elements = Category.objects.filter(name__icontains=name, owner = user)
        result = search(elements)
    return HttpResponse(result, mimetype = 'application/javascript')


def get_budgets_json(request):
    result = {}
    data = []
    user = request.user
    if user.is_authenticated():
        trans = Transaction()
        budgets = Budget.objects.filter(Q(owner=user) | Q(coowners=user))
        for budget in budgets:
            data.append({'budget_id': budget.id,
                            'budget_name' : budget.name,
                            'budget_sum' : trans.get_budget_sum(budget.id) })
        result['budgets'] = data
    return HttpResponse(simplejson.dumps(result), mimetype = 'application/javascript')

