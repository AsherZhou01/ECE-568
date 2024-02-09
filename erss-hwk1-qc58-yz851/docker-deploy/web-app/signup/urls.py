from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('driver/', views.signup_driver, name='signup_driver'),
    path('user/', views.signup_user, name='signup_user'),
    path('logged/', views.create_profile, name='create_profile'),
    path('logged/create_trip/', views.create_trip, name='create_trip'),
    path('logged/update_trip/<int:trip_id>/', views.update_trip, name='update_trip'),
    path('logged/trip_list/', views.trip_list, name='trip_list'),
    path('logged/trip_list/join_share_trip/', views.join_share_trip,name='join_share_trip'),
    path('logged/trip_list/driver_join_share_trip/', views.driver_join_share_trip,name='driver_join_share_trip'),
    path('logged/trip_list/share_search_results/', views.share_search_results,name='share_search_results'),
    path('logged/trip_list/driver_share_search_results/', views.driver_share_search_results, name='driver_share_search_results'),
    path('logged/trip_list/edit/<int:trip_id>/', views.edit_trip, name='edit_trip'),
    path('logged/detail_order/<int:trip_id>/', views.detail_order, name='detail_order'),
    path('logged/share_detail_order/<int:trip_id>/', views.share_detail_order, name='share_detail_order'),
    path('logged/driver_share_detail_order/<int:trip_id>/', views.driver_share_detail_order, name='driver_share_detail_order'),
    path('logged/add_share_passenger/<int:trip_id>/', views.add_shared_passenger, name='add_shared_passenger'),
    path('logged/driver_add_share_passenger/<int:trip_id>/', views.driver_add_shared_passenger, name='driver_add_shared_passenger')
]