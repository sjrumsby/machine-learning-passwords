from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def view(request):
    context = {}
    return render(request, 'main/view.html', context)

def create(request):
    context = {}
    return render(request, 'main/create.html', context)

def login(request):
    context = {}
    return render(request, 'main/login.html', context)

