from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.
class RideHost(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    contact = PhoneNumberField()
    start_point = models.CharField(max_length = 500,null = True,blank = True)
    destination = models.CharField(max_length = 500,null = True,blank = True)
    creation_time = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return str(self.contact)+'-'+str(self.destination)
class RidePool(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    ride = models.ForeignKey(RideHost,on_delete = models.CASCADE)
    isriding = models.BooleanField(default = False,null = True,blank = True)

    def __str__(self):
        string = str(self.ride.start_point)+'-'+str(self.ride.destination)+'-'+str(self.ride.id)
        return string
    def save(self,*args,**kwargs):
        if not self.isriding:
            self.isriding = True
        super(RidePool,self).save(*args,**kwargs)
