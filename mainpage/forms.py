from .models import Tables
from django.forms import ModelForm


class TaskForm(ModelForm):
    class Meta:
        model = Tables
        fields = ["title", "quantity"]

