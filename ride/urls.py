from . import views
from django.urls import path,include


urlpatterns = [
    #HostARide
    path('create/',views.HostRide.as_view(),name = "create_ride"),
    path('ride/<int:pk>/edit/',views.HostRideEditView.as_view(),name ="edit_hosted_ride"),
    path('delete/created/<int:pk>/ride',views.deleteride,name = "delete_hosted_ride"),
    #PoolARide
    path('accept/<int:pk>/',views.acceptride,name = "accept_ride"),
    path('cancel/accepted/ride/<int:pk>/',views.cancelride,name = "cancel_ride"),

]
