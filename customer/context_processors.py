from products.models import Category

def categories_processor(request):
    categories = Category.objects.all()
    return {'context_categories': categories}

from .forms import SubscriberForm, CheckoutForm

def subscriber_form(request):
    return {'subscriber_form': SubscriberForm()}

def checkout_form(request):
    return {'checkout_form': CheckoutForm()}