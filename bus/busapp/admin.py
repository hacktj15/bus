from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([
    models.County,
    models.Bus,
    models.Coordinate,
    models.Slot,
    models.BusInstance
])