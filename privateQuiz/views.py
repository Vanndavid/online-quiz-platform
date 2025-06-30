from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q

from django.urls import reverse
from privateQuiz.models import PrivateQuiz
from difficulty.models import Difficulty
from privateQuiz.forms import JoinForm, PrivateQuizForm
from quiz.forms import QuizForm
from quiz.models import Quiz, generate_quiz_questions
from subject.models import Subject
from django.http import HttpResponse,JsonResponse
from privateQuiz.forms import PrivateQuizForm
from users.decorators import signin_required,teacher_required

# Create your views here.
def getPrivateQuizzes(request):
    privateQuizzes=PrivateQuiz.objects.filter(teacher=request.user).all()
    subjects = Subject.objects.all()
    difficulties = Difficulty.objects.all()
    print(privateQuizzes)
    context={'privateQuizzes':privateQuizzes, 'subjects':subjects, 'difficulties':difficulties}
    return render(request,'privateQuiz/index.html',context)
def getPrivateQuiz(request,pk):
    privateQuiz=PrivateQuiz.objects.get(id=pk)
    context={'privateQuiz': privateQuiz,'participants':privateQuiz.get_user_scores(),'numberOfParticipant':privateQuiz.quiz_set.count()}
    return render(request,'privateQuiz/show.html', context)

@signin_required
def createPrivateQuiz(request):
    
    print('here')
    if request.method == 'POST':
        quiz_form = PrivateQuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.teacher = request.user
            quiz.save()
            return redirect(reverse('privateQuiz', kwargs={'pk': quiz.id}))
        else:
            print("Quiz Form Errors:", quiz_form.errors)
    else:
        quiz_form = PrivateQuizForm()
    subjects=Subject.objects.all()
    difficulties=Difficulty.objects.all()
    context={'subjects':subjects,'difficulties':difficulties,'quiz_form': quiz_form}
    return render(request, 'privateQuiz/create.html', context)

@signin_required
def joinPrivateQuiz(request):
    if request.method == 'POST':

        code = request.POST.get('code')  
        privateQuiz=PrivateQuiz.objects.get(code=code)
        quizIsExisted=Quiz.objects.filter(privateQuiz=privateQuiz,user=request.user).first()
        if quizIsExisted:
            return redirect(reverse('getQuizResult', kwargs={'pk': quizIsExisted.id}))
        quiz_form = QuizForm()
        quiz = quiz_form.save(commit=False)
        quiz.subject=privateQuiz.subject
        quiz.difficulty=privateQuiz.difficulty
        quiz.numberOfQuestion=privateQuiz.numberOfQuestion
        quiz.user = request.user
        quiz.privateQuiz=privateQuiz
        quiz.save()
        generate_quiz_questions(quiz)
        return redirect(reverse('getQuiz', kwargs={'pk': quiz.id}))
    return render(request, 'privateQuiz/join.html')
@teacher_required
def updatePrivateQuiz(request, pk):
       # Get the privateQuiz object or return a 404 error if not found

    privateQuiz = get_object_or_404(PrivateQuiz, pk=pk)
    choices = list(privateQuiz.choices.all().values())
    # return JsonResponse(choices, safe=False)
    # return HttpResponse({privateQuiz.choice_set.all()})
    if request.method == 'POST':
       
        return redirect('privateQuizs')  # Redirect to privateQuiz list page after successful update

    else:
        # Fetch all subjects and difficulties for rendering the form
        subjects = Subject.objects.all()
        difficulties = Difficulty.objects.all()
        context = {'subjects': subjects, 'difficulties': difficulties, 'privateQuiz': privateQuiz,'choices':choices}
        return render(request, 'privateQuiz/update.html', context)

@teacher_required
def deletePrivateQuiz(request, pk):
    privateQuiz = PrivateQuiz.objects.get(id=pk)
    if request.method == 'POST':
        privateQuiz.delete()
        return redirect('privateQuizzes')
    return render(request, 'privateQuiz/delete.html', {'obj':privateQuiz})