from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import User, Review, Borrow, Item, Authenticator
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
import os
import hmac
from django.conf import settings


def index(request):
    return HttpResponse("Hello, world. You're at the app index (used for api calls to the database).")


def jsonResponse(dic=None):
    if dic == None:
        result = json.dumps({'ok': True})
    else:
        result = json.dumps({'result': dic, 'ok': True}, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')


def jsonErrorResponse(model_name, id):
    result = json.dumps(
        {'error': '{} with id={} not found'.format(model_name, id), 'ok': False})
    return HttpResponse(result, content_type='application/json')


def formatErrorResponse(jsonInput):
    result = json.dumps(
        {'error': 'json input {} was not valid'.format(jsonInput), 'ok': False})
    return HttpResponse(result, content_type='application/json')


def get(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        obj_dict = model_to_dict(obj)
        return jsonResponse(obj_dict)
    except model.DoesNotExist:  # should never happen because we're always routing from a method
        return jsonErrorResponse(type(model()).__name__, id)


def update(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        form_data = request.POST
        for key, value in form_data.items():
            if key in {'owner', 'lender', 'reviewer', 'reviewee', 'borrower'}:
                try:
                    value = User.objects.get(pk=value)
                except:
                    return jsonErrorResponse("User", value)
            if key == 'item':
                try:
                    value = Item.objects.get(pk=value)
                except:
                    return jsonErrorResponse("Item", value)
            if key == 'score':
                try:
                    value = int(value)
                except ValueError:
                    return formatErrorResponse(form_data)
                if not value >= 1 or not value <= 5:
                    return formatErrorResponse(form_data)
            setattr(obj, key, value)
        obj.save()
        obj_dict = model_to_dict(obj)
        obj_dict.pop('password', None)
        return jsonResponse(obj_dict)
    except ValidationError:
        return formatErrorResponse(form_data)
    except model.DoesNotExist:
        return jsonErrorResponse(type(model()).__name__, id)


def delete(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        obj.delete()
        return jsonResponse()
    except model.DoesNotExist:
        return jsonErrorResponse(type(model()).__name__, id)


def serialize_borrows(borrows, key):
    return [
        {
            'item': model_to_dict(m.item),
            key: model_to_dict(getattr(m, key)),
            'borrow_date': m.borrow_date,
            'borrow_days': m.borrow_days,
        } for m in borrows
    ]

@csrf_exempt
def user(request, id):
    if request.method == "GET":
        try:
            obj = User.objects.get(pk=id)
            obj_dict = {}
            obj_dict['user'] = model_to_dict(obj)

            obj_dict['items'] = [model_to_dict(m)for m in list(obj.item_set.all())]

            obj_dict['borrows'] = serialize_borrows(list(obj.borrowed_items.all()), 'lender')

            obj_dict['lends'] = serialize_borrows(list(obj.borrowed_items.all()), 'borrower')

            obj_dict['received_reviews'] = serialize_reviews(list(obj.received_reviews.all()))
            # [model_to_dict(m) for m in list(obj.received_reviews.all())]

            return jsonResponse(obj_dict)
        except User.DoesNotExist:  # should never happen because we're always routing from a method
            return jsonErrorResponse('User', id)

    elif request.method == "POST":
        return update(request, User, id)

def serialize_reviews(reviews):
    return [
        {
            'reviewer': model_to_dict(m.reviewer),
            'reviewee': model_to_dict(m.reviewee),
            'text': m.text,
            'score': m.score,
        } for m in reviews
    ]

def serialize_borrows_item(borrows):
    return [
                {
                    'lender': model_to_dict(m.lender),
                    'borrower': model_to_dict(m.borrower),
                    'borrow_date': m.borrow_date,
                    'borrow_days': m.borrow_days,
                } for m in borrows
            ]

@csrf_exempt
def item(request, id):
    if request.method == "GET":
        try:
            obj = Item.objects.get(pk=id)
            obj_dict = {}
            obj_dict['item'] = model_to_dict( obj )
            obj_dict['owner'] = obj.owner.first_name + " " + obj.owner.last_name
            obj_dict['borrows'] = serialize_borrows_item(list(Borrow.objects.filter(item=obj.id).order_by('-borrow_date')[:5]))
            return jsonResponse(obj_dict)
        except Item.DoesNotExist: # should never happen because we're always routing from a method
            return jsonErrorResponse(type(Item()).__name__, id)
            
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
            password = form_data['password']
            if len(User.objects.filter(email=email)) > 0:
                return JsonResponse({'ok': False, 'error': "Email address already exists"})
            if 'phone_number' in form_data:
                phone_number = form_data['phone_number']
                obj = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    overview=overview,
                    zip_code=zip_code,
                    password=make_password(password),
                    lender_rating_total=0,
                    lender_rating_count=0,
                    borrower_rating_total=0,
                    borrower_rating_count=0
                )
            else:
                obj = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    overview=overview,
                    zip_code=zip_code,
                    password=make_password(password),
                    lender_rating_total=0,
                    lender_rating_count=0,
                    borrower_rating_total=0,
                    borrower_rating_count=0
                )
            obj.save()

            authenticator = hmac.new(
                key = settings.SECRET_KEY.encode('utf-8'),
                msg = os.urandom(32),
                digestmod = 'sha256',
            ).hexdigest()
            my_auth = Authenticator.objects.create(
                user_id=obj,
                authenticator=authenticator,
            )
            obj_dict = model_to_dict(obj)
            obj_dict.pop('password')
            return jsonResponse(obj_dict)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(form_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')


@csrf_exempt
def create_item(request):
    if request.method == "POST":
        form_data = request.POST
        try:
            if 'owner' in form_data: # backwards compatibility for Postman testing
                owner_id = form_data['owner']
                owner = User.objects.get(id=owner_id)
            else:
                authenticator = form_data['authenticator']
                try: #checking if the authenticator is valid
                    auth_obj = Authenticator.objects.get(authenticator=authenticator)
                    owner = auth_obj.user_id
                except: # Authenticator.DoesNotExist exception
                    return JsonResponse({'error': 'invalid authenticator', 'ok': False})
            title = form_data['title']
            condition = form_data['condition']
            description = form_data['description']
            price_per_day = form_data['price_per_day']
            max_borrow_days = int(form_data['max_borrow_days'])
            if max_borrow_days < 1:
                return JsonResponse({'ok': False, 'error': 'Invalid maximum borrow days'})
            currently_borrowed = form_data['currently_borrowed'] if 'currently_borrowed' in form_data else False
            obj = Item.objects.create(
                owner=owner,
                title=title,
                condition=condition,
                description=description,
                price_per_day=price_per_day,
                max_borrow_days=max_borrow_days,
                currently_borrowed=currently_borrowed
            )
            obj.save()
            obj_dict = model_to_dict(obj)
            return jsonResponse(obj_dict)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(form_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')


@csrf_exempt
def create_borrow(request):
    if request.method == "POST":
        form_data = request.POST
        try:
            # can probably change this so you get the lender_id from the Item object
            # might depend on frontend implementation
            lender_id = form_data['lender']
            lender = User.objects.get(id=lender_id)
            borrower_id = form_data['borrower']
            borrower = User.objects.get(id=borrower_id)
            item_id = form_data['item']
            item = Item.objects.get(id=item_id)
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
            obj_dict = model_to_dict(obj)
            return jsonResponse(obj_dict)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(form_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')


@csrf_exempt
def create_review(request):
    if request.method == "POST":
        form_data = request.POST
        try:
            reviewer_id = form_data['reviewer']
            reviewer = User.objects.get(id=reviewer_id)
            # reviewer_name = reviewer.first_name
            reviewee_id = form_data['reviewee']
            reviewee = User.objects.get(id=reviewee_id)
            text = form_data['text']
            score = form_data['score']
            obj = Review.objects.create(
                reviewer=reviewer,
                reviewee=reviewee,
                text=text,
                score=score
            )
            obj.save()
            obj_dict = model_to_dict(obj)
            return jsonResponse(obj_dict)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(form_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')


def featured_items(req):
    res = []
    for item in list(Item.objects.all().order_by('-id')[:12]):
        d = model_to_dict(item)
        d['owner'] = model_to_dict(User.objects.get(pk=d['owner']))
        res.append(d)
    return jsonResponse(res)

def all_items(req):
    res = []
    for item in list(Item.objects.all().order_by('-id')):
        d = model_to_dict(item)
        d['owner'] = model_to_dict(User.objects.get(pk=d['owner']))
        res.append(d)
    return jsonResponse(res)

@csrf_exempt
def check_login(req):
    if req.method == "POST":
        form_data = req.POST

        #try:
        email = form_data['email']
        password = form_data['password']
        users = User.objects.filter(email=email)
        if len(users) == 1:
            if check_password(password, users[0].password):
                auth = Authenticator.objects.get(user_id=users[0]).authenticator
                return jsonResponse({'authenticator': auth})
            else:
                # password doesn't match
                return JsonResponse({'error': 'Username or password is invalid', 'ok': False})
        else:
            # email doesn't match
            return JsonResponse({'error': 'Username or password is invalid', 'ok': False})

