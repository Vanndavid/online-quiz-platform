from django.forms import ModelForm
from .models import Choice, Question

from django.forms import formset_factory

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'correctAnswer']
ChoiceFormSet = formset_factory(ChoiceForm, extra=4)  # Assuming you want to display 3 extra choice forms by default