from django.db import models

# Create your models here.

class County(models.Model):
    """Represents a county that a bus is associated with."""

    name = models.CharField(max_length=30)

class Bus(models.Model):
    """Represents a physical bus."""

    name = models.CharField(max_length=25)
    county = models.ForeignKey(County, null=True, blank=True)

class Coordinate(models.Model):
    """Represents an (x, y) coordinate."""

    x = models.IntegerField()
    y = models.IntegerField()

class Slot(models.Model):
    """Represents a possible location for a bus."""

    coord = models.ForeignKey(Coordinate)

class BusInstance(models.Model):
    """Represents a specific instance of a bus."""

    bus = models.ForeignKey(Bus)
    arrived = models.BooleanField()
    arrived_time = models.DateTimeField(null=True)
    slot = models.ForeignKey(Slot)
