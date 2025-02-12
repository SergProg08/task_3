from django.urls import path
from .views import UserCreateAPIView, UserLogoutAPIView, MeAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'apiapp'

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('me/', MeAPIView.as_view(),name='me'),
]
