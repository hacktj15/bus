from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from .models import BusInstance, Bus, County, Slot, Coordinate


# Create your views here.


def display_view(request):
    """Displays the list of buses."""

    slots = Slot.objects.all()
    instances = BusInstance.objects.all()

    #for inst in instances:
    #    slots.remove(inst.slot)

    context = {
        "slots": slots,
        "instances": instances
    }
    return render(request, "display.html", context)


def modify_view(request):

    if request.method == 'POST' and 'action' in request.POST:
        act = request.POST.get('action')
        if act == 'modify_pos':
            try:
                bus = Bus.objects.get(id=request.POST.get('busid'))
            except (Bus.DoesNotExist, ValueError):
                # is title
                bus = Bus.objects.create(name=request.POST.get('busid'))

            businst = BusInstance.objects.get_or_create(
                bus=bus,
                arrived=False,
                slot=Slot.objects.get(id=request.POST.get('slotid'))
            )
            return HttpResponse("ok")

        if act == 'remove_inst':
            inst = BusInstance.objects.get(id=request.POST.get('id'))
            inst.delete()
            return HttpResponse("ok")



    slots = Slot.objects.all()
    instances = BusInstance.objects.all()
    buses = Bus.objects.all()

    #for inst in instances:
    #    slots.remove(inst.slot)

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
