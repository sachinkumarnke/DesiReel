from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .models import Movie, Category, Rating, Review, UserProfile

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Movie statistics
        context['total_movies'] = Movie.objects.count()
        context['avg_rating'] = Rating.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        context['total_reviews'] = Review.objects.count()
        
        # User statistics
        context['total_users'] = UserProfile.objects.count()
        
        # Category statistics
        categories = Category.objects.annotate(movie_count=Count('movies'))
        context['categories'] = categories
        
        # Recent content
        context['recent_movies'] = Movie.objects.order_by('-created_at')[:5]
        context['recent_reviews'] = Review.objects.order_by('-created_at')[:5]
        
        # Top rated movies
        context['top_rated'] = Movie.objects.filter(average_rating__gt=0).order_by('-average_rating')[:5]
        
        return context