# Movie Streaming Website

A Django-based movie streaming platform designed to be hosted on AWS.

## Features

- Movie browsing and streaming
- User authentication
- Watchlist functionality
- Categories and genres
- Search functionality
- Responsive design

## Local Development

1. **Install dependencies**:
   ```
   pip install -r requirements-local.txt
   ```

2. **Run migrations**:
   ```
   cd movies
   python manage.py migrate
   ```

3. **Start the server**:
   ```
   python manage.py runserver
   ```

## Deployment Options

### AWS EC2
See `ec2_deployment_guide.md` for detailed instructions.

### AWS Elastic Beanstalk
Use the `.ebextensions` configuration for easy deployment.

## Project Structure

- `movies/` - Main Django project
  - `core/` - Main application with views, models, and templates
  - `movies/` - Project settings and configuration
- `requirements.txt` - Project dependencies
- `.ebextensions/` - AWS Elastic Beanstalk configuration
- `ec2_setup.sh` - Setup script for EC2 deployment