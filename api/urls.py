from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path,include
from api import views
from .views import UserDetailView
from rest_framework.routers import DefaultRouter
from .views import RideViewSet,BookingViewSet
from .views import PublishRideView,BookRideView,UserProfileView

router = DefaultRouter()
router.register(r'rides',RideViewSet)
router.register(r'booking',BookingViewSet)




urlpatterns = [
    path("token/",views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path("token/refresh/",TokenRefreshView.as_view(),name='token_refresh'),
    path("register/",views.RegisterView.as_view(),name='auth_register'),
    path('test/',views.testEndPoint,name='test'),

    # --------------- Ride ------------------

    path('',include(router.urls)),
    path('search-rides/', views.search_rides, name='search_rides'),
    path('ride/', PublishRideView.as_view(), name='publish_ride'),
    path('rides/book/', BookRideView.as_view(), name='book-ride'),
    path("verify/", UserProfileView.as_view(), name="user-profile"),
    
]
