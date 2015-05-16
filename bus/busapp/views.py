from django.shortcuts import render
from .models import BusInstance, Bus, County, Slot, Coordinate


# Create your views here.


def display_view(request):
    """Displays the list of buses."""

    slots = Slot.objects.all()
    instances = BusInstance.objects.all()
    context = {
        "slots": slots,
        "instances": instances
    }
    return render(request, "display.html", context)