from .models import Tables, Contributors
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Tables
        fields = ["equip", "quantity", "approved_by_manager","delivered"]


class ContributorForm(ModelForm):
    class Meta:
        model = Contributors
        fields = ["title", "bio","contributor_id"]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



