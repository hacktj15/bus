from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from .models import BusInstance, Bus, County, Slot, Coordinate


# Create your views here.


def display_view(request):
    """Displays the list of buses."""

    slots = list(Slot.objects.all())
    instances = BusInstance.objects.all()

    for inst in instances:
        slots.remove(inst.slot)

    context = {
        "slots": slots,
        "instances": instances
    }
    return render(request, "display.html", context)


def modify_view(request):

    if request.method == 'POST' and 'action' in request.POST:
        act = request.POST.get('action')
        if act == 'modify_pos':
            businst = BusInstance.objects.get_or_create(
                bus=Bus.objects.get(id=request.POST.get('busid')),
                arrived=False,
                slot=Slot.objects.get(id=request.POST.get('slotid'))
            )
            return HttpResponse("ok")



    slots = list(Slot.objects.all())
    instances = BusInstance.objects.all()
    buses = Bus.objects.all()

    for inst in instances:
        slots.remove(inst.slot)

    context = {
        "slots": slots,
        "instances": instances,
        "buses": buses
    }
    return render(request, "modify.html", context)

def login_view(request):
    """Displays the login page and processes authentication."""

    context = {}
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/modify')
        else:
            context["error"] = "Invalid username or password."

    return render(request, "login.html", context)
