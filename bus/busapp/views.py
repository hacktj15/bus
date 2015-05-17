import urllib.parse
import base64
import time
import json
import string
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import BusInstance, Bus, County, Slot, Coordinate, BusUser


# Create your views here.


def display_view(request):
    """Displays the list of buses."""

    slots = Slot.objects.all()
    instances = BusInstance.objects.all()

    num = len(slots) + len(instances)

    context = {
        "slots": slots,
        "instances": instances,
        "num": num,
        "loc": "display"
    }
    return render(request, "display.html", context)

@login_required
def buses_view(request):
    if not BusUser.is_admin(request.user):
        return HttpResponseRedirect("/?permission_denied")
    if request.method == 'POST' and 'action' in request.POST:
        act = request.POST.get('action')
        if act == 'modify_pos':
            if 'busid' in request.POST and request.POST.get('busid') != "new":
                busid = request.POST.get('busid')
                bus = Bus.objects.get(id=busid)
            if 'busname' in request.POST:
                bus = Bus.objects.create(name=request.POST.get('busname'))

            oinsts = BusInstance.objects.filter(bus=bus)
            if len(oinsts) > 0:
                for i in oinsts:
                    i.delete()
            businst = BusInstance.objects.get_or_create(
                bus=bus,
                arrived=False,
                slot=Slot.objects.get(id=request.POST.get('slotid'))
            )
            return HttpResponse("{"+('"instid":{}, "busid":{}'.format(
                businst[0].id, bus.id
            ))+"}")

        if act == 'remove_inst':
            try:
                inst = BusInstance.objects.get(id=request.POST.get('instid'))
                inst.delete()
            except (BusInstance.DoesNotExist, ValueError):
                return HttpResponse("dne")
            return HttpResponse("ok")

        if act == 'remove_all':
            insts = BusInstance.objects.all()
            for i in insts:
                i.delete()
            return HttpResponse("ok")



    slots = Slot.objects.all()
    instances = BusInstance.objects.all()
    buses = Bus.objects.all()

    num = len(slots) + len(instances)

    context = {
        "slots": slots,
        "instances": instances,
        "buses": buses,
        "num": num,
        "loc": "buses"
    }
    return render(request, "buses-modify.html", context)

@login_required
def map_view(request):
    if not is_admin(request.user):
        return HttpResponseRedirect("/?permission_denied")
    if request.method == 'POST' and 'action' in request.POST:
        act = request.POST.get('action')
        if act == 'remove_slot':
            slot = Slot.objects.get(id=request.POST.get('slotid'))
            slot.delete()
            return HttpResponse("ok")

        if act == 'remove_all':
            slots = Slot.objects.all()
            for slot in slots:
                slot.delete()
            return HttpResponse("ok")

        if act == 'save':
            id = request.POST.get('slotid')
            if id and id != "add":
                slot = Slot.objects.get(id=request.POST.get('slotid'))
                slot.rotate = request.POST.get('rot')
                slot.coord.x = request.POST.get('x')
                slot.coord.y = request.POST.get('y')
                slot.coord.save()
                slot.save()
            else:
                coord = Coordinate.objects.create(
                    x=request.POST.get('x'),
                    y=request.POST.get('y')
                )
                slot = Slot.objects.create(coord=coord)
            
            return HttpResponse("{}".format(slot.id))

    slots = Slot.objects.all()
    context = {
        "slots": slots,
        "loc": "map"
    }
    return render(request, "map.html", context)

def gen_iodine_reqtoken():
    data = {
        "title": "Bus Locator",
        "return": "http://127.0.0.1:8000/login",
        "time": int(time.time()),
        "exp": int(time.time() + 120),
        "method": "GET" # REQUIRED due to requirement for csrftoken in POST
    }

    datastr = urllib.parse.urlencode(data)
    reqtoken = base64.b64encode(datastr.encode('ascii'))

    return reqtoken

def process_iodine_token(sso):
    url = "https://iodine.tjhsst.edu/ajax/sso/valid_key?sso={}".format(sso)
    respstr = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(respstr)
    data = data["sso"]
    if data["valid_key"]:
        return setup_iodine_user(data["username"])

    return HttpResponse(respstr)

def setup_iodine_user(username):
    # password is never used
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        randpass = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))
        user = User.objects.create_user(username=username, email="{}@tjhsst.edu".format(username), password=randpass)

    obj = BusUser.objects.get_or_create(tjusername=username, user=user)
    return user

def setup_view(request):
    context = {
        "model": BusUser.objects.get(user=request.user),
        "buses": Bus.objects.all()
    }
    return render(request, "setup.html", context)

def login_view(request):
    """Displays the login page and processes authentication."""

    context = {}

    if 'sso' in request.GET:
        sso = request.GET.get('sso')
        user = process_iodine_token(sso)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return HttpResponseRedirect("/setup")

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/buses')
        else:
            context["error"] = "Invalid username or password."


    context["iodine_token"] = gen_iodine_reqtoken()

    return render(request, "login.html", context)

def logout_view(request):
    return logout(request, next_page="/")