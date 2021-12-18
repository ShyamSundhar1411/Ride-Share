from . models import RideHost,RidePool
from . forms import HostRideForm, UserForm,ProfileForm
from . tasks import send_notification_on_acceptance,send_notification_on_cancellation,send_notification_on_expiration_to_pools
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from phonenumber_field.modelfields import PhoneNumberField
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
    fields = ['start_point','destination','contact','start_time','seats']
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
    rides = RideHost.objects.filter(status = "OPEN").order_by('-creation_time')
    participants = None
    if RideHost.objects.filter(user = request.user,status = "OPEN").exists():
        ride = RideHost.objects.filter(user = request.user,status = "OPEN").order_by('-creation_time')[0]
        if RidePool.objects.filter(ride = ride,status = "ACCEPTED").exists():
            participants = RidePool.objects.filter(ride = ride,status = "ACCEPTED")
        else:
            participants = None
        isHost = True
    else:
        isHost = False
    try:
        accepted_ride = RidePool.objects.get(user = request.user,status = "ACCEPTED")
        isRiding = True
    except:
        accepted_ride = None
        isRiding = False
    return render(request,'ride/home.html',{'rides':rides,'isHost':isHost,'isRiding':isRiding,"accepted_ride":accepted_ride,'participants':participants})
@login_required
def hostaride(request):
    if not(request.user.profile.contact):
        messages.info(request, "Add your contact to continue to host your ride. Until then you will be prompted for the same.")
        return redirect("profile",slug = request.user.profile.slug)
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
                return render(request,"ride/createride.html",{"form":hostride_form,"hostride_form_errors":hostride_form.errors})
        else:
            return render(request,"ride/createride.html",{"form":HostRideForm()})
        
    
@login_required
def acceptride(request,pk):
    accepted_ride = RideHost.objects.get(id = pk)
    if request.method == "POST":
        if not RidePool.objects.filter(ride = accepted_ride,status = "OPEN",user = request.user).exists() and  not accepted_ride.available > accepted_ride.seats:
            if not RidePool.objects.filter(ride = accepted_ride,user = request.user).exists():
                RidePool.objects.create(
                    user = request.user,
                    ride = accepted_ride,
                    status = "ACCEPTED"
                )
                accepted_ride.seats -=1  
                accepted_ride.save()
                send_notification_on_acceptance(pk)
                if request.user.profile.contact:
                    messages.success(request,"Accepted the Ride")
                    return redirect("home")
                else:
                    messages.info(request,"Accepted the Ride. Add Contact Number for Best Experience")
                    return redirect("profile",slug = request.user.profile.slug)
            else:
                accepted_pool = RidePool.objects.get(user = request.user,ride = accepted_ride)
                accepted_pool.status = "ACCEPTED"
                accepted_pool.save()
                accepted_ride.seats -=1  
                accepted_ride.save()
                send_notification_on_acceptance(pk)
                if request.user.profile.contact:
                    messages.success(request,"Accepted the Ride")
                    return redirect("home")
                else:
                    messages.info(request,"Accepted the Ride. Add Contact Number for Best Experience")
                    return redirect("profile",slug = request.user.profile.slug)
        else:
            messages.error(request,"Error while processing request.")
            return redirect("home")
    else:
        return redirect("create_ride")
@login_required
def cancelride(request,pk):
    accepted_pool_ride = RidePool.objects.get(id=pk)
    accepted_ride = RideHost.objects.get(id = accepted_pool_ride.ride.id)
    if request.method == "POST":
        accepted_pool_ride.status = "CANCELLED"
        accepted_pool_ride.isriding = False
        accepted_pool_ride.save()
        accepted_ride.seats+=1
        accepted_ride.save()
        messages.success(request,"Successfully cancelled your ride")
        send_notification_on_cancellation(accepted_pool_ride.ride.id,accepted_pool_ride.id)
        return redirect("home")
    else:
        messages.error(request,"Error while processing request")
        return redirect("home")
@login_required
def deleteride(request,pk):
    accepted_ride = RideHost.objects.get(id = pk)
    if request.method == "POST":
        accepted_ride.status = "EXPIRED"
        if RidePool.objects.filter(ride = accepted_ride).exists():
            pool_mails = RidePool.objects.filter(ride = accepted_ride,status = "ACCEPTED")
            email_l = []
            for i in pool_mails:
                email = i.user.email
                email_l.append(email)
            RidePool.objects.filter(ride = accepted_ride).update(status = "EXPIRED",isriding = False)
            send_notification_on_expiration_to_pools(email_l,pk)
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
@login_required
def dashboard(request):
    hostedrides = RideHost.objects.filter(user = request.user).order_by('-creation_time')
    hosted_ride_page = request.GET.get('hosted_ride_page', 1)
    hosted_ride_paginator = Paginator(hostedrides,4)
    hosted_ride_count = hosted_ride_paginator.count
    acceptrides = RidePool.objects.filter(user = request.user).order_by('-update_time')
    accepted_ride_page = request.GET.get('accepted_ride_page', 1)
    accepted_ride_paginator = Paginator(acceptrides,4)
    accepted_ride_count = accepted_ride_paginator.count
    try:
        hostedrides = hosted_ride_paginator.page(hosted_ride_page)
    except PageNotAnInteger :
        hostedrides = hosted_ride_paginator.page(1)

    except EmptyPage:
        hostedrides = hosted_ride_paginator.page(hosted_ride_paginator.num_pages)

    try:
        acceptrides = accepted_ride_paginator.page(accepted_ride_page)
    except PageNotAnInteger :
        acceptrides = accepted_ride_paginator.page(1)
    except EmptyPage:
        acceptrides = accepted_ride_page.page(accepted_ride_paginator.num_pages)
    return render(request,'ride/dashboard.html',{"hosted_rides":hostedrides,"accepted_rides":acceptrides,'hosted_ride_count':hosted_ride_count,'accepted_ride_count':accepted_ride_count})
@login_required
def clear_history(request):
    hostedrides = RideHost.objects.filter(user = request.user).delete()
    acceptedrides = RidePool.objects.filter(user = request.user).delete()
    messages.success(request,"History Cleared")
    return redirect("dashboard")
    
    