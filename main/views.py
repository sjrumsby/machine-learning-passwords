import json

from django.shortcuts import render
from django.http import HttpResponse

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

#Begin API Ajax Things
def get_users(request):
    response_data = {
        "draw": 1,
        "recordsTotal": 1,
        "recordsFiltered": 1,
        "data": [
            [
                "sjrumsby",
                "Pancakes!",
            ]
        ]
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")
