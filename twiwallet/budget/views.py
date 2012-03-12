from django.shortcuts import render_to_response, HttpResponse
from helpers.autocomplete import search
from models import Budget, Category
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_transaction_ajax(request):
    result = {}
    result['budget'] = request.POST.get('budget', '')
    result['category'] = request.POST.get('category', '')
    result['money'] = request.POST.get('money', '')
    result['posted'] = True
    print result
    return HttpResponse(result, mimetype = 'application/javascript')

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