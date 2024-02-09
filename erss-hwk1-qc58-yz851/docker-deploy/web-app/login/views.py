from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from signup.models import UserProfile
from django.shortcuts import render, redirect
from signup.models import UserProfile, Trip
from django.utils import timezone
from django.db.models import Q, F


# @login_required
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('account-number')
        password = request.POST.get('pwd')
        is_driver = 'darkmode' in request.POST
        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return render(request, 'login.html', {'show_modal': True, 'message': 'Account does not exist.'})

        if password == user.password:
            if is_driver != user.is_driver:
                return render(request, 'login.html', {'show_modal': True, 'message': 'Please check if you are driver.'})
            elif not is_driver:
                request.session['username'] = username
                return redirect(reverse('login_user'))
            else:
                request.session['username'] = username
                return redirect(reverse('login_driver'))  #need to be modified

        else:
            return render(request, 'login.html', {'show_modal': True, 'message': 'Password is incorrect.'})




# Create your views here.
def login(request):
    return render(request, "../templates/login.html")


def login_user(request):
    username = request.session.get('username', None)
    return render(request, "../templates/login_user.html",{"username": username})

# def login_driver(request):
#     trip_list = Trip.objects.all()
#     username = request.session.get('username', None)
#     return render(request, "../templates/login_driver.html", {"trip_list": trip_list, "username": username})
#
# def my_rides(request):
#     username = request.session.get('username', None)
#     trip_list = Trip.objects.all()
#     return render(request, "../templates/my_rides.html", {"trip_list": trip_list, "username": username})

def login_driver(request):
    username = request.session.get('username', None)
    driver = get_object_or_404(UserProfile, username=username)
    now = timezone.now()
    initial_trip_list = Trip.objects.filter(
        driver_profile__isnull=True,
        total_passenger__lte=driver.max_passenger_number,
    ).exclude(user_profile=driver)
    trip_list = [trip for trip in initial_trip_list if
                 trip.vehicle_type == 'any' or trip.vehicle_type == driver.vehicle_type]
    return render(request, "login_driver.html", {"trip_list": trip_list, "username": username})
def my_rides(request):
    username = request.session.get('username', None)
    user_profile = UserProfile.objects.get(username=username)
    trips_as_initiator = user_profile.trips.all()
    trips_as_passenger = user_profile.shared_trips.all()
    combined_trip_list = list(trips_as_initiator) + list(trips_as_passenger)
    trip_list_rider = list(set(combined_trip_list))

    username = request.session.get('username', None)
    if username is not None:
        user = get_object_or_404(UserProfile, username=username)
        trip_list_driver_completed = Trip.objects.filter(driver_profile=user) & Trip.objects.filter(status='completed')
        trip_list_driver = Trip.objects.filter(driver_profile=user) & Trip.objects.filter(status='confirmed')
        # trip_list_rider = Trip.objects.filter(user_profile=user)
    else:
        trip_list_driver = Trip.objects.none()
        trip_list_rider = Trip.objects.none()
        # trip_list_driver_completed = Trip.objects.none()
    return render(request, "../templates/my_rides.html", {"trip_list_driver": trip_list_driver,"trip_list_driver_completed": trip_list_driver_completed, "trip_list_rider": trip_list_rider, "username": username})


def request_ride_driver(request):
    username = request.session.get('username', None)
    return render(request, "../templates/driver_request_ride.html",{"username": username})

def confirm_order(request):
    if request.method == 'POST':
        username = request.session.get('username', None)
        driver = get_object_or_404(UserProfile, username=username)
        trip_id = request.POST.get('trip_id')
        trip_confirmed = get_object_or_404(Trip, id=trip_id)
        trip_confirmed.driver_profile = driver
        if trip_confirmed.status == 'open':
            trip_confirmed.status = 'confirmed'
        elif trip_confirmed.status == 'confirmed':
            trip_confirmed.status = 'completed'
        else:
            trip_confirmed.status = 'completed'
        trip_confirmed.save()
        now = timezone.now()
        trip_list = Trip.objects.filter(
            (Q(arriving_date__gt=now.date()) |
            (Q(arriving_date=now.date()) & Q(arriving_time__gt=now.time()))),
            driver_profile__isnull=True
        ).exclude(user_profile=driver)
        return render(request, 'login_driver.html', {'show_modal': True, 'message': 'You have successfully confirm this ride!.', "trip_list": trip_list, "username": username})

