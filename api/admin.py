
from django.contrib import admin
from .models import User,Profile,Ride,Booking

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']

class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user','full_name','verified']



