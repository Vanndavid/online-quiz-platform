from django.shortcuts import render,redirect

from difficulty.models import Difficulty


from django.http import HttpResponse 


from .forms import DifficultyForm

from users.decorators import teacher_required #added by ronald

# Create your views here.
@teacher_required #added by ronald
def getDifficulties(request):
    Difficultiess=Difficulty.objects.all()
    context={'difficulties':Difficultiess}
    return render(request,'difficulty/index.html',context)

@teacher_required 
def getDifficulty(request,pk):
    diff=Difficulty.objects.get(id=pk)
    context={'difficulty': diff}
    return render(request,'difficulty/show.html', context)
    
@teacher_required 
def createDifficulty(request):
    form = DifficultyForm()
    if request.method == 'POST':
        form = DifficultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('difficulties')
    context = {'form': form}
    return render(request, 'difficulty/Difficulty_form.html', context)
    
@teacher_required 
def updateDifficulty(request, pk):
    difficulty = Difficulty.objects.get(id=pk)
    form = DifficultyForm(instance=difficulty)
    if request.method == 'POST':
        form = DifficultyForm(request.POST, instance=difficulty)
        if form.is_valid():
            form.save()
            return redirect('difficulties')
    context = {'form': form}
    return render(request, 'difficulty/Difficulty_form.html', context)

@teacher_required 
def deleteDifficulty(request, pk):
    difficulty = Difficulty.objects.get(id=pk)
    if request.method == 'POST':
        difficulty.delete()
        return redirect('difficulties')
    return render(request, 'difficulty/delete.html', {'obj':difficulty})
    