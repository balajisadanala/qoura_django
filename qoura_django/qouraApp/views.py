import json
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm,QuestionForm,AnswerForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.cache import never_cache

@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@never_cache
@login_required
def home(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print("Formvlid",form.is_valid())
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()

    questions = Questions.objects.all().order_by('-posted_date')
    return render(request, 'home.html', {
        'form': form,
        'questions': questions
    })
@never_cache
@login_required
def vote_question(request, question_id, vote_type):
    question = get_object_or_404(Questions, id=question_id)
    user = request.user
    response_data = {'status': 'success'}

    if vote_type == 'up':
        if question.upvotes.filter(id=user.id).exists():
            question.upvotes.remove(user)
            response_data['action'] = 'removed'
        else:
            question.upvotes.add(user)
            response_data['action'] = 'added'
        if question.downvotes.filter(id=user.id).exists():
            question.downvotes.remove(user)
    elif vote_type == 'down':
        print("down")
        if question.downvotes.filter(id=user.id).exists():
            question.downvotes.remove(user)
            print("dremove")
            response_data['action'] = 'removed'
        else:
            question.downvotes.add(user)
            print("d added")
            response_data['action'] = 'added'
        if question.upvotes.filter(id=user.id).exists():
            print("at d up removed")
            question.upvotes.remove(user)

    response_data.update({
        'upvotes': question.upvotes.count(),
        'downvotes': question.downvotes.count(),
        'net_votes': question.upvotes.count(),
        'user_vote_status': 'upvoted' if question.upvotes.filter(id=user.id).exists() else
                           'downvoted' if question.downvotes.filter(id=user.id).exists() else
                           'none'
    })
    return JsonResponse(response_data)

@never_cache
@login_required
def vote_answer(request, answer_id, vote_type):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user
    response_data = {'status': 'success'}

    if vote_type == 'up':
        if answer.upvotes.filter(id=user.id).exists():
            answer.upvotes.remove(user)
            response_data['action'] = 'removed'
        else:
            answer.upvotes.add(user)
            response_data['action'] = 'added'
        if answer.downvotes.filter(id=user.id).exists():
            answer.downvotes.remove(user)
    elif vote_type == 'down':
        if answer.downvotes.filter(id=user.id).exists():
            answer.downvotes.remove(user)
            response_data['action'] = 'removed'
        else:
            answer.downvotes.add(user)
            response_data['action'] = 'added'
        if answer.upvotes.filter(id=user.id).exists():
            answer.upvotes.remove(user)

    response_data.update({
        'upvotes': answer.upvotes.count(),
        'downvotes': answer.downvotes.count(),
        'net_votes': answer.upvotes.count(),
        'user_vote_status': 'upvoted' if answer.upvotes.filter(id=user.id).exists() else
                           'downvoted' if answer.downvotes.filter(id=user.id).exists() else
                           'none'
    })
    return JsonResponse(response_data)

def question_detail(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    answers = question.answers.all().order_by('-updated_at')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()

    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })



@login_required
def post_answer(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Answer.objects.create(
                user=request.user,
                question=question,
                content=content
            )
    return redirect('home')

@login_required
def edit_question(request, pk):
    question = get_object_or_404(Questions, pk=pk)
    if question.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question.question = data.get('question')
            question.description = data.get('description')
            question.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def delete_question(request, pk):
    question = get_object_or_404(Questions, pk=pk)
    if question.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    if request.method == 'POST':
        question.delete()
        return JsonResponse({'status': 'success'})

@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answer.content = data.get('content')
            answer.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    if request.method == 'POST':
        answer.delete()
        return JsonResponse({'status': 'success'})
