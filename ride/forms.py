from django import forms
from . models import Profile, RideHost
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.models import User

class HostRideForm(forms.ModelForm):
    start_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    class Meta:
        model = RideHost
        fields = ['start_point','destination','contact','start_time','seats']
class UserForm(forms.ModelForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
class ProfileForm(forms.ModelForm):
    contact = PhoneNumberField(required = True)
    class Meta:
        model = Profile
        fields = ['avatar','address','contact']