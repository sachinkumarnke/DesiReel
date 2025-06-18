from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Movie, Category, Rating, Review, UserProfile, StreamingContent
from datetime import timedelta
import mimetypes
import os

# Home view
def home(request):
    featured_movies = Movie.objects.filter(content_type='movie').order_by('-average_rating')[:10]
    featured_series = Movie.objects.filter(content_type='webseries').order_by('-average_rating')[:10]
    categories = Category.objects.all()[:12]
    
    context = {
        'featured_movies': featured_movies,
        'featured_series': featured_series,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

# Movie detail view
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    related_movies = Movie.objects.filter(category=movie.category).exclude(id=movie_id)[:6]
    
    context = {
        'movie': movie,
        'related_movies': related_movies,
    }
    return render(request, 'core/movie_detail.html', context)

# Search view
def search(request):
    query = request.GET.get('q', '')
    content_type = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', 'relevance')
    
    if query:
        # Base query
        results = Movie.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        ).distinct()
        
        # Apply content type filter
        if content_type:
            results = results.filter(content_type=content_type)
        
        # Apply category filter
        if category_id:
            results = results.filter(category_id=category_id)
        
        # Apply sorting
        if sort == 'newest':
            results = results.order_by('-release_year', 'title')
        elif sort == 'rating':
            results = results.order_by('-average_rating', 'title')
        # Default is relevance, which is the default search order
    else:
        results = Movie.objects.none()
    
    # Get all categories for filter options
    categories = Category.objects.all()
    
    context = {
        'query': query,
        'results': results,
        'categories': categories,
        'selected_type': content_type,
        'selected_category': category_id,
        'selected_sort': sort,
    }
    return render(request, 'core/search.html', context)

# Authentication views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('core:home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Use get_or_create to prevent duplicate UserProfile creation
            UserProfile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}. You can now log in.")
            return redirect('core:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('core:home')

# Rating and review views
@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    rating_value = int(request.POST.get('rating'))
    
    if 1 <= rating_value <= 5:
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'rating': rating_value}
        )
        movie.update_average_rating()
        
    return redirect('core:movie_detail', movie_id=movie_id)

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    content = request.POST.get('content')
    
    if content:
        Review.objects.create(
            user=request.user,
            movie=movie,
            content=content
        )
        messages.success(request, "Your review has been added.")
    
    return redirect('core:movie_detail', movie_id=movie_id)

# Watchlist views
@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if movie in profile.watchlist.all():
        profile.watchlist.remove(movie)
        status = 'removed'
    else:
        profile.watchlist.add(movie)
        status = 'added'
    
    return JsonResponse({'status': status})

@login_required
def remove_from_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if movie in profile.watchlist.all():
        profile.watchlist.remove(movie)
        messages.success(request, f"{movie.title} has been removed from your watchlist.")
    
    # Check if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed'})
    
    return redirect('core:watchlist')

@login_required
def watchlist(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    watchlist_items = profile.watchlist.all()
    
    context = {
        'watchlist_items': watchlist_items,
    }
    return render(request, 'core/watchlist.html', context)

# Content type and category views
def content_type(request, type_name):
    if type_name not in ['movie', 'webseries']:
        return redirect('core:home')
    
    # Get filter parameters
    category_id = request.GET.get('category')
    year = request.GET.get('year')
    sort = request.GET.get('sort', 'newest')
    
    # Base query
    movies = Movie.objects.filter(content_type=type_name)
    
    # Apply filters
    if category_id:
        movies = movies.filter(category_id=category_id)
    
    if year:
        movies = movies.filter(release_year=year)
    
    # Apply sorting
    if sort == 'oldest':
        movies = movies.order_by('release_year', 'title')
    elif sort == 'newest':
        movies = movies.order_by('-release_year', 'title')
    elif sort == 'rating':
        movies = movies.order_by('-average_rating', 'title')
    elif sort == 'az':
        movies = movies.order_by('title')
    elif sort == 'za':
        movies = movies.order_by('-title')
    else:
        # Default sorting to prevent pagination warning
        movies = movies.order_by('id')
    
    # Get all categories and years for filters
    categories = Category.objects.all()
    years = Movie.objects.filter(content_type=type_name).values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'type_name': type_name,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categories': categories,
        'years': years,
    }
    return render(request, 'core/content_list.html', context)

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    movies = Movie.objects.filter(category=category)
    
    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'core/category.html', context)

