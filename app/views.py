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
    except model.DoesNotExist: # should never happen because we're always routing from a method
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

def create(request, model, id):
    try:
        form_data = request.CREATE
        # check if all fields are present in request
        fields = model._meta.get_fields()
        required_fields = []
        for f in fields:
            if hasattr(f, 'blank') and f.blank == False:
                required_fields.append(f)
        for f in required_fields:
            if f not in form_data:
                result = json.dumps({'error': 'Field {} is not present in CREATE request'.format(f), 'ok': False})
                return HttpResponse(result, content_type='application/json')
        for f in required_fields:
        new_instance = model.objects.create()
        
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

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        return create(request, User)

@csrf_exempt
def create_item(request):
    if request.method == "POST":
        return create(request, Item)

@csrf_exempt
def create_borrow(request):
    if request.method == "POST":
        return create(request, Borrow)

@csrf_exempt
def create_review(request):
    if request.method == "POST":
        return create(request, Review)
