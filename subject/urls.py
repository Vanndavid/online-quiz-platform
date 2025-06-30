
from django.urls import path
from .import views
urlpatterns = [
    path('', views.getSubjects,name="subjects"),
    path('<int:pk>', views.getSubject,name="subject"),
    path('create-subject/', views.createSubject, name="create-subject"),
    path('update-subject/<str:pk>/', views.updateSubject, name="update-subject"),
    path('delete-subject/<str:pk>/', views.deleteSubject, name="delete-subject"),
]