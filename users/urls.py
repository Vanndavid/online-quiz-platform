
from django.urls import path 
from . import views 


urlpatterns = [
    path('login/', views.loginView, name="login"), #added by ronald
    path('logout/', views.logoutUser, name="logout"), #added by ronald
    path('register/', views.registerPage, name="register"), #added by ronald
    path('', views.getUsers,name="users"),
    path('<int:pk>', views.getUser,name="user"),
    
    path('create-user/', views.createUser, name="create-user"),
    path('reset-user/<str:pk>/', views.resetPasswordUser, name="reset-user"),
    path('update-user/<str:pk>/', views.updateUser, name="update-user"),
    path('delete-user/<str:pk>/', views.deleteUser, name="delete-user"),
]
