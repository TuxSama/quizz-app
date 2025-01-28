from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import AuthForm,SignUpForm,QuizForm
from .models import Question1,Stock
from django.db.models import Max  
from django.contrib.auth.models import User
def introduction(request):
    return render(request, "introduction.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form =SignUpForm()
        return render(request, "registration/signup.html", {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
     
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after successful login
            else:
                form.add_error(None, "Invalid username or password")  
        else:
            form.add_error(None, "Form is not valid.") 
    else:
        form = AuthForm()
    
    return render(request, "registration/signin.html", {'form': form})

@login_required
def dashboard(request):
    return render(request, "dashboard.html")
@login_required
def profile(request):
     return render(request, "registration/profile.html",{'user': request.user})
@login_required
def signout(request):
    logout(request)
    return redirect('signin')
@login_required
def leaders(request):
    leaderboard = (
        Stock.objects.values('user') 
        .annotate(high_score=Max('score')) 
        .order_by('-high_score')[:10] 
    )

    for entry in leaderboard:
        user = User.objects.get(id=entry['user'])  # Fetch the User object
        entry['username'] = user.username  # Add the username to the entry

    return render(request, "leaders.html", {'leaderboard': leaderboard})
def quiz1(request):
    questions = Question1.objects.all()
    current_index = request.session.get('current_question', 0)
    history = request.session.get('quiz_history', [])

    if current_index < len(questions):
        question = questions[current_index]
        form = QuizForm(question)

        if request.method == "POST":
            form = QuizForm(question, request.POST)
            if form.is_valid():
                selected_answer = form.cleaned_data[f"answer_{question.id}"]
                history.append({
                    'question': question.question_text,
                    'selected_answer': selected_answer,
                    'correct_answer': question.correct_answer,
                })
                request.session['quiz_history'] = history
                request.session['current_question'] = current_index + 1
                return redirect('quiz1')

        return render(request, 'quiz1.html', {'form': form})
    else:
        request.session['current_question'] = 0
        quiz_history = request.session.pop('quiz_history', [])
        score = sum(1 for item in quiz_history if item['selected_answer'] == item['correct_answer'])

    
        ticker = "QUIZ1"  
        name = "Quiz 1"   
        Stock.objects.create(
            user=request.user,
            ticker=ticker,
            name=name,
            score=score
        )

        return render(request, 'quiz_completed.html', {
            'quiz_history': quiz_history,
            'score': score
        })
