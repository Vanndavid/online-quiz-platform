from privateQuiz.models import PrivateQuiz

from django.forms import ModelForm

class PrivateQuizForm(ModelForm):
    class Meta:
        model = PrivateQuiz
        fields = ['name','subject', 'difficulty','numberOfQuestion']
        
class JoinForm(ModelForm):
    class Meta:
        model = PrivateQuiz
        fields = ['code']