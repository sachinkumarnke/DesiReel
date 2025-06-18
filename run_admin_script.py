import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
django.setup()

# Create a superuser
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print("Superuser 'admin' created successfully!")
else:
    # Update the existing admin user to ensure they have staff and superuser permissions
    admin = User.objects.get(username='admin')
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password('adminpassword')
    admin.save()
    print("Superuser 'admin' updated successfully!")