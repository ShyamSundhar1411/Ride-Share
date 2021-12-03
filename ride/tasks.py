from celery import shared_task
from .models import RideHost,RidePool
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
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
    user = User.objects.get(pk = ride.user.id)
    host_email = user.email
    host_username = user.username
    html_message = render_to_string('ride/mail_template.html', {'ridepool': ridepool,'host_username':host_username})
    subject = 'Acceptance of Ride'
    message = EmailMessage(subject, html_message, me, [host_email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()
@shared_task(bind  = True)
def send_notification_on_cancellation(self,ride_id,cancelled_id):
    ride = RideHost.objects.get(pk = ride_id)
    ridepool = RidePool.objects.filter(id = cancelled_id,status = "CANCELLED")
    user = User.objects.get(pk = ride.user.id)
    host_username = user.username
    html_message = render_to_string('ride/mail_cancel_template.html', {'ridepool': ridepool,'host_username':host_username})
    host_email = user.email
    
    subject = 'Cancellation of Ride'
    message = EmailMessage(subject, html_message, me, [host_email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()
    
    