from django import forms
from . models import Profile, RideHost
from django.contrib.auth.models import User

class HostRideForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    class Meta:
        model = RideHost
        fields = ['start_point','destination','contact','start_time','seats']
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','address','contact']