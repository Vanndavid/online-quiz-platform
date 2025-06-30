from quiz.models import Quiz
from django.forms import ModelForm

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['subject', 'difficulty','numberOfQuestion']