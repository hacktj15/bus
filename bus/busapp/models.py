from django.db import models

# Create your models here.

class County(models.Model):
    """Represents a county that a bus is associated with."""

    name = models.CharField(max_length=30)

    def __unicode__(self):
        return "{}".format(self.name)

class Bus(models.Model):
    """Represents a physical bus."""

    name = models.CharField(max_length=25)
    county = models.ForeignKey(County, null=True, blank=True)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.county)

class Coordinate(models.Model):
    """Represents an (x, y) coordinate."""

    x = models.IntegerField()
    y = models.IntegerField()

    def __unicode__(self):
        return "({}, {})".format(self.x, self.y)

class Slot(models.Model):
    """Represents a possible location for a bus."""

    coord = models.ForeignKey(Coordinate)
    rotate = models.IntegerField(default=0) # between 0-360

    def style(self):
        pos = "left: {}px; top: {}px".format(self.coord.x, self.coord.y)
        if self.rotate != 0:
            for vend in ["-ms-", "-webkit-", ""]:
                pos += "; transform: {}rotate({}deg)".format(vend, self.rotate)

        return pos

    def __unicode__(self):
        return "{}".format(self.coord)

class BusInstance(models.Model):
    """Represents a specific instance of a bus."""

    bus = models.ForeignKey(Bus)
    arrived = models.BooleanField(default=False)
    arrived_time = models.DateTimeField(null=True)
    slot = models.ForeignKey(Slot)

    def __unicode__(self):
        return "{} - {}".format(self.bus, self.slot)
