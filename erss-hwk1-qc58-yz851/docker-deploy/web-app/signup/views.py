from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import UserProfile, Trip
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.db.models import Q, Count, F

# @login_required
def create_profile(request):
    if request.method == 'POST':
        username = request.POST.get('account-number')
        password = request.POST.get('pwd')
        vehicle_type = request.POST.get('vehicle-type', '')
        is_driver = (vehicle_type != '')
        license_number = request.POST.get('license-plate-number', '')
        max_passenger_number = request.POST.get('max-num-passenger', 0)

        profile = UserProfile(
            username=username,
            password=password,  # 在实际应用中，应该加密密码
            is_driver=is_driver,
            vehicle_type=vehicle_type,
            license_number=license_number,
            max_passenger_number=max_passenger_number
        )
        profile.save()
        return redirect(reverse('index'))

@require_http_methods(["POST"])
# @login_required
def create_trip(request):
    if request.method == 'POST':
        current_location = request.POST.get('current-location')
        destination_address = request.POST.get('destination-address')
        departure_date = request.POST.get('departure-date')
        departure_time = request.POST.get('departure-time')
        total_passenger = request.POST.get('total-passenger')
        vehicle_type = request.POST.get('vehicle-type', 'any')
        is_shared = 'share_ride' in request.POST

        response_message = "Current logged-in user's username: " + request.user.username
        username = request.session.get('username')
        try:
            user_profile = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            response_message += " | User profile does not exist."
            return HttpResponse(response_message, status=404)

        # 创建并保存新的行程记录
        trip = Trip(
            user_profile=user_profile,
            current_location=current_location,
            destination=destination_address,
            arriving_date=departure_date,
            arriving_time=departure_time,
            total_passenger=total_passenger,
            is_share=is_shared,
            vehicle_type=vehicle_type
        )
        trip.save()

        if not user_profile.is_driver:
            return redirect('trip_list')
        else:
            return redirect('my_rides')
        # return HttpResponse("Successful request", status=200)

@require_http_methods(["POST"])
# @login_required
def update_trip(request, trip_id):
    if request.method == 'POST':
        # 获取表单数据
        current_location = request.POST.get('current-location', '')
        destination_address = request.POST.get('destination-address', '')
        departure_date = request.POST.get('departure-date', '')
        departure_time = request.POST.get('departure-time', '')
        total_passenger = request.POST.get('total-passenger', 1)
        vehicle_type = request.POST.get('vehicle-type', 'any')
        is_shared = 'share_ride' in request.POST

        # 获取当前登录的用户的UserProfile
        # user_profile = get_object_or_404(UserProfile, user=request.user)
        #
        # # 查找并更新Trip记录
        # trip = get_object_or_404(Trip, pk=trip_id, user_profile=user_profile)
        username = request.session.get('username')
        try:
            user_profile = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            # UserProfile不存在时的自定义错误消息
            return HttpResponse("UserProfile does not exist for the logged-in user.", status=404)

        try:
            trip = Trip.objects.get(pk=trip_id, user_profile=user_profile)
        except Trip.DoesNotExist:
            # Trip不存在时的自定义错误消息
            return HttpResponse("Trip with the given ID does not exist for the current user.", status=404)

        trip.current_location = current_location
        trip.destination = destination_address
        trip.arriving_date = departure_date
        trip.arriving_time = departure_time
        trip.total_passenger = total_passenger
        trip.is_share = is_shared
        trip.vehicle_type = vehicle_type
        trip.save()

        # 可以选择重定向到某个页面，或者返回一个成功的响应
        return redirect('trip_list')

    # 如果不是POST请求，可能需要处理其他逻辑或返回错误响应
    return HttpResponse("Invalid request", status=400)

def trip_list(request):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)
    trips_as_initiator = user_profile.trips.all()
    trips_as_passenger = user_profile.shared_trips.all()
    combined_trip_list = list(trips_as_initiator) + list(trips_as_passenger)
    trip_list = list(set(combined_trip_list))
    return render(request, "../templates/trip_list.html", {"trip_list": trip_list, "username": username})

