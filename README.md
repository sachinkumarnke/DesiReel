# Movie Streaming Website

This project is organized into three main directories:

## Project Structure

```
WEBSITE/
├── frontend/           # Frontend files
│   ├── templates/      # HTML templates
│   ├── static/         # CSS, JS, and other static files
│   ├── static_root/    # Collected static files
│   └── media/          # User-uploaded content
│
├── backend/            # Backend files
│   ├── core/           # Main application code
│   │   ├── migrations/ # Database migrations
│   │   ├── admin.py    # Admin configuration
│   │   ├── models.py   # Database models
│   │   ├── views.py    # View functions
│   │   └── urls.py     # URL routing
│   │
│   └── movies/         # Project settings
│       ├── settings.py # Django settings
│       ├── urls.py     # Main URL configuration
│       └── wsgi.py     # WSGI configuration
│
└── database/           # Database files
    └── db.sqlite3      # SQLite database
```

## Running the Project

1. Make sure you have Python and Django installed
2. Run the development server:
   ```
   python manage.py runserver
   ```

## Deployment

For production deployment, use the nginx configuration file provided in the root directory.