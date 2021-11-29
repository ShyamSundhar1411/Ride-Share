import random
import json
import uuid
from django.db import models
from .choices import Host_Status_Choices,Pool_Status_Choices
from django.dispatch import receiver
from django.core.validators import MaxValueValidator,MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_celery_beat.models import PeriodicTask,CrontabSchedule

# Create your models here.
class RideHost(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    contact = PhoneNumberField()
    start_point = models.CharField(max_length = 500,null = True,blank = True)
    destination = models.CharField(max_length = 500,null = True,blank = True)
    creation_time = models.DateTimeField(auto_now_add = True)
    start_time = models.TimeField(editable = True)
    status = models.CharField(max_length = 500,choices = Host_Status_Choices,default = "EXPIRED")
    seats = models.PositiveIntegerField(default = 1,validators = [MaxValueValidator(10),MinValueValidator(0)])
    available = models.PositiveIntegerField(default = 1,validators = [MaxValueValidator(10),MinValueValidator(0)])
    slug = models.SlugField(blank = True)
    def __str__(self):
        return str(self.contact)+'-'+str(self.destination)
    def save(self,*args,**kwargs):
        if self.contact is None:
            self.contact = self.user.profile.contact
        if not self.slug:
            self.slug = uuid.uuid4()
        super(RideHost,self).save(*args,**kwargs)
class RidePool(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    ride = models.ForeignKey(RideHost,on_delete = models.CASCADE)
    status = models.CharField(max_length = 500,choices = Pool_Status_Choices,default = "CANCELLED")
    isriding = models.BooleanField(default = False,null = True,blank = True)
    update_time = models.DateTimeField(auto_now = True)
    def __str__(self):
        string = str(self.ride.start_point)+'-'+str(self.ride.destination)+'-'+str(self.ride.id)
        return string
    def save(self,*args,**kwargs):
        if not self.isriding:
            self.isriding = True
        super(RidePool,self).save(*args,**kwargs)
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    avatar = models.ImageField(blank = True,upload_to = "avatar/")
    slug = models.SlugField(blank = True,unique = True)
    address = models.TextField(max_length = 500,null = True,blank = True)
    contact = PhoneNumberField(blank = True)
    
    def __str__(self):
        return self.user.username
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Profile,self).save(*args,**kwargs)
@receiver(post_save,sender = RideHost)
def create_expiration_for_ride(sender,instance,created,**kwargs):
    if created:
        schedule,created = CrontabSchedule.objects.get_or_create(hour = 6)
        task_name = "Expire_Ride Automatically"+str(instance.slug)
        task = PeriodicTask.objects.create(crontab = schedule,name = task_name,task = "ride.tasks.expirehostedride",args = json.dumps([instance.id,instance.user.id]))
@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance)
        instance.profile.save()
@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()