from django import forms
from . models import Profile, RideHost
from django.contrib.auth.models import User

class HostRideForm(forms.ModelForm):
    class Meta:
        model = RideHost
        fields = ['start_point','destination','contact']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','address','contact']