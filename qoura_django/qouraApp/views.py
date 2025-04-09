from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm,QuestionForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.cache import never_cache

@never_cache
def signup(request):
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

    if vote_type == 'up':
        if question.downvotes.filter(id=user.id).exists():
            question.downvotes.remove(user)
        question.upvotes.add(user)
    elif vote_type == 'down':
        if question.upvotes.filter(id=user.id).exists():
            question.upvotes.remove(user)
        question.downvotes.add(user)
    elif vote_type == 'remove':
        question.upvotes.remove(user)
        question.downvotes.remove(user)

    return redirect('home')
@never_cache
@login_required
def vote_answer(request, answer_id, vote_type):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user

    if vote_type == 'up':
        if answer.downvotes.filter(id=user.id).exists():
            answer.downvotes.remove(user)
        answer.upvotes.add(user)
    elif vote_type == 'down':
        if answer.upvotes.filter(id=user.id).exists():
            answer.upvotes.remove(user)
        answer.downvotes.add(user)
    elif vote_type == 'remove':
        answer.upvotes.remove(user)
        answer.downvotes.remove(user)

    return redirect('question_detail', pk=answer.question.id)