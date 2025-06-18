from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Movie, Rating, Review, UserProfile, StreamingContent

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie_count')
    search_fields = ('name',)
    
    def movie_count(self, obj):
        return obj.movies.count()
    movie_count.short_description = 'Movies'

class StreamingContentInline(admin.TabularInline):
    model = StreamingContent
    extra = 1
    fields = ('streaming_url', 'download_url', 'is_active')

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'rating', 'created_at')
    can_delete = False
    max_num = 0

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'content', 'rating', 'created_at')
    can_delete = False
    max_num = 0

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'release_year', 'content_type', 'display_rating', 'cover_preview')
    list_filter = ('category', 'content_type', 'release_year', 'allow_download')
    search_fields = ('title', 'description', 'director', 'cast')
    inlines = [StreamingContentInline, RatingInline, ReviewInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'content_type')
        }),
        ('Details', {
            'fields': ('release_year', 'cover_image', 'video_url', 'trailer_url', 'duration', 'director', 'cast')
        }),
        ('Series Info', {
            'fields': ('seasons', 'episodes'),
            'classes': ('collapse',),
            'description': 'Only applicable for web series'
        }),
        ('Download Options', {
            'fields': ('allow_download', 'download_url', 'share_enabled')
        }),
        ('Ratings', {
            'fields': ('average_rating',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('average_rating',)
    
    def display_rating(self, obj):
        rating_value = float(obj.average_rating) if obj.average_rating else 0
        stars = '★' * int(rating_value)
        empty_stars = '☆' * (5 - int(rating_value))
        rating_formatted = f"{rating_value:.1f}"
        return format_html('<span style="color: #FFD700;">{}</span><span style="color: #CCCCCC;">{}</span> ({})', 
                          stars, empty_stars, rating_formatted)
    display_rating.short_description = 'Rating'
    
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="75" style="object-fit: cover; border-radius: 4px;" />', obj.cover_image.url)
        return "No Image"
    cover_preview.short_description = 'Cover'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'display_rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'movie__title')
    
    def display_rating(self, obj):
        stars = '★' * obj.rating
        empty_stars = '☆' * (5 - obj.rating)
        return format_html('<span style="color: #FFD700;">{}</span><span style="color: #CCCCCC;">{}</span>', 
                          stars, empty_stars)
    display_rating.short_description = 'Rating'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'short_content', 'display_rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'movie__title', 'content')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'
    
    def display_rating(self, obj):
        if obj.rating:
            stars = '★' * obj.rating
            empty_stars = '☆' * (5 - obj.rating)
            return format_html('<span style="color: #FFD700;">{}</span><span style="color: #CCCCCC;">{}</span>', 
                              stars, empty_stars)
        return "No Rating"
    display_rating.short_description = 'Rating'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'public_profile', 'email_notifications', 'watchlist_count')
    list_filter = ('public_profile', 'email_notifications', 'newsletter')
    search_fields = ('user__username', 'bio')
    filter_horizontal = ('watchlist',)
    
    def watchlist_count(self, obj):
        count = obj.watchlist.count()
        return format_html('<span style="background-color: #4287f5; color: white; padding: 3px 8px; border-radius: 10px;">{}</span>', count)
    watchlist_count.short_description = 'Watchlist'

@admin.register(StreamingContent)
class StreamingContentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'is_active', 'has_download', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('movie__title',)
    
    def has_download(self, obj):
        return bool(obj.download_url)
    has_download.boolean = True
    has_download.short_description = 'Download'