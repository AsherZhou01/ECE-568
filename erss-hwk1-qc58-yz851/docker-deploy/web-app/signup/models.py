from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField

class UserProfile(models.Model):
    VEHICLE_CHOICES = (
        ('economy', 'Economy'),
        ('comfort', 'Comfort'),
        ('luxury', 'Luxury'),
        ('suv', 'SUV'),
    )

    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    is_driver = models.BooleanField(default=False)
    # vehicle_type = MultiSelectField(choices=VEHICLE_CHOICES, max_choices=4, max_length=50, default='', blank=True)
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES,
        default='economy',
        blank=True
    )
    license_number = models.CharField(max_length=20, default='', blank=True)
    max_passenger_number = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8)  # max num of valid passenger
        ], default=0
    )

    def __str__(self):
        return f"{self.username}'s driver profile"



class Trip(models.Model):
    # 定义与UserProfile的一对多关系
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='trips')
    driver_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='trips_as_driver', null=True, blank=True)
    current_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    arriving_date = models.DateField()
    arriving_time = models.TimeField()
    total_passenger = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ]
    )
    is_share = models.BooleanField(default=False)
    VEHICLE_CHOICES = (
        ('any', 'Any'),
        ('economy', 'Economy'),
        ('comfort', 'Comfort'),
        ('luxury', 'Luxury'),
        ('suv', 'SUV'),
    )
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES,
        default='economy',
        blank=True
    )
    # need to be modified -------------------------------
    is_confirmed = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    )
    shared_passenger = models.ManyToManyField(
        UserProfile,
        related_name='shared_trips',
        blank=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Trip for {self.user_profile.username} from {self.current_location} to {self.destination} on {self.arriving_date}"