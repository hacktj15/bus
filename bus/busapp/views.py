from django.shortcuts import render
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


def login_view(request):
    """Displays the login page and processes authentication."""

    context = {}
    return render(request, "login.html", context)