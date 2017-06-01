import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import *

import logging
logger = logging.getLogger(__name__)

def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def search(request):
    context = {}
    return render(request, 'main/search.html', context)

def create(request):
    context = {}
    return render(request, 'main/create.html', context)

def redirect(request):
    return HttpResponseRedirect('/search')

def train_select(request):
    users = Machine_User.objects.filter(status__description='Untrained')
    context = {"users": users}
    return render(request, 'main/train_select.html', context)

def train(request, user_id):
    try:
        user = Machine_User.objects.get(id=user_id)
    except Machine_User.DoesNotExist:
        return HttpResponseRedirect("/train")
    context = {"user": user}

    return render(request, 'main/train.html', context)

def test(request):
    context = {}
    return render(request, 'main/test.html', context)

#Begin API Ajax Things
@csrf_exempt
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if username == None or password == None:
        resp = {"result": 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    u = Machine_User.objects.filter(username=username, password=password)

    if u.count() == 1:
        resp = {"result": 1}
    else:
        resp = {"result": 0}

    return HttpResponse(json.dumps(resp), content_type="application/json")
        

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
        links = ''

        if u.status.description == "Untrained":
            links += '<a href="/train/%s">Train User</a>' % u.id
        else:
            links += '<a href="/test/%s">Test User</a>' % u.id
        response_data['data'].append([u.username, u.password, u.status.description, links])

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

@csrf_exempt
def save_analysis(request):
    if request.method != "POST":
        resp = {"result": 0}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    try:
        username = request.POST['username']
        password = request.POST['password']
        keyStrokes = json.loads(request.POST['keyStrokes'])
    except KeyError:
        resp = {"result": 0, "error_msg": "All 3 of username, password, and keyStrokes are required fields"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    try:
        u = Machine_User.objects.get(username=username)
    except Machine_User.DoesNotExist:
        resp = {"result": 0, "error_msg": "That username does not exist"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    if u.password != password:
        resp = {"result": 0, "error_msg": "Password does not match"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    keyStrokeUsername = ""
    keyStrokePassword = ""

    for k in keyStrokes:
        if k['action'] == "keypress":
            if k['keyCode'] not in [9,13]:
                c = k['key']

                if k['element'] == "username":
                    keyStrokeUsername += c
                else:
                    keyStrokePassword += c

    if keyStrokeUsername != username or keyStrokePassword != password:
        logger.info(keyStrokeUsername)
        logger.info(keyStrokePassword)
        resp = {"result": 0, "error_msg": "key stroke analysis failed to validate the username and password"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    totalTime = keyStrokes[-1]['time'] - keyStrokes[0]['time']
    tabPressed = False
    enterPressed = False

    for k in keyStrokes:
        if k['keyCode'] == 9:
            tabPressed = True
        if k['keyCode'] == 13:
            enterPressed = True

    userSig = User_Signature.objects.create(machine_user=u, tab_pressed=tabPressed, enter_pressed=enterPressed, total_time=totalTime)

    for i in range(len(keyStrokes)):
        if keyStrokes[i]['action'] == 'keypress':
            currentKeyCode = keyStrokes[i]['keyCode']
        else:
            continue

        #Get the start press time
        for j in range(i, -1, -1):
            logger.info(j)
            if keyStrokes[j]['action'] == 'keydown':
                startTime = keyStrokes[j]['time']
                break

        #Get the end lift time
        for j in range(i, len(keyStrokes)):
            if keyStrokes[j]['action'] == 'keyup':
                endTime = keyStrokes[j]['time']
                break

        holdTime = endTime - startTime

        Key_Stroke.objects.create(user_signature=userSig, letter=currentKeyCode, hold_time=holdTime)

        

        

    resp = {"result": 1}
    return HttpResponse(json.dumps(resp), content_type="application/json")















