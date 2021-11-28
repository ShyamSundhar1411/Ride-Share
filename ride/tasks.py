from celery import shared_task
from .models import RideHost,RidePool
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rideshare.settings import DEFAULT_FROM_EMAIL as me

@shared_task(bind = True)
def expirehostedride(self,ride_id,user_id):
    user = User.objects.get(pk = user_id)
    ride = RideHost.objects.get(pk = ride_id,user = user)
    ride.status = "EXPIRED"
    ride.save()
@shared_task(bind = True)
def send_notification_on_acceptance(self,ride_id):
    ride = RideHost.objects.get(pk = ride_id)
    ridepool = RidePool.objects.filter(ride = ride,status = "ACCEPTED")
    d1 = []
    user = User.objects.get(pk = ride.user.id)
    print(user)
    host_email = user.email
    print(host_email)
    for i in ridepool:
        str1 = 'Name:{},Email:{},Contact:{}'.format(i.user.username,i.user.email,i.user.profile.contact)
        d1.append([str1])
    print(d1)
    subject = 'Acceptance of Ride'
    content = '''Hi {}, Hope you are doing well. The following users have accepted your ride
    {}
    '''.format(ride.user.username,d1)
    send_mail(subject,content,me,[host_email])
@shared_task(bind  = True)
def send_notification_on_cancellation(self,ride_id):
    ride = RideHost.objects.get(pk = ride_id)
    ridepool = RidePool.objects.filter(ride = ride,status = "CANCELLED")
    d1 = []
    user = User.objects.get(pk = ride.user.id)
    print(user)
    host_email = user.email
    print(host_email)
    for i in ridepool:
        str1 = 'Name:{},Email:{},Contact:{}'.format(i.user.username,i.user.email,i.user.profile.contact)
        d1.append([str1])
    print(d1)
    subject = 'Cancellation of Ride'
    content = '''Hi {}, Hope you are doing well. The following users have accepted your ride
    {}
    '''.format(ride.user.username,d1)
    send_mail(subject,content,me,[host_email])
    