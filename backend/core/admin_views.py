from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Movie, Rating, Review

def admin_login_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    decorated_view_func = staff_member_required(view_func, login_url='core:login')
    return decorated_view_func

def custom_admin_forbidden(request):
    """
    Custom view to handle unauthorized access to admin
    """
    messages.error(request, "You don't have permission to access the admin area.")
    return redirect('core:home')

@staff_member_required
def admin_movie_analytics(request):
    """
    View for movie analytics dashboard
    """
    movies = Movie.objects.all()
    total_movies = movies.count()
    total_ratings = Rating.objects.count()
    total_reviews = Review.objects.count()
    
    context = {
        'total_movies': total_movies,
        'total_ratings': total_ratings,
        'total_reviews': total_reviews,
        'movies': movies[:10],  # Show only 10 most recent movies
    }
    
    return render(request, 'admin/movie_analytics.html', context)