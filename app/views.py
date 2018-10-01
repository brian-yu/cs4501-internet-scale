from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import User, Review, Borrow, Item
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import json


def index(request):
    return HttpResponse("Hello, world. You're at the app index.")


def get(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        obj_dict = model_to_dict( obj )
        result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')
    except model.DoesNotExist: # should never happen because we're always routing from a method
        result = json.dumps({'error': '{} not found'.format(type(model()).__name__), 'ok': False})
        return HttpResponse(result, content_type='application/json')

def user(request, id):
    if request.method == "GET":
        return get(request, User, id)
        
    elif request.method == "POST":
        return HttpResponse("POST user with id {}".format(id))

def item(request, id):
    if request.method == "GET":
        return get(request, Item, id)
        
    elif request.method == "POST":
        return HttpResponse("POST user with id {}".format(id))

def review(request, id):
    if request.method == "GET":
        return get(request, Review, id)
        
    elif request.method == "POST":
        return HttpResponse("POST user with id {}".format(id))

def borrow(request, id):
    if request.method == "GET":
        return get(request, Borrow, id)
        
    elif request.method == "POST":
        return HttpResponse("POST user with id {}".format(id))