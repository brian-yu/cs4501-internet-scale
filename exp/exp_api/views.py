from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import urllib.request
import urllib.parse
import json

def home(req, id):
	return HttpResponse("<p>Home for exp_api!!</p>")

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
		res['score'] = sum([r['score'] for r in resp['received_reviews']]) / len(resp['received_reviews'])

	res['user'] = resp['user']
	res['items'] = resp['items']
	res['reviews'] = resp['received_reviews']

	result = json.dumps({'ok': True, 'result': res}, cls=DjangoJSONEncoder)
	return HttpResponse(result, content_type='application/json')