def edit_trip(request, trip_id):
    username = request.session.get('username', None)
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'edit_trip.html', {'trip': trip, "username": username})
    # return render(request, "../templates/edit_trip.html", {"trip_list": trip_list, "username": username})

def detail_order(request, trip_id):
    button_text = "Confirm"
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)
    is_driver = user_profile.is_driver
    trip = get_object_or_404(Trip, pk=trip_id)
    if trip.driver_profile and username == trip.driver_profile.username:
        button_text = "Complete"
    return render(request, 'detail_order.html', {'trip': trip, "username": username, "button_text": button_text, "is_driver":is_driver})

def share_detail_order(request, trip_id):
    button_text = "Join"
    username = request.session.get('username', None)
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'share_detail_order.html', {'trip': trip, "username": username, "button_text": button_text})

def driver_share_detail_order(request, trip_id):
    button_text = "Join"
    username = request.session.get('username', None)
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'driver_share_detail_order.html', {'trip': trip, "username": username, "button_text": button_text})

# @login_required
def join_share_trip(request):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)
    # trip_list_share = Trip.objects.filter(is_share=True, status='open').exclude(shared_passenger=user_profile)
    trip_list_share = Trip.objects.annotate(
        shared_passenger_count=Count('shared_passenger')
    ).filter(
        is_share=True,
        status='open',
        shared_passenger_count__lt=F('total_passenger') - 1  # 确保加上当前用户后不会超过最大乘客数
    ).exclude(
        shared_passenger=user_profile  # 排除当前用户已经是共享乘客的行程
    )
    return render(request, 'join_share_trip.html',{"trip_list_share": trip_list_share, "username": username})

# @login_required
def driver_join_share_trip(request):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)
    # trip_list_share = Trip.objects.filter(is_share=True, status='open').exclude(shared_passenger=user_profile)
    trip_list_share = Trip.objects.annotate(
        shared_passenger_count=Count('shared_passenger')
    ).filter(
        is_share=True,
        status='open',
        shared_passenger_count__lt=F('total_passenger') - 1  # 确保加上当前用户后不会超过最大乘客数
    ).exclude(
        shared_passenger=user_profile  # 排除当前用户已经是共享乘客的行程
    )
    return render(request, 'driver_join_share_trip.html',{"trip_list_share": trip_list_share, "username": username})


def add_shared_passenger(request, trip_id):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)
    trip = get_object_or_404(Trip, pk=trip_id)
    trip.shared_passenger.add(user_profile)
    trip.save()
    trips_as_initiator = user_profile.trips.all()
    trips_as_passenger = user_profile.shared_trips.all()
    combined_trip_list = list(trips_as_initiator) + list(trips_as_passenger)
    trip_list = list(set(combined_trip_list))
    return render(request, 'trip_list.html', {'trip_list': trip_list, "username": username})

def driver_add_shared_passenger(request, trip_id):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)
    trip = get_object_or_404(Trip, pk=trip_id)
    trip.shared_passenger.add(user_profile)
    trip.save()
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
    return render(request, "../templates/my_rides.html",
                  {"trip_list_driver": trip_list_driver, "trip_list_driver_completed": trip_list_driver_completed,
                   "trip_list_rider": trip_list_rider, "username": username})


# def share_search_results(request):
#     username = request.session.get('username', None)
#     destination = request.GET.get('destination')
#     arrival_start = request.GET.get('arrival_start')
#     arrival_end = request.GET.get('arrival_end')
#     passengers = request.GET.get('passengers')
#
#     filters = Q()
#     if destination:
#         filters &= Q(destination__icontains=destination)
#     if arrival_start and arrival_end:
#         filters &= Q(arriving_date__range=[arrival_start, arrival_end])
#     if passengers:
#         filters &= Q(total_passenger=passengers)
#     filters &= Q(status='open')
#
#     trips = Trip.objects.filter(filters)
#
#     return render(request, 'share_search_results.html', {'trips': trips, "username": username})

