from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:movie_id>/rate/', views.rate_movie, name='rate_movie'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('add-to-watchlist/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    
    # Content type and category URLs
    path('content/<str:type_name>/', views.content_type, name='content_type'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('categories/', views.all_categories, name='all_categories'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('settings/', views.update_settings, name='update_settings'),
    
    # Streaming and download
    path('stream/<int:movie_id>/', views.stream_movie, name='stream_movie'),
    path('download/<int:movie_id>/', views.download_movie, name='download_movie'),
    
    # Genre pages
    path('genre/<str:genre_name>/', views.genre_view, name='genre'),
    path('category/name/<str:category_name>/', views.category_by_name, name='category_name'),
    path('new-releases/', views.new_releases, name='new_releases'),
    
    # Help and support pages
    path('faq/', views.faq_view, name='faq'),
    path('support/', views.support_view, name='support'),
    path('contact/', views.contact_view, name='contact'),
    
    # Legal pages
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('cookies/', views.cookies_view, name='cookies'),
    path('about/', views.about_view, name='about'),
    
    # App download pages
    path('apps/ios/', views.ios_app_view, name='ios_app'),
    path('apps/android/', views.android_app_view, name='android_app'),
    path('apps/tv/', views.tv_app_view, name='tv_app'),
    
    # Health check for AWS
    path('health/', views.health_check, name='health_check'),
    
    # Admin access denied page
    path('admin-access-denied/', lambda request: render(request, 'admin/funny_access_denied.html'), name='admin_access_denied'),
]