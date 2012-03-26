# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def home(request):
    data = {}
    user = request.user
    data['user'] = user
    if user.is_authenticated():     
        return render_to_response('main/home_loged.html', data)
    else:
        return render_to_response('main/home.html', data)
