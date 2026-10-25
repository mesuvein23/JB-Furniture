from .models import Category

def category_list(request):
    return {
        'allcategories': Category.objects.all()
    }