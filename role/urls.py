from django.urls import path
from .import views
urlpatterns = [
    path('', views.getRoles,name="roles"),
    path('<int:pk>', views.getRole,name="role"),
    path('create-role/', views.createRole, name="create-role"),
    path('update-role/<str:pk>/', views.updateRole, name="update-role"),
    path('delete-role/<str:pk>/', views.deleteRole, name="delete-role"),
]