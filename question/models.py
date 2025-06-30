from datetime import datetime, timezone
from django.db import models
from difficulty.models import Difficulty
from subject.models import Subject

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correctAnswer = models.BooleanField(default=0)

    def __str__(self):
        return self.choice_text
