from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, RegisterForm, ResetPasswordForm, UserForm
from django.urls import reverse
from role.models import Role
from users.decorators import admin_required
from django.db.models import Q
from django.contrib.auth.hashers import make_password

@admin_required 
def getUsers(request):
    userQuery = request.GET.get('q')

    users = None
    if userQuery != None:
        users=User.objects.filter( Q(name__icontains=userQuery) )
    else:
        users=User.objects.all()
    context={'users':users}
    return render(request,'users/index.html',context)

@admin_required 
def getUser(request,pk):
    user=User.objects.get(id=pk)
    return render(request,'users/show.html', context={'user':user})

@admin_required 
def createUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #then it allows for additional processing before saving

            user.username = request.POST.get('email')  
            user.save()
            return redirect('users')
    context = {'form': form}
    return render(request, 'users/user_form.html', context)

@admin_required 
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    context = {'form': form}
    return render(request, 'users/user_form.html', context)
@admin_required 
def resetPasswordUser(request, pk):
    user = User.objects.get(id=pk)
    form = ResetPasswordForm(instance=user)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    context = {'form': form}
    return render(request, 'users/user_form.html', context)

@admin_required 
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users')
    return render(request, 'users/delete.html', {'obj':user})

#added by ronald 
#source: https://www.youtube.com/watch?v=PtQiiknWUcI&t=10147s&ab_channel=TraversyMedia 
def loginView(request):
    
    page = 'login'

    if request.user.is_authenticated:
        return redirect(reverse('users'))

    # if form submitted
    if request.method == 'POST':

        # requests information from POST
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # then it checks if email (user) exists
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        # then it checks if email and password matches
        user = authenticate(request, email=email, password=password)

        # if the user does exist
        if user is not None:
            login(request, user) #creates session
            return redirect(reverse('homepage'))
        else:
            messages.error(request, 'Username or password is incorrect.')

    # this loads the login page 
    context = {'page': page}
    return render(request, 'users/login_register.html', context) 

def logoutUser(request):
    logout(request) #deletes token
    return redirect(reverse('homepage'))


def registerPage(request):
    #this creates an object with an empty array 
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        endwithString='instatute.edu.au'
        email = request.POST['email']
        if not email.endswith(endwithString) :
            # Password is too short, display error message\
            print('asdf')
            messages.error(request, 'You must use your school email')
            return render(request, 'users/login_register.html', {'form': form})
        
        if len(password1) < 8:
            # Password is too short, display error message
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'users/login_register.html', {'form': form})
        
        # this checks if form is valid
        if password1 == password2:
            if form.is_valid():
                role_instance = Role.objects.get(name='student')
                user = form.save(commit=False) #then it allows for additional processing before saving

                user.username = user.email.lower() #cleans data (makes sure username lowercase)

                user.role = role_instance

                user.save() #registers user

                login(request,user) #logs in user immediately after registration
                return redirect(reverse('homepage')) # and redirect to users page
            else:
                messages.error(request, 'An error occured during registration')
        else:
            messages.error(request, "Passwords don't match.")

    return render(request, 'users/login_register.html', {'form': form})

