from django.db import models
from privateQuiz.models import PrivateQuiz
from difficulty.models import Difficulty
from question.models import Choice, Question
from subject.models import Subject
from users.models import User
import random
# Create your models here.
class Quiz(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    numberOfQuestion=models.IntegerField(null=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')  # Define many-to-many relationship
    privateQuiz = models.ForeignKey(PrivateQuiz, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-created date field
    submitted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    def count_correct_answers(self):
        return self.quizquestion_set.filter(choice__correctAnswer=True).count()
    def count_all_questions(self):
        return self.quizquestion_set.count()
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str(self.id)
    
def generate_quiz_questions(quiz):
    subject = quiz.subject
    difficulty = quiz.difficulty

    # Build a filter based on subject and difficulty
    filter_args = {}
    if subject:
        filter_args['subject'] = subject
    if difficulty:
        filter_args['difficulty'] = difficulty

    # Retrieve questions based on the filter
    all_questions = Question.objects.filter(**filter_args)

    # Shuffle the questions
    shuffled_questions = list(all_questions)
    random.shuffle(shuffled_questions)

    # Select the first `numberOfQuestion` questions
    selected_questions = shuffled_questions[:quiz.numberOfQuestion]

    # Create QuizQuestion instances for the selected questions
    for question in selected_questions:
        QuizQuestion.objects.create(quiz=quiz, question=question)