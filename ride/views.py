from . models import RideHost,RidePool
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    rides = RideHost.objects.all()
    return render(request,'ride/home.html',{'rides':rides})
