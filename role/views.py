from django.shortcuts import render,redirect
from users.decorators import teacher_required #added by ronald

from role.forms import RoleForm
from role.models import Role

# Create your views here.

@teacher_required #added by ronald
def getRoles(request):
    roles=Role.objects.all()
    context={'roles':roles}
    return render(request,'role/index.html',context)
@teacher_required 
def getRole(request,pk):
    role=Role.objects.get(id=pk)
    context={'role': role}
    return render(request,'role/show.html', context)

@teacher_required 
def createRole(request):
    form = RoleForm()
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles')
    context = {'form': form}
    return render(request, 'role/role_form.html', context)

@teacher_required 
def updateRole(request, pk):
    role = Role.objects.get(id=pk)
    form = RoleForm(instance=role)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('roles')
    context = {'form': form}
    return render(request, 'role/role_form.html', context)

@teacher_required 
def deleteRole(request, pk):
    role = Role.objects.get(id=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('roles')
    return render(request, 'role/delete.html', {'obj':role})