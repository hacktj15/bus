from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import BusInstance, Bus, County, Slot, Coordinate


# Create your views here.


def display_view(request):
    """Displays the list of buses."""

    slots = Slot.objects.all()
    instances = BusInstance.objects.all()

    num = len(slots) + len(instances)

    context = {
        "slots": slots,
        "instances": instances,
        "num": num
    }
    return render(request, "display.html", context)

@login_required
def buses_view(request):
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



    slots = Slot.objects.all()
    instances = BusInstance.objects.all()
    buses = Bus.objects.all()

    num = len(slots) + len(instances)

    context = {
        "slots": slots,
        "instances": instances,
        "buses": buses,
        "num": num
    }
    return render(request, "buses-modify.html", context)

@login_required
def map_view(request):
    if request.method == 'POST' and 'action' in request.POST:
        act = request.POST.get('action')
        if act == 'remove_slot':
            slot = Slot.objects.get(id=request.POST.get('slotid'))
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
        "slots": slots
    }
    return render(request, "map.html", context)

def login_view(request):
    """Displays the login page and processes authentication."""

    context = {}
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/buses')
        else:
            context["error"] = "Invalid username or password."

    return render(request, "login.html", context)

def logout_view(request):
    return logout(request, next_page="/")