from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views

urlpatterns = [
    path('', views.UserListAPIView.as_view(), name='list'),
    path('<int:user_id>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-delete'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
