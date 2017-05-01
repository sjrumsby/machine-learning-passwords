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

def create_user(request):
    if request.method != "POST":
        resp = {"result": 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        resp = {"result": 0, "error_msg": "Both username and password are required fields"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    resp = {"result": 1}
    return HttpResponse(json.dumps(resp), content_type="application/json")


