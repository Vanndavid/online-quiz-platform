from django.contrib import admin

from quiz.models import Quiz, QuizQuestion

# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizQuestion)