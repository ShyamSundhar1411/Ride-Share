from . models import RideHost,RidePool
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.
#Class Based
class HostRide(generic.CreateView):
    model = RideHost
    fields = ['start_point','destination','contact']
    template_name = "ride/HostRide.html"
    success_url = reverse_lazy("home")
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(HostRide, self).form_valid(form)
#Function Based
def home(request):
    rides = RideHost.objects.all()
    return render(request,'ride/home.html',{'rides':rides})
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
