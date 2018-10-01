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
        form_data = request.POST
        try:
            first_name = form_data['first_name']
            last_name = form_data['last_name']
            email = form_data['email']
            overview = form_data['overview']
            zip_code = form_data['zip_code']
            if 'phone_number' in form_data:
                phone_number = form_data['phone_number']
                obj = User.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone_number = phone_number,
                    overview = overview,
                    zip_code = zip_code
                )
            else:
                obj = User.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    overview = overview,
                    zip_code = zip_code
                )
            obj.save()
            obj_dict = model_to_dict( obj )
            result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
            return HttpResponse(result, content_type='application/json')
        except:
            result = json.dumps({'error': 'Missing field or malformed data in CREATE request', 'ok': False})
            return HttpResponse(result, content_type='application/json')

@csrf_exempt
def create_item(request):
    if request.method == "POST":
        form_data = request.POST
        try:
            owner = form_data['owner']
            title = form_data['title']
            condition = form_data['condition']
            description = form_data['description']
            price_per_day = form_data['price_per_day']
            max_borrow_days = form_data['max_borrow_days']
            obj = Item.objects.create(
                owner=owner,
                title=title,
                condition=condition,
                description=description,
                price_per_day=price_per_day,
                max_borrow_days=max_borrow_days
            )
            obj.save()
            obj_dict = model_to_dict( obj )
            result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
            return HttpResponse(result, content_type='application/json')
        except:
            result = json.dumps({'error': 'Missing field or malformed data in CREATE request', 'ok': False})
            return HttpResponse(result, content_type='application/json')

@csrf_exempt
def create_borrow(request):
    if request.method == "POST":
        form_data = request.POST
        try:
            lender = form_data['lender']
            borrower = form_data['borrower']
            item = form_data['item']
            borrow_date = form_data['borrow_date']
            borrow_days = form_data['borrow_days']
            obj = Borrow.objects.create(
                lender=lender,
                borrower=borrower,
                item=item,
                borrow_date=borrow_date,
                borrow_days=borrow_days
            )
            obj.save()
            obj_dict = model_to_dict( obj )
            result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
            return HttpResponse(result, content_type='application/json')
        except:
            result = json.dumps({'error': 'Missing field or malformed data in CREATE request', 'ok': False})
            return HttpResponse(result, content_type='application/json')


@csrf_exempt
def create_review(request):
    if request.method == "POST":
        form_data = request.POST
        try:
            reviewer = form_data['reviewer']
            reviewee = form_data['reviewee']
            text = form_data['text']
            score = form_data['score']
            obj = Review.objects.create(
                reviewer=reviewer,
                reviewee=reviewee,
                text=text,
                score=score
            )
            obj.save()
            obj_dict = model_to_dict( obj )
            result = json.dumps({'result': obj_dict, 'ok': True}, cls=DjangoJSONEncoder)
            return HttpResponse(result, content_type='application/json')
        except:
            result = json.dumps({'error': 'Missing field or malformed data in CREATE request', 'ok': False})
            return HttpResponse(result, content_type='application/json')