def all_categories(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'core/categories.html', context)

# Profile views
@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile
    except:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)

@login_required
def update_profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('core:profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'core/update_profile.html', context)

@login_required
def update_settings(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle all settings in one form
        profile.autoplay_videos = 'autoplay_videos' in request.POST
        profile.show_subtitles = 'show_subtitles' in request.POST
        profile.default_language = request.POST.get('default_language', 'en')
        profile.email_notifications = 'email_notifications' in request.POST
        profile.newsletter = 'newsletter' in request.POST
        profile.public_profile = 'public_profile' in request.POST
        
        profile.save()
        
        messages.success(request, "Your settings have been updated.")
        return redirect('core:profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'core/settings.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been updated.")
            return redirect('core:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'core/change_password.html', context)

# Streaming and download views
@login_required
def stream_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    related_movies = Movie.objects.filter(category=movie.category).exclude(id=movie_id)[:5]
    
    # Process video URLs for proper embedding
    if movie.streaming_content.exists():
        streaming_url = movie.streaming_content.first().streaming_url
        if "drive.google.com" in streaming_url:
            # Format Google Drive URLs for embedding
            if "/file/d/" in streaming_url:
                file_id = streaming_url.split("/file/d/")[1].split("/")[0]
                movie.streaming_content.first().streaming_url = f"https://drive.google.com/file/d/{file_id}/preview"
            elif "id=" in streaming_url:
                file_id = streaming_url.split("id=")[1].split("&")[0]
                movie.streaming_content.first().streaming_url = f"https://drive.google.com/file/d/{file_id}/preview"
        elif "youtube.com/watch?v=" in streaming_url:
            # Format YouTube URLs for embedding
            video_id = streaming_url.split("v=")[1].split("&")[0]
            movie.streaming_content.first().streaming_url = f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in streaming_url:
            video_id = streaming_url.split("youtu.be/")[1].split("?")[0]
            movie.streaming_content.first().streaming_url = f"https://www.youtube.com/embed/{video_id}"
    elif movie.video_url:
        if "drive.google.com" in movie.video_url:
            # Format Google Drive URLs for embedding
            if "/file/d/" in movie.video_url:
                file_id = movie.video_url.split("/file/d/")[1].split("/")[0]
                movie.video_url = f"https://drive.google.com/file/d/{file_id}/preview"
            elif "id=" in movie.video_url:
                file_id = movie.video_url.split("id=")[1].split("&")[0]
                movie.video_url = f"https://drive.google.com/file/d/{file_id}/preview"
        elif "youtube.com/watch?v=" in movie.video_url:
            # Format YouTube URLs for embedding
            video_id = movie.video_url.split("v=")[1].split("&")[0]
            movie.video_url = f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in movie.video_url:
            video_id = movie.video_url.split("youtu.be/")[1].split("?")[0]
            movie.video_url = f"https://www.youtube.com/embed/{video_id}"
    
    context = {
        'movie': movie,
        'related_movies': related_movies,
    }
    return render(request, 'core/stream.html', context)

@login_required
def download_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if download is allowed for this movie
    if not movie.allow_download:
        messages.error(request, "Downloads are not available for this content.")
        return redirect('core:movie_detail', movie_id=movie_id)
    
    # Get download URL from movie or streaming content
    download_url = movie.download_url
    if not download_url and movie.streaming_content.exists():
        streaming_content = movie.streaming_content.first()
        if streaming_content and streaming_content.download_url:
            download_url = streaming_content.download_url
    
    if not download_url:
        messages.error(request, "Download link not available.")
        return redirect('core:movie_detail', movie_id=movie_id)
    
    # For local files, you could serve them directly
    # This is a simplified example - in production, you'd handle this differently
    try:
        # If the URL is a local file path
        if os.path.exists(download_url):
            file_path = download_url
            file_name = os.path.basename(file_path)
            
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
        else:
            # For remote URLs, redirect to the URL
            return redirect(download_url)
    except:
        # If any error occurs, redirect to the download URL
        return redirect(download_url)

# New views for genre pages
def genre_view(request, genre_name):
    genre_mapping = {
        'bollywood': 'Bollywood',
        'south-indian': 'South Indian',
        'regional': 'Regional',
    }
    
    genre_title = genre_mapping.get(genre_name, 'Unknown')
    
    # This is a simplified example - in a real app, you'd have proper genre filtering
    if genre_name == 'bollywood':
        movies = Movie.objects.filter(Q(description__icontains='bollywood') | Q(title__icontains='bollywood'))
    elif genre_name == 'south-indian':
        movies = Movie.objects.filter(Q(description__icontains='south indian') | Q(description__icontains='tamil') | 
                                     Q(description__icontains='telugu') | Q(description__icontains='malayalam') | 
                                     Q(description__icontains='kannada'))
    elif genre_name == 'regional':
        movies = Movie.objects.filter(Q(description__icontains='regional') | Q(description__icontains='bengali') | 
                                     Q(description__icontains='marathi') | Q(description__icontains='punjabi'))
    else:
        movies = Movie.objects.none()
    
    # Get related categories
    related_categories = Category.objects.all()[:6]
    
    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'genre_title': genre_title,
        'movies': page_obj,
        'related_categories': related_categories,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'core/genre.html', context)

def category_by_name(request, category_name):
    """View to access categories by name instead of ID"""
    # First try exact match, then case-insensitive match
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        # Try case-insensitive match
        try:
            category = Category.objects.get(name__iexact=category_name)
        except Category.DoesNotExist:
            # Create the category if it doesn't exist (for the main genres)
            if category_name in ["Action", "Comedy", "Drama", "Romance", "Thriller"]:
                category = Category.objects.create(name=category_name)
            else:
                raise
    
    movies = Movie.objects.filter(category=category)
    
    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'core/category.html', context)

def new_releases(request):
    # Get movies released in the last 30 days
    from django.utils import timezone
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_releases = Movie.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at')
    
    # Get a featured new release (the newest one with highest rating)
    featured_release = new_releases.order_by('-average_rating', '-created_at').first()
    
    # Get latest additions (most recently added movies)
    latest_additions = Movie.objects.all().order_by('-created_at')[:12]
    
    paginator = Paginator(new_releases, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'featured_release': featured_release,
        'new_releases': page_obj,
        'latest_additions': latest_additions,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'core/new_releases.html', context)

# Help and support pages
def faq_view(request):
    return render(request, 'core/faq.html')

def support_view(request):
    return render(request, 'core/support.html')

def contact_view(request):
    return render(request, 'core/contact.html')

# Legal pages
def terms_view(request):
    return render(request, 'core/terms.html')

def privacy_view(request):
    return render(request, 'core/privacy.html')

def cookies_view(request):
    return render(request, 'core/cookies.html')

def about_view(request):
    return render(request, 'core/about.html')

# App download pages
def ios_app_view(request):
    return render(request, 'core/ios_app.html')

def android_app_view(request):
    return render(request, 'core/android_app.html')

def tv_app_view(request):
    return render(request, 'core/tv_app.html')

# Health check for AWS
def health_check(request):
    """
    Health check endpoint for AWS Elastic Beanstalk
    """
    return HttpResponse("OK")