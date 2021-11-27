from celery import shared_task
from .models import RideHost
from django.http import HttpResponse
from django.contrib.auth.models import User

@shared_task(bind = True)
def expirehostedride(self,ride_id,user_id):
    user = User.objects.get(pk = user_id)
    ride = RideHost.objects.get(pk = ride_id,user = user)
    ride.status = "EXPIRED"
    ride.save()
    