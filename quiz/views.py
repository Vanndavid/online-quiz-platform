from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from average import averageScore
from difficulty.models import Difficulty
from question.models import Choice
from quiz.forms import  QuizForm
from quiz.models import  Quiz, QuizQuestion, generate_quiz_questions
from subject.models import Subject
from django.http import HttpResponse,JsonResponse
import json
from users.decorators import signin_required
# Create your views here.

@signin_required #added by ronald
def getQuizs(request):
    quizs=Quiz.objects.all()
    context={'quizs':quizs}
    return render(request,'quiz/index.html',context)
@signin_required 
def getQuiz(request,pk):
    quiz=Quiz.objects.prefetch_related('questions__choices').get(id=pk)
    if quiz.submitted:
        print(quiz.submitted)
        return redirect(reverse('getQuizResult', kwargs={'pk': quiz.id}))
    if request.method == 'POST':
        for question_id, choice_id in request.POST.items():
            if question_id == 'csrfmiddlewaretoken':
                continue

            print(question_id,' --- ', choice_id)
            quizQuestion=QuizQuestion.objects.get(quiz_id=pk,question_id=question_id)
            quizQuestion.choice=Choice.objects.get(id=choice_id)
            quizQuestion.save()
        quiz.submitted=True
        quiz.save()
        return redirect(reverse('getQuizResult', kwargs={'pk': quiz.id}))
    questions = quiz.questions.all()
    context={'quiz': quiz, 'questions':questions}
    return render(request,'quiz/show.html', context)
@signin_required 
def getQuizResult(request,pk):
    quiz=Quiz.objects.prefetch_related('questions__choices').get(id=pk)
    quizQuestions=QuizQuestion.objects.filter(quiz_id=pk)
    print(quizQuestions)
    # json_data = json.dumps(quizQuestions)
    # return JsonResponse(json_data, safe=False)

    questions = quiz.questions.all()
    #count answers
    allQuestions=quiz.questions.count()
    allCorrectQuestions=quizQuestions.filter(choice__correctAnswer=True).count()
    average=averageScore(allCorrectQuestions,allQuestions)
    context={'quiz': quiz, 'questions':questions, 'quizQuestions':quizQuestions,'numOfQ':allQuestions,'numOfC':allCorrectQuestions,'average':average}
    return render(request,'quiz/result.html', context)

@signin_required
def createQuiz(request):
    
    print('here')
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            # Save the quiz
            quiz = quiz_form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            generate_quiz_questions(quiz)
    
            # return redirect('getQuiz')  # Redirect to quiz list page after successful creation
            
            return redirect(reverse('getQuiz', kwargs={'pk': quiz.id}))
        else:
            print("Quiz Form Errors:", quiz_form.errors)
    else:
        quiz_form = QuizForm()
    subjects=Subject.objects.all()
    difficulties=Difficulty.objects.all()
    context={'subjects':subjects,'difficulties':difficulties,'quiz_form': quiz_form}
    return render(request, 'quiz/create.html', context)
@signin_required 
def updateQuiz(request, pk):
       # Get the quiz object or return a 404 error if not found

    quiz = get_object_or_404(Quiz, pk=pk)
    choices = list(quiz.choice_set.values())
    # return JsonResponse(choices, safe=False)
    # return HttpResponse({quiz.choice_set.all()})
    if request.method == 'POST':
        # Extract data from POST request
        quiz_text = request.POST.get('quiz_text')
        subject_id = request.POST.get('subject')
        difficulty_id = request.POST.get('difficulty')

        # Update the quiz object
        quiz.quiz_text = quiz_text
        quiz.subject_id = subject_id
        quiz.difficulty_id = difficulty_id
        quiz.save()

        # Delete existing choices related to the quiz
        quiz.choice_set.all().delete()

        # Extract choice data from POST request and save new choices
        for i in range(1, 5):  # Assuming you have 4 choices
            choice_text = request.POST.get(f'choice{i}')
            correct_answer = request.POST.get('correct_answer') == str(i)  # Check if choice is correct
            choice = Choice.objects.create(
                quiz=quiz,
                choice_text=choice_text,
                correctAnswer=correct_answer
            )

        return redirect('quizs')  # Redirect to quiz list page after successful update

    else:
        # Fetch all subjects and difficulties for rendering the form
        subjects = Subject.objects.all()
        difficulties = Difficulty.objects.all()
        context = {'subjects': subjects, 'difficulties': difficulties, 'quiz': quiz,'choices':choices}
        return render(request, 'quiz/update.html', context)
@signin_required 
def deleteQuiz(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quizs')
    return render(request, 'quiz/delete.html', {'obj':quiz})