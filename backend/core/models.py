from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Movie(models.Model):
    CONTENT_TYPES = (
        ('movie', 'Movie'),
        ('webseries', 'Web Series'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='movies')
    release_year = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='covers/')
    video_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)
    duration = models.CharField(max_length=10, blank=True)
    director = models.CharField(max_length=100, blank=True)
    cast = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='movie')
    seasons = models.PositiveIntegerField(default=0, help_text="Number of seasons (for web series only)")
    episodes = models.PositiveIntegerField(default=0, help_text="Number of episodes (for web series only)")
    allow_download = models.BooleanField(default=False)
    download_url = models.URLField(blank=True)
    share_enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def update_average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            self.average_rating = avg_rating
            self.save()

class StreamingContent(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='streaming_content')
    streaming_url = models.URLField(help_text='URL for streaming the movie')
    download_url = models.URLField(blank=True, null=True, help_text='URL for downloading the movie')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie.title} - Streaming Content"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_average_rating()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    watchlist = models.ManyToManyField(Movie, blank=True, related_name='in_watchlists')
    
    # Notification settings
    email_notifications = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    notify_new_releases = models.BooleanField(default=True)
    notify_recommendations = models.BooleanField(default=True)
    
    # Privacy settings
    public_profile = models.BooleanField(default=False)
    show_activity = models.BooleanField(default=True)
    
    # Preferences
    autoplay_videos = models.BooleanField(default=True)
    show_subtitles = models.BooleanField(default=False)
    default_language = models.CharField(max_length=5, default='en')
    
    def __str__(self):
        return self.user.username