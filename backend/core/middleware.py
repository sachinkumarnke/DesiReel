from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import resolve

class AdminAccessMiddleware:
    """
    Middleware to restrict access to the admin site for non-superusers
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the admin site
        if request.path.startswith('/admin/'):
            # Only allow superusers to access admin
            if not request.user.is_authenticated or not request.user.is_superuser:
                return render(request, 'admin/funny_access_denied.html')
        
        response = self.get_response(request)
        return response