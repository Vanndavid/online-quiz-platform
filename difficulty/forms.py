from django.forms import ModelForm
from .models import Difficulty


class DifficultyForm(ModelForm):
    class Meta:
        model = Difficulty
        fields = '__all__'