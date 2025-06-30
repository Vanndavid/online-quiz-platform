# source: https://www.youtube.com/watch?v=PtQiiknWUcI&t=10147s&ab_channel=TraversyMedia
from django.db import models
from django.contrib.auth.models import AbstractUser

from role.models import Role
# Login model
class User(AbstractUser):
    pass 
    name=models.CharField(max_length=200, null=True) 
    email=models.EmailField(unique=True, max_length=250, null=True) 
    
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    
    USERNAME_FIELD = 'email' #sets username field to email field. use instead of username.
    REQUIRED_FIELDS = [] #set required fields
    