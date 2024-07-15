from django.forms import ModelForm
from .models import outfit,User
from django.contrib.auth.forms import UserCreationForm

class MyOutfit(ModelForm):
    class Meta:
        model=outfit
        fields=['image']

