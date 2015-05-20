from .models import BusUser
from django.contrib.auth.models import User
def is_admin(request):
    """Add whether the user is an admin."""
    if request.user and request.user.is_authenticated():
        try:
            bususer = BusUser.objects.get(user__id=request.user.id)
        except BusUser.DoesNotExist:
            bususer = BusUser.objects.create(user=request.user)
        admin = bususer.admin
    else:
        admin = False
    return {"is_admin": admin}