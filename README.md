# DesiReel - Indian Movie & Web Series Streaming Platform

DesiReel is a comprehensive streaming platform focused on Indian content, including Bollywood, South Indian, and regional movies and web series.

## Features

- **Content Library**: Browse and stream movies and web series
- **User Authentication**: Register, login, and manage user profiles
- **Content Filtering**: Filter by category, year, and sort options
- **Watchlist**: Add content to personal watchlist
- **Rating System**: Rate movies and web series
- **Reviews**: Leave and read user reviews
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Grid/List View**: Toggle between different content viewing modes
- **Admin Panel**: Manage content, users, and site settings (superusers only)

## Technology Stack

- **Backend**: Django 5.0.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django Allauth
- **Media Storage**: Local storage (development), AWS S3 (production)

## Project Structure

```
WEBSITE/
├── frontend/           # Frontend files
│   ├── templates/      # HTML templates
│   │   ├── admin/      # Admin template overrides
│   │   └── core/       # Main application templates
│   ├── static/         # CSS, JS, and other static files
│   ├── static_root/    # Collected static files
│   └── media/          # User-uploaded content (images, videos)
│
├── backend/            # Backend files
│   ├── core/           # Main application code
│   │   ├── migrations/ # Database migrations
│   │   ├── admin.py    # Admin configuration
│   │   ├── models.py   # Database models (Movie, Category, etc.)
│   │   ├── views.py    # View functions
│   │   ├── urls.py     # URL routing
│   │   ├── middleware.py # Custom middleware
│   │   └── context_processors.py # Template context processors
│   │
│   └── movies/         # Project settings
│       ├── settings.py # Django settings
│       ├── urls.py     # Main URL configuration
│       └── wsgi.py     # WSGI configuration
│
├── database/           # Database files
│   └── db.sqlite3      # SQLite database
│
└── venv/               # Virtual environment
```

## Key Models

- **Movie**: Stores movie/series details (title, description, cover image, etc.)
- **Category**: Content categories (Action, Comedy, Drama, etc.)
- **Rating**: User ratings for content
- **Review**: User reviews for content
- **UserProfile**: Extended user information and preferences
- **StreamingContent**: Links to streaming sources

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Unix/MacOS
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   cd backend
   python manage.py migrate
   ```
5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```
7. Access the site at http://127.0.0.1:8000/

## User Roles

- **Regular Users**: Can browse content, create watchlists, rate movies, and leave reviews
- **Staff**: Additional permissions for content management
- **Superusers**: Full access to admin panel and all site features

## Security Features

- CSRF protection
- Admin access restricted to superusers only
- Password validation and security
- Secure media handling

## Frontend Components

- Responsive navigation with user dropdown menu
- Content filtering system with active filter tags
- Grid/list view toggle with localStorage persistence
- Movie detail pages with tabs for information, reviews, and related content
- Custom CSS with consistent color scheme and design language

## Deployment

For production deployment:

1. Update `settings.py` with production settings:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set up a production database
   - Configure static and media file storage

2. Collect static files:
   ```
   python manage.py collectstatic
   ```

3. Use a production-ready web server like Nginx with Gunicorn:
   ```
   gunicorn movies.wsgi:application
   ```

## License

This project is proprietary and not licensed for public use or distribution.

## Contact

For support or inquiries, contact support@desireel.com