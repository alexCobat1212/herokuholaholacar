from api.models import User,Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


# ----------------------- Creating User ------------------------

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','verified']


class MyenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)


        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio

        return token



# ----------------- User Registration ----------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,required=True,validators=[validate_password]
    )

    password2 = serializers.CharField(
        write_only=True,required=True
    )

    class Meta:
        model = User
        fields = ['username','email','password','password2']

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2':'Passwords must match'})
        return attrs

    def create(self,validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# --------------------- Ride Booking   --------------------------

from .models import Ride,Booking

from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            'id', 'user', 'start_location', 'end_location', 'price',
            'start_time', 'end_time', 'date', 'available_seats',
            'booked_seats', 'is_complete', 'note', 'contact_number'
        ]

    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be later than start time.")
        if data['available_seats'] < data['booked_seats']:
            raise serializers.ValidationError("Available seats cannot be fewer than booked seats.")
        return data


class BookingSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Booking
        fields = ['id','ride','user','booking_date']


def perform_create(self, serializer):
    serializer.save(user=self.request.user)
