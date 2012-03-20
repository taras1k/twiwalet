# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def home(request):
    if request.user.is_authenticated():
        return render_to_response('main/home_loged.html')
    else:
        return render_to_response('main/home.html')
