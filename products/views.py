from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
import boto3
from django.conf import settings
from .models import ProductDemo, Category

import os
import zipfile
from django.core.files.storage import default_storage

def product_detail(request, id):
    from products.models import Product
    product = Product.objects.get(pk=id)
    return render(request, 'customer-temp/featured_products.html', {'product': product})

def view_demo(request, demo_id):
    """
    Render the demo HTML file stored in S3 for public access.
    """
    try:
        demo = ProductDemo.objects.get(id=demo_id)
        demo_path = demo.get_demo_path()

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Get the HTML file from the demo directory
        html_key = f"{demo_path}/index.html"  # Assuming `index.html` is the main entry point
        response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=html_key)
        html_content = response['Body'].read().decode('utf-8')

        return HttpResponse(html_content, content_type='text/html')
    except ProductDemo.DoesNotExist:
        return HttpResponse("Demo not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)

import os
import zipfile
import boto3
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404
from products.models import ProductDemo, Product
import logging

logger = logging.getLogger(__name__)

def serve_demo_file(request, product_id):
    # Get the product demo and corresponding S3 path
    demo = get_object_or_404(ProductDemo, product__id=product_id)
    zip_file_path = demo.demo_file.name  # Path in S3

    # Local paths for download and extraction
    local_zip_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(zip_file_path))
    extracted_folder = os.path.join(settings.MEDIA_ROOT, 'products/demos/', str(product_id))
    os.makedirs(extracted_folder, exist_ok=True)

    # Log paths for debugging
    logger.info(f"Local zip path: {local_zip_path}")
    logger.info(f"S3 path: {zip_file_path}")

    # Download the zip file from S3 if not already present locally
    if not os.path.exists(local_zip_path):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        try:
            logger.info(f"Downloading {zip_file_path} from S3...")
            s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, zip_file_path, local_zip_path)
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise Http404(f"Unable to download demo file from S3: {str(e)}")

    # Extract the zip file
    try:
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)
    except zipfile.BadZipFile:
        logger.error(f"File {local_zip_path} is not a valid zip file.")
        raise Http404("Invalid zip file. Please check the source file.")

    # Serve the `index.html` file
    index_html_path = os.path.join(extracted_folder, 'index.html')

    if not os.path.exists(index_html_path):
        raise Http404("index.html not found in the extracted demo.")

    return FileResponse(open(index_html_path, 'rb'), content_type='text/html')
    
    
def category_form_view(request):
    categories = Category.objects.all()
    return render(request, 'manage-product.html', {'categories': categories})

from django.db.models import Q
from difflib import SequenceMatcher
from django.core.paginator import Paginator
from decimal import Decimal

def calculate_similarity(text1, text2):
    """
    Calculates the similarity percentage between two text strings using SequenceMatcher.
    """
    return SequenceMatcher(None, text1, text2).ratio() * 100

def single_product_detail(request, pk):
    # Get the product object or return a 404
    product = get_object_or_404(Product, pk=pk)
    screenshots = product.screenshots.all()
    category = product.category

    # Convert floats to Decimal for arithmetic with product.price
    price_range_lower = product.price * Decimal('0.8')
    price_range_upper = product.price * Decimal('1.2')

    # Query for potential similar products
    similar_products_query = Product.objects.filter(
        Q(category=product.category) |  # Same category
        Q(price__gte=price_range_lower, price__lte=price_range_upper)  # Within 20% price range
    ).exclude(pk=pk)
    
    similar_products = [
        other_product for other_product in similar_products_query
        if calculate_similarity(product.description, other_product.description) > 60
    ]
    
    paginator = Paginator(similar_products, 9)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer-temp/product_detail.html', {
        'product': product,
        'screenshots': screenshots,
        'category': category,
        'page_obj': page_obj,
    })