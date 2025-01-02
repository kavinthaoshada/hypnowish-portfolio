# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
from products.models import Category
def manage_product(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'home/manage-product.html', {'categories': categories})

from django.conf import settings
from products.models import Product, ProductDemo, ProductScreenshot, Category
import boto3
def add_product(request):
    if request.method == 'POST':
        # Extract product details from the request
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        icon = request.POST.get('icon')
        image = request.FILES.get('image')

        # Validate required fields
        if not all([name, description, price, category_id]):
            return render(request, 'add_product.html', {
                'error': 'All fields are required.',
                'categories': Category.objects.all()
            })

        # Save the product to the database
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            icon=icon,
            image=image
        )

        # Handle demo and download files
        demo_file = request.FILES.get('demoFile')
        download_file = request.FILES.get('downloadFile')
        if demo_file:
            demo_file_path = upload_to_s3(demo_file, f"products/demos/demo-{product.id}.zip")
        if download_file:
            download_file_path = upload_to_s3(download_file, f"products/downloads/download-{product.id}.zip")

        # Save the ProductDemo entry
        demo_name = request.POST.get('demoName')
        demo_description = request.POST.get('demoDescription', '')
        if demo_name and demo_file_path and download_file_path:
            ProductDemo.objects.create(
                product=product,
                name=demo_name,
                demo_file=demo_file_path,
                description=demo_description,
                download_file=download_file_path
            )

        # Handle screenshots
        screenshots = request.FILES.getlist('screenshots')
        for screenshot in screenshots:
            ProductScreenshot.objects.create(
                product=product,
                image=screenshot
            )

        return redirect('success_url')  # Replace with your success URL

    return render(request, 'add_product.html', {'categories': Category.objects.all()})


def upload_to_s3(file, path):
    """Uploads a file to AWS S3 and returns the S3 path."""
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    try:
        s3.upload_fileobj(file, bucket_name, path)
        return path
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return None

