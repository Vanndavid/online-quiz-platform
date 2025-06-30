from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q

from difficulty.models import Difficulty
from question.forms import ChoiceFormSet, QuestionForm,ChoiceForm
from question.models import Choice, Question
from subject.models import Subject
from django.http import HttpResponse,JsonResponse
import json
from users.decorators import teacher_required 

# Create your views here.

@teacher_required 
def getQuestions(request):
    subjectQuery = request.GET.get('subject')
    difficultyQuery = request.GET.get('difficulty') 
    questionQuery = request.GET.get('q')

    questions = None
    if subjectQuery != None:
        questions=Question.objects.filter(subject__name=subjectQuery)
    elif difficultyQuery != None:
        questions=Question.objects.filter(difficulty__name=difficultyQuery)
    elif questionQuery != None:
        questions=Question.objects.filter( Q(question_text__icontains=questionQuery) | 
                                           Q(subject__name__icontains=questionQuery) | 
                                           Q(difficulty__name__icontains=questionQuery) )
    else:
        questions=Question.objects.all()
    subjects = Subject.objects.all()
    difficulties = Difficulty.objects.all()
    context={'questions':questions, 'subjects':subjects, 'difficulties':difficulties}
    return render(request,'question/index.html',context)

@teacher_required
def getQuestion(request,pk):
    question=Question.objects.get(id=pk)
    context={'question': question}
    return render(request,'question/show.html', context)

@teacher_required
def createQuestion(request):
    
    print('here')
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if question_form.is_valid():
            # Save the question
            question = question_form.save()
         
            for i in range(1, 5):  # Assuming you have 4 choices
                choice_text = request.POST.get(f'choice{i}')
                correct_answer = request.POST.get('correct_answer') == str(i)  # Check if choice is correct
                choice = Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    correctAnswer=correct_answer
                )

    
            return redirect('questions')  # Redirect to question list page after successful creation
        else:
            print("Question Form Errors:", question_form.errors)
            print("Choice Formset Errors:", choice_formset.errors)
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()
    subjects=Subject.objects.all()
    difficulties=Difficulty.objects.all()
    context={'subjects':subjects,'difficulties':difficulties,'question_form': question_form, 'choice_formset': choice_formset}
    return render(request, 'question/create.html', context)

@teacher_required
def updateQuestion(request, pk):
       # Get the question object or return a 404 error if not found

    question = get_object_or_404(Question, pk=pk)
    choices = list(question.choices.all().values())
    # return JsonResponse(choices, safe=False)
    # return HttpResponse({question.choice_set.all()})
    if request.method == 'POST':
        # Extract data from POST request
        question_text = request.POST.get('question_text')
        subject_id = request.POST.get('subject')
        difficulty_id = request.POST.get('difficulty')

        # Update the question object
        question.question_text = question_text
        question.subject_id = subject_id
        question.difficulty_id = difficulty_id
        question.save()

        # # Delete existing choices related to the question
        # question.choices.all().delete()

        # # Extract choice data from POST request and save new choices
        # for i in range(1, 5):  # Assuming you have 4 choices
        #     choice_text = request.POST.get(f'choice{i}')
        #     correct_answer = request.POST.get('correct_answer') == str(i)  # Check if choice is correct
        #     choice = Choice.objects.create(
        #         question=question,
        #         choice_text=choice_text,
        #         correctAnswer=correct_answer
        #     )
        # Get existing choices related to the question
        existing_choices = question.choices.all()

        # Update existing choices with new data from POST request
        for choice in existing_choices:
            choice_text = request.POST.get(f'choice{choice.id}')
            correct_answer_id = int(request.POST.get('correct_answer'))
            correct_answer = (correct_answer_id == choice.id)
            choice.choice_text = choice_text
            choice.correctAnswer = correct_answer
            choice.save()
        return redirect('questions')  # Redirect to question list page after successful update

    else:
        # Fetch all subjects and difficulties for rendering the form
        subjects = Subject.objects.all()
        difficulties = Difficulty.objects.all()
        context = {'subjects': subjects, 'difficulties': difficulties, 'question': question,'choices':choices}
        return render(request, 'question/update.html', context)

@teacher_required
def deleteQuestion(request, pk):
    question = Question.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('questions')
    return render(request, 'question/delete.html', {'obj':question})