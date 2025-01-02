from products.models import Category

def categories_processor(request):
    categories = Category.objects.all()
    return {'context_categories': categories}

from .forms import SubscriberForm

def subscriber_form(request):
    return {'subscriber_form': SubscriberForm()}