from django.shortcuts import redirect
from django.http import HttpResponse

def signin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to login page if not a teacher
    return wrapper

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and ((request.user.role.name).lower() == 'teacher' or (request.user.role.name).lower() == 'admin'):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorised to access this page. You will need to login as a teacher or and admin. Please use browser back button to return to previous page.")  # Redirect to login page if not a teacher
    return wrapper
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and ((request.user.role.name).lower() == 'admin' ):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorised to access this page. You will need to login as a admin. Please use browser back button to return to previous page.")  # Redirect to login page if not a teacher
    return wrapper