# def driver_share_search_results(request):
#     username = request.session.get('username', None)
#     response_message = "Current logged-in user's username: " + request.user.username
#     try:
#         user_profile = UserProfile.objects.get(username=username)
#     except UserProfile.DoesNotExist:
#         response_message += " | User profile does not exist."
#         return HttpResponse(response_message, status=404)
#     # trip_list_share = Trip.objects.filter(is_share=True, status='open').exclude(shared_passenger=user_profile)
#     trip_list_share = Trip.objects.annotate(
#         shared_passenger_count=Count('shared_passenger')
#     ).filter(
#         is_share=True,
#         status='open',
#         shared_passenger_count__lt=F('total_passenger') - 1  # 确保加上当前用户后不会超过最大乘客数
#     ).exclude(
#         shared_passenger=user_profile  # 排除当前用户已经是共享乘客的行程
#     )
#
#     username = request.session.get('username', None)
#     destination = request.GET.get('destination')
#     arrival_start = request.GET.get('arrival_start')
#     arrival_end = request.GET.get('arrival_end')
#     passengers = request.GET.get('passengers')
#
#     filters = Q()
#     if destination:
#         filters &= Q(destination__icontains=destination)
#     if arrival_start and arrival_end:
#         filters &= Q(arriving_date__range=[arrival_start, arrival_end])
#     if passengers:
#         filters &= Q(total_passenger=passengers)
#     filters &= Q(status='open')
#
#     trips = Trip.objects.filter(filters)
#
#     return render(request, 'driver_share_search_results.html', {'trips': trips, "username": username})

def share_search_results(request):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)

    destination = request.GET.get('destination')
    arrival_start = request.GET.get('arrival_start')
    arrival_end = request.GET.get('arrival_end')
    passengers = request.GET.get('passengers')

    # 构建基础查询条件
    base_filters = Q(is_share=True, status='open')

    if destination:
        base_filters &= Q(destination__icontains=destination)
    if arrival_start and arrival_end:
        base_filters &= Q(arriving_date__range=[arrival_start, arrival_end])
    if passengers:
        base_filters &= Q(total_passenger=passengers)

    trips = Trip.objects.annotate(
        shared_passenger_count=Count('shared_passenger')
    ).filter(
        base_filters,
        shared_passenger_count__lt=F('total_passenger') - 1  # 确保加上当前用户后不会超过最大乘客数
    ).exclude(
        shared_passenger=user_profile  # 排除当前用户已经是共享乘客的行程
    )
    return render(request, 'share_search_results.html', {'trips': trips, "username": username})


# @login_required
def driver_share_search_results(request):
    username = request.session.get('username', None)
    response_message = "Current logged-in user's username: " + request.user.username
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        response_message += " | User profile does not exist."
        return HttpResponse(response_message, status=404)

    destination = request.GET.get('destination')
    arrival_start = request.GET.get('arrival_start')
    arrival_end = request.GET.get('arrival_end')
    passengers = request.GET.get('passengers')

    # 构建基础查询条件
    base_filters = Q(is_share=True, status='open')

    if destination:
        base_filters &= Q(destination__icontains=destination)
    if arrival_start and arrival_end:
        base_filters &= Q(arriving_date__range=[arrival_start, arrival_end])
    if passengers:
        base_filters &= Q(total_passenger=passengers)

    trip_list = Trip.objects.annotate(
        shared_passenger_count=Count('shared_passenger')
    ).filter(
        base_filters,
        shared_passenger_count__lt=F('total_passenger') - 1  # 确保加上当前用户后不会超过最大乘客数
    ).exclude(
        shared_passenger=user_profile  # 排除当前用户已经是共享乘客的行程
    )

    return render(request, 'driver_share_search_results.html', {
        'trips': trip_list,
        "username": username
    })

# Create your views here.
def signup(request):
    return render(request, "../templates/signup.html")

def signup_driver(request):
    return render(request, "../templates/signup_driver.html")

def signup_user(request):
    return render(request, "../templates/signup_user.html")