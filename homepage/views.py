from django.shortcuts import render
from django.db.models import Q

from average import averageScore
from sortTheTop10 import sortTheTop10
# Create your views here.
def getHomePage(request):

    context={}
    if request.user.is_authenticated:
        practices=sortTheTop10(request.user.quiz_set.filter((Q(privateQuiz__isnull=True))))
        quizzes=sortTheTop10(request.user.quiz_set.filter((Q(privateQuiz__isnull=False))))
        total_correct_answers = sum(quiz.count_correct_answers() for quiz in practices)
        total_questions = sum(quiz.count_all_questions() for quiz in practices)
        total_quiz_correct_answers = sum(quiz.count_correct_answers() for quiz in quizzes)
        total_quiz_questions = sum(quiz.count_all_questions() for quiz in quizzes)
        average_practice_score = averageScore(total_correct_answers , total_questions)
        average_quiz_score = averageScore(total_quiz_correct_answers,total_quiz_questions)
        context={'practices':practices,'quizzes':quizzes,'averagePracticeScore':average_practice_score,'averageQuizScore':average_quiz_score}
    return render(request,'homepage/index.html',context)