from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class RegistrationForm(UserCreationForm):
    """ subclass of Django's UserCreationForm, to handle customer registration
    with a required minimum length and password strength. Also contains an
    additional field for capturing the email on registration.

    """
    email = forms.EmailField(max_length="50")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
