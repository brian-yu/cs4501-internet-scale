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

	score = sum([r['score'] for r in resp['received_reviews']]) / len(resp['received_reviews'])

	user = resp['user']
	items = resp['items']
	reviews = resp['received_reviews']

	return render(req, 'user.html', {'user': user, 'items': items, 'score': score})
