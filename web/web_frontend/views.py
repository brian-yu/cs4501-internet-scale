from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.urls import reverse
import urllib.request
import urllib.parse
import json

from web_frontend.forms import RegisterForm, CreateItemForm, LoginForm


def home(req):

    url = 'http://exp-api:8000/api/v1/'

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'home.html', {'ok': False})

    resp['result']['ok'] = True

    return render(req, 'home.html', resp['result'])


def user(req, id):
    url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'user.html', {'ok': False})

    resp['result']['ok'] = True

    return render(req, 'user.html', resp['result'])


def item(req, id):
    url = 'http://exp-api:8000/api/v1/items/{}/'.format(id)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    return render(req, 'item.html', resp)


def review(req, id):

    url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'review.html', {'ok': False})

    reviews = ""
    resp['result']['ok'] = True

    return render(req, 'review.html', resp['result'])


def register(req):

    if req.method == "POST":
        form = RegisterForm(req.POST)
        # if form.is_valid(): # this isn't right, we have to pass info to the exp and models
        # SEND TO EXP_API
        #     form.save()
        #     messages.success(req, 'Account created successfully')
        #     return redirect("login/")
        if not form.is_valid():
            form = RegisterForm()
            args = {'form': form}
            return render(req, "register.html", args)
        post_data = form.cleaned_data
        url = 'http://exp-api:8000/api/v1/users/create/'
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req2 = urllib.request.Request(url, data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req2).read().decode('utf-8')
        resp = json.loads(resp_json)
        try:
            if not resp['ok']:
                result = json.dumps(
                    {'error': 'CREATE request did not pass through to exp and models layer. Here is the data we received: {}'.format(post_data), 'ok': False})
                return HttpResponse(result, content_type='application/json')

            form = LoginForm()
            args = {'form': form}
            messages.success(req, 'Account successfully created!')

            response = render(req, "login.html", args)
            # response.set_cookie(key='authenticator', value=resp['result']['authenticator'])
            return response
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request because of exception. Here is the data we received: {}'.format(post_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')

    else:  # showing the form data with GET
        form = RegisterForm()
        args = {'form': form}
        return render(req, "register.html", args)


def login(req):
    if req.method == "POST":
        form = LoginForm(req.POST)
    else:
        form = LoginForm()
        args = {'form': form}
        return render(req, "login.html", args)


def post_item(req):
    if req.method == "POST":
        form_data = req.POST
        form = CreateItemForm(form_data)
        if not form.is_valid():
            form = CreateItemForm()
            args = {'form': form}
            return render(req, "post_item.html", args)
        url = 'http://exp-api:8000/api/v1/items/create/'
        post_encoded = urllib.parse.urlencode(form_data).encode('utf-8')
        req = urllib.request.Request(url, data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req)
        resp_json = resp_json.read().decode('utf-8')
        try:

            resp = json.loads(resp_json)
            if not resp['ok']:
                return render(req, "post_item.html", args)
            return HttpResponse(resp, content_type='application/json')
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request of web_frontend. Here is the data we received: {}'.format(form_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')

    else:
        form = CreateItemForm()
        args = {'form': form}
        return render(req, "post_item.html", args)
