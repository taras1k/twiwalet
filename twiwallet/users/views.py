# -*- coding: utf-8 -*-
import urllib
import simplejson
import random
import oauth2 as oauth
import cgi
import tweepy
import string
import mimetypes
import os
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from models import Profile

urllib.FancyURLopener.prompt_user_passwd = lambda self, host, realm: (uname, password)

consumer = oauth.Consumer(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET_KEY)
client = oauth.Client(consumer)

request_token_url = settings.TWITTER_REQUEST_TOKEN_URL
access_token_url = settings.TWITTER_ACCESS_TOKEN_URL

# This is the slightly different URL used to authenticate/authorize.
authenticate_url = settings.TWITTER_AUTHORIZATION_URL

def twitter_login(request):
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        return  HttpResponseRedirect('/')
    # Step 2. Store the request token in a session for later use.
    request_token = dict(cgi.parse_qsl(content))
    request.session['oauth_token'] = request_token['oauth_token']
    request.session['oauth_token_secret'] = request_token['oauth_token_secret']
    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url, request_token['oauth_token'])
    return HttpResponseRedirect(url)

@login_required
def twitter_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')



def twitter_authenticated(request):
    oauth_token = request.session.get('oauth_token',None)
    oauth_token_secret = request.session.get('oauth_token_secret', None)
    if oauth_token == None and oauth_token_secret == None:
        return  HttpResponseRedirect('/')

    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(oauth_token, oauth_token_secret)
    client = oauth.Client(consumer, token)
    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        return  HttpResponseRedirect('/')
    access_token = dict(cgi.parse_qsl(content))
    # Step 3. Lookup the user or create them if they don't exist.
    try:
        #user = User.objects.get(username=access_token['screen_name'])
        user = User.objects.get(username=access_token['user_id'])
    except User.DoesNotExist:
        # When creating the user I just use their screen_name@twitter.com
        # for their email and the oauth_token_secret for their password.
        # These two things will likely never be used. Alternatively, you 
        # can prompt them for their email here. Either way, the password 
        # should never be used.
        user = User.objects.create_user(access_token['user_id'], '%s@twitter.com' % access_token['screen_name'],
            access_token['oauth_token_secret'])
        # Save our permanent token and secret for later.
        profile = Profile()
        profile.user = user
        profile.twitter_username = access_token['screen_name']
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()
        

    # Authenticate the user and log them in using Django's pre-built 
    # functions for these things.
    if not user.check_password(access_token['oauth_token_secret']):
        user.set_password(access_token['oauth_token_secret'])
        user.save()
        profile = Profile.objects.get(user = user)
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    user = authenticate(username=access_token['user_id'], password=access_token['oauth_token_secret'])
    login(request, user)

    return HttpResponseRedirect('/')


