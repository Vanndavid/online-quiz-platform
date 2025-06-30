
from django.urls import path
from .import views
urlpatterns = [
    path('', views.getQuestions,name="questions"),
    path('create', views.createQuestion,name="create_question"),
    path('<int:pk>', views.getQuestion,name="getQuestion"),
    path('update-question/<str:pk>/', views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>/', views.deleteQuestion, name="delete-question"),
]