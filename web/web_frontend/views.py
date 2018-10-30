from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import urllib.request
import urllib.parse
import json


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
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Account created successfully')
            return redirect("login/")

    else:
        form = UserCreationForm()
        args = {'form': form}
        return render(req, "register.html", args)


def login(req):
    return render(req, "login.html")
