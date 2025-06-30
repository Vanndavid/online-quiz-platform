from django.shortcuts import render

from role.models import Role

# Create your views here.
def getroles(request):
    roles=Role.objects.all()
    context={'roles':roles}
    return render(request,'role/index.html')
def getRole(request,pk):
    role=Role.objects.get(id=pk)
    context={'role': role}
    return render(request,'role/show.html', context)