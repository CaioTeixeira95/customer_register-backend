from .views import CustomerViewSet, UserRegisterCreateAPIView
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'^customer', CustomerViewSet, basename='customer')

urlpatterns = [
    path('register/', UserRegisterCreateAPIView.as_view(), name='user-register'),
] + router.urls
