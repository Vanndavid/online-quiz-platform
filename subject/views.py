from django.shortcuts import render, redirect
from django.http import HttpResponse 
# below line added from users.views.py
from subject.models import Subject
from .forms import SubjectForm
from users.decorators import teacher_required #added by ronald


# Create your views here.
@teacher_required #added by ronald
def getSubjects(request):
    subjects=Subject.objects.all()
    context={'subjects':subjects}
    return render(request,'subject/index.html',context)
@teacher_required 
def getSubject(request,pk):
    subject=Subject.objects.get(id=pk)
    context={'subject': subject}
    return render(request,'subject/show.html', context)

@teacher_required 
def createSubject(request):
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects')
    context = {'form': form}
    return render(request, 'subject/subject_form.html', context)

@teacher_required 
def updateSubject(request, pk):
    subject = Subject.objects.get(id=pk)
    form = SubjectForm(instance=subject)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subjects')
    context = {'form': form}
    return render(request, 'subject/subject_form.html', context)

@teacher_required 
def deleteSubject(request, pk):
    subject = Subject.objects.get(id=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subjects')
    return render(request, 'subject/delete.html', {'obj':subject})