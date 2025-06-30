
from django.urls import path
from .import views
urlpatterns = [
    path('', views.getQuizs,name="quizzes"),
    path('create', views.createQuiz,name="create_quiz"),
    path('<int:pk>', views.getQuiz,name="getQuiz"),
    path('<str:pk>/result/', views.getQuizResult, name='getQuizResult'),
    path('update-quiz/<str:pk>/', views.updateQuiz, name="update-quiz"),
    path('delete-quiz/<str:pk>/', views.deleteQuiz, name="delete-quiz"),
]