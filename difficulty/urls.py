from django.urls import path
from . import views

urlpatterns = [
    path('',views.getDifficulties, name="difficulties"),
    path('<int:pk>', views.getDifficulty,name="difficulty"),
    path('create-difficulty/', views.createDifficulty, name="create-difficulty"),
    path('update-difficulty/<str:pk>/', views.updateDifficulty, name="update-difficulty"),
    path('delete-difficulty/<str:pk>/', views.deleteDifficulty, name="delete-difficulty"),
    
]
