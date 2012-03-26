# -*- coding: utf-8 -*-
from budget.models import Budget, Category
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from transactions.helpers import Transaction, get_similar

@csrf_exempt
@login_required
def add_transaction_ajax(request):
    result = {}
    user = request.user
    trans = Transaction()
    budgets = Budget.objects.filter(Q(owner=user) | Q(coowners=user))
    categories = Budget.objects.filter(Q(owner=user) | Q(coowners=user))

    trans.budget_name = request.POST.get('budget', '')
    trans.budget_id = request.POST.get('budget_id', 0)
    trans.category_name = request.POST.get('category', '')
    trans.category_id = request.POST.get('category_id', 0)
    trans.money = request.POST.get('money', '')
    trans.owner = user.username

    if trans.budget_id and \
        not budgets.filter(id=trans.budget_id).count():
            trans.budget_id = 0
    if trans.category_id and \
        not categories.filter(id=trans.category_id).count():
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

    trans.save_transaction()
    result['posted'] = True
    return HttpResponse(result, mimetype = 'application/javascript')
