from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import User


def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

def user(request, id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=id)
            return HttpResponse("GET user with id {} - {}".format(id, user.user.first_name + " " + user.user.last_name))
        except User.DoesNotExist:
            raise Http404("User does not exist")
        
    elif request.method == "POST":
        return HttpResponse("POST user with id {}".format(id))