from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from products.models import Product, ProductDemo
from django.utils.timezone import now, timedelta

import boto3
from django.conf import settings
from botocore.exceptions import NoCredentialsError

def default_expiration_date():
    """Calculate the default expiration date as 7 days from now."""
    return now() + timedelta(days=7)
    
class Customer(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchases")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=default_expiration_date)

    def has_expired(self):
        return now() > self.expiration_date

    def get_download_link(self, demo_file_key, expiration=3600):
        """
        Generate a time-limited S3 pre-signed URL for the given file key.

        :param demo_file_key: Path to the file in the S3 bucket
        :param expiration: Time in seconds for the link to be valid
        :return: Pre-signed URL or None if link generation fails
        """
        if self.has_expired():
            return None

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': demo_file_key,
                },
                ExpiresIn=expiration,  # Default: 1 hour
            )
            return url
        except NoCredentialsError:
            return None
        
class ProductInteraction(models.Model):
    """Logs customer interactions with product demos."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    demo = models.ForeignKey(ProductDemo, on_delete=models.SET_NULL, null=True, blank=True)
    interaction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction with {self.product.name} by {self.customer or 'Guest'}"
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email