from django.shortcuts import render
from django.http import HttpResponse

def home(id):
	return HttpResponse("<p>Home for exp_api!!</p>")