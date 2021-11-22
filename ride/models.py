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
