from rest_framework import (
    generics,
    permissions,
)

from .models import User
from .permissions import IsOwnerOrAdminUser
from .serializers import UserSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows new users to create an account. It uses the UserSerializer
    to validate the input data and create a new user instance in the database.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a user.

    This view allows authenticated users to retrieve their own information,
    update their profile, or delete their account. It ensures that only the owner of the user
    instance or the admin user can perform these actions through the IsOwner permission class.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdminUser,
    ]


class UserAdminListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing all users or creating a new staff-user.

    This view allows admin users to list all user accounts in the system
    and to create a new user with is_staff=True. The IsAdminUser permission ensures that only
    users with admin privileges can access this view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]

    def perform_create(self, serializer):
        serializer.is_staff = True
        serializer.save()
