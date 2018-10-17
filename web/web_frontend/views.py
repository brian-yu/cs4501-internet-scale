from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'range': range(50)})