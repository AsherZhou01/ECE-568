from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.login, name='login'),
    path('user/', views.login_user, name='login_user'),
    path('driver/', views.login_driver, name='login_driver'),
    path('admin/', admin.site.urls),
    path('checked/', views.log_in, name='check_log'),
    path('driver/myrides/', views.my_rides, name = "my_rides"),
    path('driver/comfirm_order/', views.confirm_order, name = "confirm_order"),
    path('driver/request_ride/', views.request_ride_driver, name = "request_ride_driver")

]