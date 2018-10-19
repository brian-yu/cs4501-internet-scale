from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import urllib.request
import urllib.parse
import json


def home(req):
    url = 'http://models-api:8000/api/v1/featured_items/'

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp["ok"] == False:
        result = json.dumps({"ok": False}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')

    resp = resp['result']
    res = {}
    res['items'] = resp

    result = json.dumps({'ok': True, 'result': res}, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')


def users(req):
    return HttpResponse("<p>Users listing for exp_api!!</p>")


def user_detail(req, id):
    url = 'http://models-api:8000/api/v1/users/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp["ok"] == False:
        result = json.dumps({"ok": False}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')

    resp = resp['result']

    res = {}

    if len(resp['received_reviews']) == 0:
        res['score'] = "-"
    else:
        res['score'] = sum(
            [r['score'] for r in resp['received_reviews']]) / len(resp['received_reviews'])

    res['user'] = resp['user']
    res['items'] = resp['items']
    res['reviews'] = resp['received_reviews']

    result = json.dumps({'ok': True, 'result': res}, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')


def items(req):
    return HttpResponse("<p>Items listing for exp_api!!</p>")


def item_detail(req, id):
    url = 'http://models-api:8000/api/v1/items/{}/'.format(id)

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        result = json.dumps({"ok": False}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')

    owner = urllib.request.urlopen(
        'http://models-api:8000/api/v1/users/{}/'.format(resp['result']['owner'])).read().decode('utf-8')
    owner = json.loads(owner)['result']
    username = owner['user']['first_name'] + " " + owner['user']['last_name']
    resp['result']['user_name'] = username

    res = {}
    res['item'] = resp['result']
    res['ok'] = True
    result = json.dumps(res, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')


def reviews(req):
    url = 'http://models-api:8000/api/v1/all_reviews/'

    resp_json = urllib.request.urlopen(url).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['ok'] == False:
        result = json.dumps({"ok": False}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')
    # reviewer = json.loads(resp)['result']['reviewer']
    # text = json.loads(resp)['result']['text']
    # reviewee = json.loads(resp)['result']['reviewee']
    # score = json.loads(resp)['result']['score']

    result = json.dumps(resp, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')
