import os
import joblib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Correct import
from .models import NewsArticle

# Load model and vectorizer with absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'fake_news_model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'vectorizer.pkl')

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    model = None
    vectorizer = None
    print(f"Error loading model/vectorizer: {e}")

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('detect_news')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('slider')

@login_required
def detect_news(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if model and vectorizer:
            text_vectorized = vectorizer.transform([text])
            prediction = model.predict(text_vectorized)[0]
            is_fake = bool(prediction)
            NewsArticle.objects.create(user=request.user, text=text, is_fake=is_fake)
            messages.success(request, 'Prediction completed successfully!')
        else:
            messages.error(request, 'Error: Model or vectorizer not loaded correctly.')
            is_fake = None
        return render(request, 'result.html', {'is_fake': is_fake, 'text': text})
    return render(request, 'detect_news.html')

@login_required
def history(request):
    articles = NewsArticle.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'articles': articles})

def slider(request):
    return render(request, 'slider.html')