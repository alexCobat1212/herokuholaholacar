from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=500,blank=True)
    image = models.ImageField(default='default.jpg',upload_to="user_images")
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()





# ---------------- Ride Booking ------------------\
#from django.db import models
#from django.contrib.auth.models import User  # Or your custom user model
from django.core.validators import RegexValidator

class Ride(models.Model):
    user = models.CharField(max_length=200)  # User's name entered manually
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField()
    available_seats = models.PositiveIntegerField(default=4)
    booked_seats = models.PositiveIntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    note = models.CharField(max_length=200)
    contact_number = models.CharField(
        max_length=10, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        help_text="Contact number in the format +999999999. Up to 15 digits allowed."
    )

    def __str__(self):
        # Update the string representation to use the user as a string
        return f"Ride by {self.user} from {self.start_location} to {self.end_location}"

    
class Booking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.ride} on {self.booking_date}"


