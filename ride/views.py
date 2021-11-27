from . models import RideHost,RidePool
from . forms import HostRideForm, UserForm,ProfileForm
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.
#Class Based
class HostRideEditView(LoginRequiredMixin,generic.UpdateView):
    model  = RideHost
    fields = ['start_point','destination','contact']
    sluf_field = RideHost.slug
    template_name = "ride/HostRideEdit.html"
    def get_object(self):
        ride = super(HostRideEditView,self).get_object()
        if ride.user != self.request.user:
            raise Http404
        return ride
    def get_success_url(self):
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]
        messages.success(self.request,'Updated Successfully')
        return reverse("edit_hosted_ride", kwargs={"pk": pk,'slug':slug})

#Function Based
@login_required
def home(request):
    rides = RideHost.objects.filter(status = "OPEN")
    if RideHost.objects.filter(user = request.user,status = "OPEN").exists():
        isHost = True
    else:
        isHost = False
    try:
        accepted_ride = RidePool.objects.get(user = request.user,status = "ACCEPTED")
        isRiding = True
    except:
        accepted_ride = None
        isRiding = False
    return render(request,'ride/home.html',{'rides':rides,'isHost':isHost,'isRiding':isRiding,"accepted_ride":accepted_ride})
@login_required
def hostaride(request):
    ride = RideHost.objects.filter(user = request.user,status = "OPEN").exists()
    accepted_ride  = RidePool.objects.filter(user = request.user,status = "ACCEPTED").exists()
    if ride:
        messages.error(request,"You currently Hosted a ride wait till it expires.")
        return redirect("home")
    if accepted_ride:
        messages.error(request,"You are currently enrolled in a ride. Cancel the enrolled ride to continue hosting a ride")
        return redirect("home")
    else:
        if request.method == 'POST':
            hostride_form = HostRideForm(request.POST)
            if hostride_form.is_valid():
                ride = hostride_form.save(commit = False)
                ride.user = request.user
                ride.status = "OPEN"
                ride.save()
                messages.success(request,"Hosted a Ride successfully")
                return redirect("home")
            else:
                return render(request,"ride/hostride.html",{"form":hostride_form,"hostride_form_errors":hostride_form.errors})
        else:
            return render(request,"ride/hostride.html",{"form":HostRideForm()})
        
    
@login_required
def acceptride(request,pk):
    accepted_ride = get_object_or_404(RideHost,id = pk)
    if request.method == "POST":
        if not RidePool.objects.filter(ride = accepted_ride,status = "OPEN",user = request.user).exists():
            RidePool.objects.create(
                user = request.user,
                ride = accepted_ride,
                status = "ACCEPTED"
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
        accepted_pool_ride.status = "CANCELLED"
        accepted_pool_ride.isriding = False
        accepted_pool_ride.save()
        messages.success(request,"Successfully cancelled your ride")
        return redirect("home")
    else:
        messages.error(request,"Error while processing request")
        return redirect("home")
@login_required
def deleteride(request,pk):
    accepted_ride = get_object_or_404(RideHost,id = pk)
    if request.method == "POST":
        accepted_ride.status = "EXPIRED"
        accepted_ride.save()
        messages.success(request,"Expired Ride Successfully")
        return redirect("home")
    else:
        messages.error(request,"Error while processing request")
        return redirect("home")
@login_required
def profile(request,slug):
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance = request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('profile',slug = request.user.profile.slug)
        else:
            return render(request, 'account/profile.html', {'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})
    else:
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance = request.user.profile)
        return render(request,'account/profile.html',{'user_form':user_form,'profile_form':profile_form})