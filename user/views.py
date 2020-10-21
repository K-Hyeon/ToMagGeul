from user.models import TMUser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, AuthorCreationForm

def signup(request):
    user_form = UserCreationForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if request.POST.get('is_author', ''):
                author_form = AuthorCreationForm()
                return render(request, 'createauthor.html', {'author_form':author_form, 'user':user})
            return redirect('signin')
    return render(request, 'signup.html', {'regi_form':user_form})

def createauthor(request):
    username = request.GET.get('name', '')
    author_form = AuthorCreationForm()
    if request.method == "POST":
        author_form = AuthorCreationForm(request.POST)
        if author_form.is_valid():
            author = author_form.save(commit=False)
            username = request.POST.get('name', '')
            print(username)
            user = get_object_or_404(TMUser, nickname=username)
            author.user = user
            user.is_author = True
            user.save()
            author.save()
            return redirect('thank')
 
    return render(request, 'createauthor.html', {'author_form':author_form})

def thankyou(request):
    return render(request, 'thankyou.html')


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('thank')

def profile(request):
    return render(request, 'profile.html')
