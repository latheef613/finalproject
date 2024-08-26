from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, MovieForm, ReviewForm
from .models import Movie, Review, Category

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            new_movie = form.save(commit=False)
            new_movie.added_by = request.user
            new_movie.save()
            messages.success(request, 'Movie added successfully.')
            return redirect('index')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, added_by=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully.')
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form})

@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk, added_by=request.user)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
        return redirect('index')
    return render(request, 'delete_movie.html', {'movie': movie})

@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.movie = movie
            new_review.user = request.user
            new_review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

def movies_by_category(request, category):
    category = get_object_or_404(Category, name=category)
    movies = Movie.objects.filter(category=category)
    return render(request, 'movies_by_category.html', {'category': category, 'movies': movies})

def search(request):
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'movies': movies, 'query': query})
