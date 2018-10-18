from django.shortcuts import render
import urllib.request
import urllib.parse
import json

def home(request):
    return render(request, 'home.html', {'range': range(50)})



def user(req, id):
	url = 'http://exp-api:8000/api/v1/users/{}/'.format(id)

	resp_json = urllib.request.urlopen(url).read().decode('utf-8')
	resp = json.loads(resp_json)

	if resp['ok'] == False:
		return render(req, 'user.html', {'ok': False})

	resp['result']['ok'] = True

	return render(req, 'user.html', resp['result'])
