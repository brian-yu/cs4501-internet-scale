from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.urls import reverse
import urllib.request
import urllib.parse
import json

from web_frontend.forms import RegisterForm, CreateItemForm, LoginForm, UpdateProfileForm


def auth_render(req, template, args):  # for changing the login button to logout button
    auth = req.COOKIES.get('authenticator')
    if auth:
        args['logged_in'] = True
    return render(req, template, args)


def home(req):

    url = 'http://exp-api:8000/api/v1/'

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return auth_render(req, 'home.html', {'ok': False})

    resp['result']['ok'] = True

    return auth_render(req, 'home.html', resp['result'])

def id_from_auth(req):
    '''
    takes in a request object, accesses the authenticator cookie, and returns the corresponding user id
    returns None if either the authenticator did not exist or the the user was not logged in
    '''
    auth = req.COOKIES.get('authenticator')
    # if user is not logged in (auth is None), redirect to login page
    if not auth:
        return None #HttpResponseRedirect(reverse("login") + "?next=" + reverse("profile"))
    
    url = 'http://exp-api:8000/api/v1/users/getid/{}/'.format(auth)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp['ok'] == False:
        return None
    return resp['user_id']

def user(req, data):
    if type(data) is dict:
        id = data['id']
        myself = data['myself']
    else:
        id = data
        my_id = id_from_auth(req)
        if my_id == id:
            myself = True
        else:
            myself = False
    url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return auth_render(req, 'user.html', {'ok': False})

    resp['result']['ok'] = True
    resp['result']['myself'] = myself
    
    return auth_render(req, 'user.html', resp['result'])


def profile(req):
    auth = req.COOKIES.get('authenticator')
    # if user is not logged in (auth is None), redirect to login page
    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("profile"))
    
    id = id_from_auth(req)
    if id == None:
        return auth_render(req, 'user.html', {'ok': False})
    dic = {'myself': True, 'id': id}
    return user(req, dic)
    

def update_profile(req):
    auth = req.COOKIES.get('authenticator')
    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("update_profile"))
    url = 'http://exp-api:8000/api/v1/users/getid/{}/'.format(auth)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)
    if resp['ok']:
        id = resp['user_id']
    else:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("update_profile"))
    if req.method == "POST":
        form = UpdateProfileForm(req.POST)
        if not form.is_valid():
            return auth_render(req, "update_profile.html", {'form': form})
        post_data = form.cleaned_data
        post_data['authenticator'] = auth
        url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req2 = urllib.request.Request(url, data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req2).read().decode('utf-8')
        resp = json.loads(resp_json)
        if resp['ok']:
            return HttpResponseRedirect(reverse('profile'))
        return HttpResponseRedirect(reverse('update_profile'))
    else:
        form = UpdateProfileForm()
        args = {'form': form}
        return auth_render(req, "update_profile.html", args)


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
        return auth_render(req, 'review.html', {'ok': False})
    resp['result']['ok'] = True
    return auth_render(req, 'review.html', resp['result'])


def post_review(req, id):
    return HttpResponse('hello')


def register(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if not form.is_valid():
            form = RegisterForm()
            args = {'form': form}
            return auth_render(req, "register.html", args)
        post_data = form.cleaned_data
        url = 'http://exp-api:8000/api/v1/users/create/'
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req2 = urllib.request.Request(url, data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req2).read().decode('utf-8')
        resp = json.loads(resp_json)
        try:
            if not resp['ok']:
                if resp['error'] == "Email address already exists":
                    args = {'form': RegisterForm(
                    ), 'error': 'Email address already exists!'}
                    return auth_render(req, "register.html", args)
                result = json.dumps(
                    {'error': 'CREATE request did not pass through to exp and models layer. Here is the data we received: {}'.format(post_data), 'ok': False})
                return HttpResponse(result, content_type='application/json')
            form = LoginForm()
            args = {'form': form}
            # messages.success(req, 'Account successfully created!')
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

    redirect_to = req.GET.get('next')
    form = LoginForm(req.POST)
    if not form.is_valid():
        return auth_render(req, "login.html", {'form': form, 'next': redirect_to})

    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    n = redirect_to or reverse(home)

    data = {'email': email, 'password': password}
    url = 'http://exp-api:8000/api/v1/login/'
    post_encoded = urllib.parse.urlencode(data).encode('utf-8')
    exp_req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(exp_req).read().decode('utf-8')
    resp = json.loads(resp_json)

    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp['ok']:
        return auth_render(req, "login.html", {'form': LoginForm(), 'error': resp['error'], 'next': redirect_to})

    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    authenticator = resp['result']['authenticator']

    response = redirect(n)
    response.set_cookie("authenticator", authenticator)

    return response


def logout(req):
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('authenticator')
    # need to delete authenticator in the database backend
    return response


def post_item(req):
    auth = req.COOKIES.get('authenticator')
    # if user is not logged in (auth is None), redirect to login page
    if not auth:
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
                if resp['error'] == 'Invalid maximum borrow days': # user input 0 or a negative number
                    return auth_render(req, 'post_item.html', {'form': CreateItemForm(), 'error': 'Invalid maximum borrow days'})
                result = json.dumps({'error': 'CREATE request did not pass through to exp and models layer. Here is the data we received: {}'.format(
                    post_data), 'ok': False})
                return HttpResponse(result, content_type='application/json')
            new_item = resp['result']['id']
            url = 'http://exp-api:8000/api/v1/items/{}/'.format(new_item)
            resp_json = urllib.request.urlopen(url).read().decode('utf-8')
            resp = json.loads(resp_json)
            return redirect('/items/{}/'.format(resp['item']['id']))
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
        return auth_render(req, 'home.html', {'ok': False})

    resp['result']['ok'] = True

    return auth_render(req, 'all_items.html', resp['result'])


def search(req):
    query = req.GET.get('query')
    encoded_query = urllib.parse.urlencode({'query': query})
    url = 'http://exp-api:8000/api/v1/search/?{}'.format(encoded_query)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)
    ok = resp['ok']
    result = []
    if 'result' in resp:
        result = [i['_source'] for i in resp['result']]
    return auth_render(req, 'search.html', {'ok': ok, 'query': query, 'items': result})