from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# from .models import Product
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import CustomerRegistrationForm
from .models import Customer, Subscriber
from products.models import Product, ProductDemo

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.http import JsonResponse, HttpResponseForbidden
from .models import Purchase
from django.http import HttpResponse
import boto3

def custom_404(request, exception):
    context = {
        'error_code': 404,
        'error_message': 'Page Not Found',
        'error_description': 'The page you are looking for does not exist. It might have been moved or deleted.',
    }
    return render(request, 'customer-temp/error_page.html', context, status=404)

def custom_500(request):
    context = {
        'error_code': 500,
        'error_message': 'Server Error',
        'error_description': 'An unexpected error occurred on our server. Please try again later.',
    }
    return render(request, 'customer-temp/error_page.html', context, status=500)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'customer-temp/product_list.html', {'products': products})

def schedule_demo(request):
    products = Product.objects.all()
    return render(request, 'customer-temp/schedule_demo.html', {'products': products})

def about_us(request):
    return render(request, 'customer-temp/about_us.html')

def contact_us(request):
    return render(request, 'customer-temp/contact_us.html')

def customer_home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 9)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'customer-temp/home.html', {'page_obj': page_obj})


def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
            )

            current_site = get_current_site(request)
            subject = 'Activate Your TechInnovate Account'
            message = render_to_string('customer-temp/activate_account_email.html', {
                'user': user,
                'domain': current_site.domain,
                'activation_link': activation_link, 
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Your account has been created! Please confirm your email address to complete registration.')
            return redirect('customer_login') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'customer-temp/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        User = get_user_model()
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('customer_login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('customer_register')



def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if isinstance(user, Customer):
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('customer_home')
            else:
                messages.error(request, 'You are not authorized to access this area.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'customer-temp/login.html')


from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('customer_home')


# @login_required
# def dashboard(request):
#     return render(request, 'customer-temp/dashboard.html')

from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm, SubscriberForm
from two_factor.utils import default_device

@login_required
def customer_profile(request):
    customer = request.user  # Get the currently logged-in customer

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            # Save the form data
            customer = form.save()

            # Check if 2FA toggle was updated
            if customer.two_factor_enabled:
                # Enable 2FA if not already enabled
                if not default_device(customer):
                    messages.info(request, 'Please configure 2FA by setting up your OTP device.')
                    return redirect('two_factor:setup')
            else:
                # Disable 2FA
                if default_device(customer):
                    default_device(customer).delete()
                    messages.success(request, 'Two-factor authentication has been disabled.')

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerProfileForm(instance=customer)

    return render(request, 'customer-temp/profile.html', {'form': form})



def generate_download_link(request, demo_id):
    """
    Generate a pre-signed S3 URL for downloading the product file.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Login required.")

    try:
        purchase = Purchase.objects.get(customer=request.user, product__demos__id=demo_id)
        demo = ProductDemo.objects.get(id=demo_id)

        if purchase.has_expired():
            return JsonResponse({'error': 'Purchase has expired.'}, status=403)

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': demo.download_file.name,
            },
            ExpiresIn=3600,  # 1 hour validity
        )

        return JsonResponse({'download_url': download_url})
    except Purchase.DoesNotExist:
        return HttpResponseForbidden("You haven't purchased this product.")
    except ProductDemo.DoesNotExist:
        return HttpResponse("Demo not found.", status=404)


def subscribe(request):
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                form.save()
                # Send confirmation email
                send_mail(
                    'Subscription Confirmation',
                    'Thank you for subscribing to our newsletter!',
                    'oshadhakavinthajava@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            else:
                return JsonResponse({'success': False, 'message': 'You are already subscribed.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid email address.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})