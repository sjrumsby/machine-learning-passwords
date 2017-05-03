import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import *

def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def search(request):
    context = {}
    return render(request, 'main/search.html', context)

def create(request):
    context = {}
    return render(request, 'main/create.html', context)

def train(request):
    context = {}
    return render(request, 'main/train.html', context)

def test(request):
    context = {}
    return render(request, 'main/test.html', context)

#Begin API Ajax Things
def get_users(request):
    try:
        draw = request.GET['draw']
    except KeyError:
        draw = 1

    users = Machine_User.objects.select_related().all()
    filteredUsers = users.filter()
    
    response_data = {
        "draw": draw,
        "recordsTotal": users.count(),
        "recordsFiltered": filteredUsers.count(),
        "data": [
        ]
    }
   
    columns = ["username", "password", "status"]
    order_dir = request.GET.get("order[0][dir]")
    
    try:
        order_ind = int(request.GET.get("order[0][column]"))
    except ValueError:
        order_ind = 0

    if order_ind >= len(columns):
        order_ind = 0

    order_col = columns[order_ind]

    if order_dir == "desc":
        order_col = "-" + order_col

    filteredUsers = filteredUsers.order_by(order_col)

    response_data['order_col'] = order_col

    for u in filteredUsers:
        response_data['data'].append([u.username, u.password, u.status.description])

    return HttpResponse(json.dumps(response_data), content_type="application/json")

#We're explicitly creating a public site - no CSRF required
@csrf_exempt
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

    status = User_Status.objects.get(description="Untrained")
    u = Machine_User.objects.create(username=username, password=password, status=status)

    resp = {"result": 1}
    return HttpResponse(json.dumps(resp), content_type="application/json")


