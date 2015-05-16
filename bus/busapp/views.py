from django.shortcuts import render
from django.http import HttpResponseRedirect
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
    context = {}
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
