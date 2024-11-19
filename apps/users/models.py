from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from apps.users.services import user_image_location


class CustomUserManager(UserManager):
    """
    Custom manager for the CustomUser model, handling user creation and password hashing.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, password, and additional fields.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to be saved with the user.

        Returns:
            CustomUser: The created user instance.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Create a regular user.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to be saved with the user.

        Returns:
            CustomUser: The created user instance.
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Create a superuser with additional staff and superuser privileges.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields to be saved with the superuser.

        Returns:
            CustomUser: The created superuser instance.
        """
        extra_fields['is_staff'] = extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that replaces the default username field with email
    and includes additional fields such as phone number, address, and user image.
    """

    username = None  # Disable the username field

    email = models.EmailField(unique=True)
    user_wishlist_count = models.IntegerField(default=0)
    user_cart_count = models.IntegerField(default=0)
    user_image = models.ImageField(
        upload_to=user_image_location,
        blank=True,
        null=True
    )

    # Extra fields for user details
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """
        String representation of the CustomUser.

        Returns:
            str: The email address of the user.
        """
        return self.email
