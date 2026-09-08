from django.shortcuts import render, redirect
from .models import Movie
import requests
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home(request):
    #We get a POST response from the search bar.
    res = request.POST.get('Search')
    #We receive information from the API about the movies from the result of the search bar.
    response = requests.get(f"http://www.omdbapi.com/?apikey=b2e4f2ec&s={res}")
    data = response.json()
    #We create models for movies. If models for those movies are not created yet, we create new models for them.
    for m in data['Search']:
        try:
            movie = Movie.objects.get(title=m['Title'], year=m['Year'])
        except:
            movie = Movie.objects.create(title=m['Title'], picture=m['Poster'], year=m['Year'])
    movies = Movie.objects.all()
    #We get the movies with the highest amount of preferences.
    topMovies = Movie.objects.order_by('point')[:5]
    return render(request, 'main.html', {'data': data, 'movies': movies, 'topMovies': topMovies})

@login_required(login_url='login')
def like(request, title):
    movie = Movie.objects.get(title=title)
    if movie.dislikeUsers.filter(id=request.user.id).exists():
        movie.point +=1
        movie.dislikeUsers.remove(request.user)
    movie.point += 1
    movie.likeUsers.add(request.user)
    movie.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def dislike(request, title):
    movie = Movie.objects.get(title=title)
    if movie.likeUsers.filter(id=request.user.id).exists():
        movie.point -=1
        movie.likeUsers.remove(request.user)
    movie.point -= 1
    movie.dislikeUsers.add(request.user)
    movie.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def unlike(request, title):
    movie = Movie.objects.get(title=title)
    movie.point-1
    movie.likeUsers.remove(request.user)
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def undislike(request, title):
    movie = Movie.objects.get(title=title)
    movie.point+1
    movie.dislikeUsers.remove(request.user)
    
    return redirect(request.META.get('HTTP_REFERER'))

def loginPage(request):
    if(request.method=="POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        #We search for a user with the username in the server. If we don't find any, then, there's no such user.
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Wrong username or password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')            
        else:
            messages.error(request, "Wrong password")
        
    return render(request, "login.html", {})


def logoutPage(request):
    logout(request)
    return redirect('home')

def signUp(request):
    #We get the user creation form.
    form = UserCreationForm()
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        #If the information on the form is valid, we create a new user and save it.
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error('Invalid Response')
    return render(request, 'signup.html', {'form': form})