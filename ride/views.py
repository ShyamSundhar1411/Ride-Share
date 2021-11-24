from . models import RideHost,RidePool
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy,reverse
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
class HostRideEditView(LoginRequiredMixin,generic.UpdateView):
    model  = RideHost
    fields = ['start_point','destination','contact']
    template_name = "ride/HostRideEdit.html"
    def get_object(self):
        ride = super(HostRideEditView,self).get_object()
        if ride.user != self.request.user:
            raise Http404
        return ride
    def get_success_url(self):
        pk = self.kwargs["pk"]
        messages.success(self.request,'Updated Successfully')
        return reverse("edit_hosted_ride", kwargs={"pk": pk})

#Function Based
@login_required
def home(request):
    rides = RideHost.objects.all()
    return render(request,'ride/home.html',{'rides':rides})
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
@login_required
def deleteride(request,pk):
    accepted_ride = get_object_or_404(RideHost,id = pk)
    if request.method == "POST":
        accepted_ride.delete()
        messages.success(request,"Deleted Ride Successfully")
        return redirect("home")
    else:
        messages.error(request,"Error while processing request")
        return redirect("home")
