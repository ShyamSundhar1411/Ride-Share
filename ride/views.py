from . models import RideHost,RidePool
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
#Class Based
class HostRide(LoginRequiredMixin,generic.CreateView):
    model = RideHost
    fields = ['start_point','destination','contact']
    template_name = "ride/HostRide.html"
    success_url = reverse_lazy("home")
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(HostRide, self).form_valid(form)
#Function Based
@login_required
def home(request):
    rides = RideHost.objects.all()
    try:
        accepted_ride = RidePool.objects.get(user = request.user)
    except:
        accepted_ride = None
    if accepted_ride:
        a = True
    else:
        a = False
    return render(request,'ride/home.html',{'rides':rides,'isriding':a,"accepted_ride":accepted_ride})
@login_required
def acceptride(request,pk):
    accepted_ride = get_object_or_404(RideHost,id = pk)
    if request.method == "POST":
        if not RidePool.objects.filter(ride = accepted_ride,user = request.user).exists():
            RidePool.objects.create(
                user = request.user,
                ride = accepted_ride
            )
            return redirect("home")
        else:
            return redirect("create_ride")
    else:
        return redirect("create_ride")
@login_required
def cancelride(request,pk):
    accepted_pool_ride = get_object_or_404(RidePool,id = pk)
    if request.method == "POST":
        accepted_pool_ride.delete()
        messages.success(request,"Successfully cancelled your ride")
        return redirect("home")
    else:
        return redirect("home")
