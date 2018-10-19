from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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

    reviews_list = resp['result']['reviews']
    paginator = Paginator(reviews_list, 5)
    # page = request.GET.get('page')
    # reviews = paginator.get_page(page)
    reviews = ""
    resp['result']['ok'] = True

    return render(req, 'user.html', resp['result'])


def review(req, id):
    # url = 'http://exp-api:8000/api/v1/all_reviews/'

    # resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    # resp = json.loads(resp_json)

    # if resp['ok'] == False:
    #     return render(req, 'review.html', {'ok': False})

    # resp['result']['ok'] = True

    url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        return render(req, 'user.html', {'ok': False})

    reviews_list = resp['result']['reviews']
    paginator = Paginator(reviews_list, 5)
    # page = request.GET.get('page')
    # reviews = paginator.get_page(page)
    reviews = ""
    resp['result']['ok'] = True

    return render(req, 'review.html', resp['result'])

    # return render(req, 'review.html', resp)


def item(req, id):
    url = 'http://exp-api:8000/api/v1/items/{}/'.format(id)
    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    return render(req, 'item.html', resp)
