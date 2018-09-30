from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import User
from django.forms.models import model_to_dict
import json


def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

def user(request, id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=id)
            user_json = json.dumps(model_to_dict( user ))
            return HttpResponse(user_json, content_type='application/json')
        except User.DoesNotExist:
            raise Http404("User does not exist")
        
    elif request.method == "POST":
        return HttpResponse("POST user with id {}".format(id))