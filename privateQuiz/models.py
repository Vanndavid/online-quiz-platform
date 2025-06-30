import uuid
from django.db import models

from difficulty.models import Difficulty
from ranking import ranking
from subject.models import Subject
from users.models import User
from django.utils.crypto import get_random_string

# Create your models here.
class PrivateQuiz(models.Model):
    
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    teacher= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    numberOfQuestion=models.IntegerField(null=True)
    code = models.CharField(max_length=5, unique=True)  # Generate UUID as default value
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-created date field
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        if not self.code:  # If code is not provided
            self.code = get_random_string(5)  # Generate a random string of length 5
        super().save(*args, **kwargs)  # Call the parent class save method to save the instance
    def get_user_scores(self):
        
        from quiz.models import QuizQuestion
        user_scores = []
        for quiz in self.quiz_set.all():
            quizQuestions=QuizQuestion.objects.filter(quiz_id=quiz.id)
            total_questions = quizQuestions.count()
            user_scores.append({
                'user': quiz.user,
                'correct_answers': quiz.count_correct_answers(),
                'total_questions': total_questions,
                'created_at': quiz.created_at
            })
        return ranking(user_scores)