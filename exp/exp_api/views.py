from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

import urllib.request
import urllib.parse
import json
import datetime
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


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


def all_items(req):
    url = 'http://models-api:8000/api/v1/all_items/'

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


def users(req):  # make this all users in the same zipcode
    return HttpResponse("<p>Hello there! Users listing for exp_api!!</p>")


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


@csrf_exempt
def login(req):
    if req.method != "POST":
        return JsonResponse({'ok': False, 'error': 'Invalid method'})
    post_data = req.POST
    url = 'http://models-api:8000/api/v1/login/'
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)


@csrf_exempt
def register(req):
    if req.method == "POST":
        post_data = req.POST
        try:
            url = 'http://models-api:8000/api/v1/users/create/'
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

            req = urllib.request.Request(url, data=post_encoded, method='POST')

            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            # if not resp['ok']:
            #     resp = json.dumps(
            #         {'error': 'Missing field or malformed data in CREATE request, did not get passed to models. Here is the data we received: {}'.format(post_data), 'ok': False})
            #     return HttpResponse(resp, content_type='application/json')
            return HttpResponse(json.dumps(resp))
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(post_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')


@csrf_exempt
def create_item(req):
    if req.method == "POST":
        post_data = req.POST
        try:
            url = 'http://models-api:8000/api/v1/items/create/'
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request(url, data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if not resp['ok']:
                if resp['error'] == 'Invalid maximum borrow days':
                    return JsonResponse({'ok': False, 'error': 'Invalid maximum borrow days'})
                resp = json.dumps(
                    {'error': 'Missing field or malformed data in CREATE request for model service. Here is the data we received: {}'.format(post_data), 'ok': False})
                return HttpResponse(resp, content_type='application/json')
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            producer.send('new-items-topic',
                          json.dumps(resp['result']).encode('utf-8'))
            return JsonResponse(resp)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request for experience service. Here is the data we received: {}'.format(post_data), 'ok': False})
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

    res = {}
    condition = resp['result']['item']['condition']
    if condition == 'E':
        resp['result']['item']['condition'] = 'Excellent'
    elif condition == 'G':
        resp['result']['item']['condition'] = 'Good'
    elif condition == 'O':
        resp['result']['item']['condition'] = 'Fair'
    else:
        resp['result']['item']['condition'] = 'Poor'
    res['item'] = resp['result']['item']

    borrows = resp['result']['borrows']  # the 5 most recent borrows
    for borrow in borrows:
        borrow['borrow_date'] = datetime.datetime.strftime(
            datetime.datetime.strptime(borrow['borrow_date'][:10], "%Y-%m-%d"), "%B %d, %Y")
    res['borrows'] = resp['result']['borrows']

    res['user_name'] = resp['result']['owner']
    res['ok'] = True
    result = json.dumps(res, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')


def search(req, query):
    es = Elasticsearch(['es'])
    query = query.replace("+", " ")

    res = es.search(index='items_index', body={
                    'query': {'query_string': {'query': query}}, 'size': 10})
    return JsonResponse({'ok': True, 'result': res['hits']['hits']})
    # return JsonResponse({'ok': True, 'result': []})
