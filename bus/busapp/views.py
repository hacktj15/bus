from django.shortcuts import render
from .models import BusInstance, Bus, County, Slot, Coordinate


# Create your views here.


def display_view(request):
    """Displays the list of buses."""

    instances = BusInstance.objects.all()
    context = {
        "instances": instances
    }
    return render(request, "display.html", context)