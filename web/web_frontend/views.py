from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.urls import reverse
import urllib.request
import urllib.parse
import json

from web_frontend.forms import RegisterForm, CreateItemForm, LoginForm


def auth_render(req, template, args): # for changing the login button to logout button
    auth = req.COOKIES.get('authenticator')
    if auth:
       args['logged_in'] = True 
    return render(req, template, args)

def home(req):

    url = 'http://exp-api:8000/api/v1/'

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'home.html', {'ok': False})

    resp['result']['ok'] = True

    return auth_render(req, 'home.html', resp['result'])


def user(req, id):
    url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'user.html', {'ok': False})

    resp['result']['ok'] = True

    return auth_render(req, 'user.html', resp['result'])


def item(req, id):
    url = 'http://exp-api:8000/api/v1/items/{}/'.format(id)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    return auth_render(req, 'item.html', resp)


def review(req, id):

    url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'review.html', {'ok': False})

    reviews = ""
    resp['result']['ok'] = True

    return auth_render(req, 'review.html', resp['result'])


def register(req):

    if req.method == "POST":
        form = RegisterForm(req.POST)
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
                if resp['error'] == "Email address already exists":
                    args = {'form': RegisterForm(), 'error': 'Email address already exists!'}
                    return auth_render(req, "register.html", args)
                result = json.dumps(
                    {'error': 'CREATE request did not pass through to exp and models layer. Here is the data we received: {}'.format(post_data), 'ok': False})
                return HttpResponse(result, content_type='application/json')
            form = LoginForm()
            args = {'form': form}
            messages.success(req, 'Account successfully created!')
            response = auth_render(req, "login.html", args)
            return response
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request because of exception. Here is the data we received: {}'.format(post_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')

    else:  # showing the form data
        form = RegisterForm()
        args = {'form': form}
        return auth_render(req, "register.html", args)


def login(req):
    if req.method == "GET":
        form = LoginForm()
        n = req.GET.get('next') or reverse(home)
        return auth_render(req, "login.html", {'form': form, 'next': n})

    form = LoginForm(req.POST)
    if not form.is_valid():
        return auth_render(req, "login.html", {'form': form})

    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    n = form.cleaned_data.get('next') or reverse(home)

    data = {'email': email, 'password': password}
    url = 'http://exp-api:8000/api/v1/login/'
    post_encoded = urllib.parse.urlencode(data).encode('utf-8')
    exp_req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(exp_req).read().decode('utf-8')
    resp = json.loads(resp_json)

    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp['ok']:
        return auth_render(req, "login.html", {'form': LoginForm(), 'error': resp['error']})

    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    authenticator = resp['result']['authenticator']

    response = redirect(n)
    response.set_cookie("authenticator", authenticator)

    return response

def logout(req):
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('authenticator')
    return response

def post_item(req):
    auth = req.COOKIES.get('authenticator')
    if not auth: # if user is not logged in (auth is None), redirect to login page
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))

    if req.method == "POST":
        form = CreateItemForm(req.POST)
        if not form.is_valid():
            args = {'form': form}
            return auth_render(req, "post_item.html", args)
        post_data = form.cleaned_data
        post_data['authenticator'] = auth
        url = 'http://exp-api:8000/api/v1/items/create/'
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req2 = urllib.request.Request(url, data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req2).read().decode('utf-8')

        try:
            resp = json.loads(resp_json)
            if not resp['ok']:
                if resp['error'] == 'Invalid maximum borrow days':
                    return auth_render(req, 'post_item.html', {'form': CreateItemForm(), 'error': 'Invalid maximum borrow days'})
                result = json.dumps({'error': 'CREATE request did not pass through to exp and models layer. Here is the data we received: {}'.format(
                    post_data), 'ok': False})
                return HttpResponse(result, content_type='application/json')
            new_item = resp['result']['id']
            url = 'http://exp-api:8000/api/v1/items/{}/'.format(new_item)
            resp_json = urllib.request.urlopen(url).read().decode('utf-8')
            resp = json.loads(resp_json)

        
            return render(req, 'item.html', resp)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request of web_frontend. Here is the data we received: {}'.format(post_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')

    else:
        form = CreateItemForm()
        args = {'form': form}
        return auth_render(req, "post_item.html", args)

def all_items(req):
    url = 'http://exp-api:8000/api/v1/all_items'

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'home.html', {'ok': False})

    resp['result']['ok'] = True

    return auth_render(req, 'all_items.html', resp['result'])

def search(req):
    query = req.GET.get('query')
    url = 'http://exp-api:8000/api/v1/search/{}/'.format(query)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)
    ok = resp['ok']
    result = [i['_source'] for i in resp['result']]
    return auth_render(req, 'search.html', {'ok': ok, 'query': query, 'items': result})