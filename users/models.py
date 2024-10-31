from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
        Custom User model that extends Django's AbstractUser to include additional fields
        specific to the application's requirements.

        Attributes:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            phone (str): The user's phone number, must start with '09' and be 11 digits long.
            email (str): The user's email address, unique for each user.
            created_at (datetime): The timestamp when the user account was created.
            is_active (bool): Indicates whether the user account is active; defaults to True.
    """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must start with 09 and be exactly 11 digits.'
            ),
        ],
        blank=True,
        null=True,
    )
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
