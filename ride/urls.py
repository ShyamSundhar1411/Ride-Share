from . import views
from django.urls import path,include


urlpatterns = [
    path('create/',views.HostRide.as_view(),name = "create_ride"),
    path('accept/<int:pk>/',views.acceptride,name = "accept_ride"),
]
