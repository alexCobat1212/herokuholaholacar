from django.shortcuts import render
from .models import Profile,User
from.serializer import UserSerializers,MyenObtainPairSerializer,RegisterSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        context = f"Hey {request.user} , You are seeing a get response"
        return Response({'response':context},status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get("text")
        response = f"Hey {request.user} your text is {text}"
        return Response({'response':response},status=status.HTTP_200_OK)
    
    return Response({},status=status.HTTP_400_BAD_REQUEST)
        


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"username": user.username, "email": user.email})




# ---------------- Ride ------------------

from rest_framework import viewsets,permissions
from .models import Ride,Booking
from rest_framework.decorators import action
from.serializer import RideSerializer,BookingSerializer
from django.http import JsonResponse

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


# views.py
from django.http import JsonResponse
from .models import Ride

def search_rides(request):
    start_location = request.GET.get('start_location')
    end_location = request.GET.get('end_location')
    date = request.GET.get('date')

    # Filter rides based on search criteria
    rides = Ride.objects.filter(
        start_location=start_location,
        end_location=end_location,
        date=date
    )

    # Return the results in a JSON response
    return JsonResponse({'rides': list(rides.values())})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Ride
from .serializer import RideSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ride
from .serializer import RideSerializer

class PublishRideView(APIView):
    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ride published successfully.", "ride": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .models import Booking
from .serializer import BookingSerializer

class BookRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile = {
            "username": user.username,
            "verified": user.profile.verified,
        }
        return JsonResponse(profile)

