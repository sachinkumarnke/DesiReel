from .models import Category

def categories(request):
    """
    Add categories to the context for all templates
    """
    return {
        'categories': Category.objects.all()
    }