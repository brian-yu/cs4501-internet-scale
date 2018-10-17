from django.shortcuts import render
from django.http import HttpResponse

import urllib.request
import urllib.parse
import json

def home(req, id):
	return HttpResponse("<p>Home for exp_api!!</p>")

def users(req):
	return HttpResponse("<p>Users listing for exp_api!!</p>")

def user_detail(req, id):
	url = 'http://models-api:8000/api/v1/users/{}/'.format(id)

	# req = urllib.request.Request(url)

	resp_json = urllib.request.urlopen(url).read().decode('utf-8')
	resp = json.loads(resp_json)

	# r = requests.get(url)

	return HttpResponse("{}".format(resp_json))