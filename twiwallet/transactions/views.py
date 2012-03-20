# -*- coding: utf-8 -*-
import jellyfish
from transactions.models import TransactionModel
from budget.models import Budget, Category
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

JARO_SIMULARITY = 0.88

class Transaction(object):

    def __init__(self):
        self.budget_id = 0
        self.budget = ''
        self.category_id = 0
        self.category = ''
        self.money = 0
        self.description = ''
        self.owner = None

def get_similar(queryset, criteria):
    if not queryset.count():
        return 0
    result = {element.id:jellyfish.jaro_distance(element.name.encode('utf8'), 
                    criteria.encode('utf8')) for element in queryset}
    max_simular = max(result, key=result.get)
    if result[max_simular] > JARO_SIMULARITY:
        return max_simular
    else:
        return 0

@csrf_exempt
@login_required
def add_transaction_ajax(request):
    result = {}
    user = request.user
    result = {}
    trans = Transaction()
    budgets = Budget.objects.filter(Q(owner=user) | Q(coowners=user))
    categories = Budget.objects.filter(Q(owner=user) | Q(coowners=user))

    trans.budget_name = request.POST.get('budget', '')
    trans.budget_id = request.POST.get('budget_id', 0)
    trans.category_name = request.POST.get('category', '')
    trans.category_id = request.POST.get('category_id', 0)
    trans.money = request.POST.get('money', '')
    trans.owner = user.username

    print trans.budget_name
    print trans.budget_id
    print trans.category_name
    print trans.category_id
    print trans.money
    print trans.owner

    if trans.budget_id :
        if not budgets.filter(id=trans.budget_id).count():
            trans.budget_id = 0
    if trans.category_id :
        if not categories.filter(id=trans.category_id).count():
            trans.category_id = 0

    if not trans.budget_id and trans.budget_name:
        trans.budget_id = get_similar(budgets, trans.budget_name)
        if not trans.budget_id:
            budget = Budget(owner=user, name=trans.budget_name)
            budget.save()
            trans.budget_id = budget.id
    if not trans.category_id and trans.category_name:
        trans.category_id = get_similar(categories, trans.category_name)
        if not trans.category_id:
            category = Category(owner=user, name=trans.category_name)
            category.save()
            trans.category_id = category.id
    save_transaction(trans)
    result['posted'] = True
    return HttpResponse(result, mimetype = 'application/javascript')


def save_transaction(transaction):
    t = TransactionModel(transaction.owner,
                        transaction.budget_id,
                        transaction.category_id,
                        transaction.money,
                        transaction.description)    
    t.save()
