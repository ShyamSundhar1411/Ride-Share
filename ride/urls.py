from . import views
from django.urls import path,include


urlpatterns = [
    path('',views.home,name = "home"),
    #HostARide
    path('create/',views.hostaride,name = "create_ride"),
    path('ride/<int:pk>/edit/<slug:slug>/',views.HostRideEditView.as_view(),name ="edit_hosted_ride"),
    path('delete/created/<int:pk>/ride',views.deleteride,name = "delete_hosted_ride"),
    #PoolARide
    path('accept/<int:pk>/',views.acceptride,name = "accept_ride"),
    path('cancel/accepted/ride/<int:pk>/',views.cancelride,name = "cancel_ride"),
    path('dashboard',views.dashboard,name = "dashboard"),
    path('dashboard/clear/history',views.clear_history,name = "clear_history")

]
