from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

def user(request, id=None):
	if request.method == "GET":
		return HttpResponse("GET user with id {}".format(id))
	elif request.method == "POST":
		return HttpResponse("POST user with id {}".format(id))