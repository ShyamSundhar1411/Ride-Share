from celery import shared_task
from .models import RideHost,RidePool
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage,send_mail
from rideshare.settings import DEFAULT_FROM_EMAIL as me
@shared_task(bind = True)
def send_notification_on_expiration_to_host(self,ride_id,user_id):
    ride = RideHost.objects.get(pk = ride_id)
    user = User.objects.get(pk = user_id)
    user_mail = user.email
    start_point = ride.start_point
    destination = ride.destination
    start_time = ride.start_time
    subject = 'Expiration of Ride'
    content = '''Hello {} hope you are doing well. We are Sorry to inform you that your ride from {} to {} which was about to start by {} has been expired automatically by our website norms
    Thank You
    Best Regards
    '''.format(user.username,start_point,destination,start_time)
    message = EmailMessage(subject, content, me, [user_mail])
    message.send()
@shared_task(bind = True)
def send_notification_on_expiration_to_pools(self,email_list,ride_id):
    ride = RideHost.objects.get(pk = ride_id)
    start_point = ride.start_point
    destination = ride.destination
    start_time = ride.start_time
    subject = "Expiration of Ride"
    content = '''Hi, Hope you are doing well. We are Sorry to inform you that your ride from {} to {} which was about to start by {} was either expired by user or expired automatically by our website norms.
    Thank You
    Best Regards
    '''.format(start_point,destination,start_time)
    send_mail(subject,content,me,email_list)
@shared_task(bind = True)
def expirehostedride(self,ride_id,user_id):
    user = User.objects.get(pk = user_id)
    ride = RideHost.objects.get(pk = ride_id,user = user)
    if RidePool.objects.filter(ride = ride,status = "ACCEPTED").exists():
        pool_mails = RidePool.objects.filter(ride = ride,status = "ACCEPTED")
        email_l = []
        for i in pool_mails:
            email = i.user.email
            email_l.append(email)
        RidePool.objects.filter(ride = ride,status = "ACCEPTED").update(status = "EXPIRED",isriding = False)
        send_notification_on_expiration_to_pools(email_l,ride_id)
    if ride.status == "OPEN":
        ride.status = "EXPIRED"
        send_notification_on_expiration_to_host(ride_id,user_id)
        ride.save()
    else:
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


