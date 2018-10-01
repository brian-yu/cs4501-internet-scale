from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import User, Review, Borrow, Item
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return HttpResponse("Hello, world. You're at the app index.")


def get(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        obj_dict = model_to_dict( obj )
        result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')
    except model.DoesNotExist:
        result = json.dumps({'error': '{} not found'.format(type(model()).__name__), 'ok': False})
        return HttpResponse(result, content_type='application/json')

def update(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        form_data = request.POST
        for item in form_data.items():
            setattr(obj, item[0], item[1])
        obj.save()
        obj_dict = model_to_dict( obj )
        result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
        return HttpResponse(result, content_type='application/json')
    except model.DoesNotExist:
        result = json.dumps({'error': '{} not found'.format(type(model()).__name__), 'ok': False})
        return HttpResponse(result, content_type='application/json')

def delete(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        obj.delete()
        result = json.dumps({'ok': True})
        return HttpResponse(result, content_type='application/json')
    except model.DoesNotExist:
        result = json.dumps({'error': '{} not found'.format(type(model()).__name__), 'ok': False})
        return HttpResponse(result, content_type='application/json')

@csrf_exempt
def user(request, id):
    if request.method == "GET":
        return get(request, User, id)
        
    elif request.method == "POST":
        return update(request, User, id)

@csrf_exempt
def item(request, id):
    if request.method == "GET":
        return get(request, Item, id)
        
    elif request.method == "POST":
        return update(request, Item, id)

@csrf_exempt
def review(request, id):
    if request.method == "GET":
        return get(request, Review, id)
        
    elif request.method == "POST":
        return update(request, Review, id)

@csrf_exempt
def borrow(request, id):
    if request.method == "GET":
        return get(request, Borrow, id)
        
    elif request.method == "POST":
        return update(request, Borrow, id)

@csrf_exempt
def delete_user(request, id):
    if request.method == "DELETE":
        return delete(request, User, id)

@csrf_exempt
def delete_item(request, id):
    if request.method == "DELETE":
        return delete(request, Item, id)

@csrf_exempt
def delete_borrow(request, id):
    if request.method == "DELETE":
        return delete(request, Borrow, id)

@csrf_exempt
def delete_review(request, id):
    if request.method == "DELETE":
        return delete(request, Review, id)
