from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from apps.users.models import CustomUser


class UserRegistrationForm(forms.Form):
    """
    A form for user registration with fields for first name, email, and password.

    Fields:
        - first_name: The first name of the user (used as the username).
        - email: The email address of the user.
        - password: The user's password, validated against Django's password policies.
    """
    first_name = forms.CharField(
        max_length=150,
        min_length=3,
        required=True,
        help_text="Enter your first name (3-150 characters)."
    )
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address."
    )
    password = forms.CharField(
        min_length=8,
        required=True,
        validators=[validate_password],
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters long and follow security policies."
    )

    def clean_username(self):
        """
        Validates that the first name (used as a username) is unique.

        Raises:
            ValidationError: If a user with the same username already exists.

        Returns:
            str: The validated username.
        """
        username = self.cleaned_data['first_name']
        kwargs = {
            CustomUser.USERNAME_FIELD: username,
        }
        if get_user_model().objects.filter(**kwargs).exists():
            raise forms.ValidationError('Username already exists.')
        return username



