from django.urls import path
from . import views

urlpatterns = [
    path('',views.getPrivateQuizzes, name="privateQuizzes"),
    path('create/',views.createPrivateQuiz, name="createPrivateQuiz"),
    path('<int:pk>', views.getPrivateQuiz,name="privateQuiz"),
    path('join', views.joinPrivateQuiz,name="joinPrivateQuiz"),
    path('update-private-quiz/<str:pk>/', views.updatePrivateQuiz, name="update-private-quiz"),
    path('delete-private-quiz/<str:pk>/', views.deletePrivateQuiz, name="delete-private-quiz"),
]