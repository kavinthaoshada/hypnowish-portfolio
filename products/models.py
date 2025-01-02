from django.db import models
from django.urls import reverse
import os

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('E-commerce', 'E-commerce'),
        ('Standalone', 'Standalone'),
        ('Mobile', 'Mobile'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='img/thumbnail/', null=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    rating = models.PositiveSmallIntegerField(default=0, help_text="Rating from 1 to 5")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


def demo_file_path(instance, filename):
    return f"products/demos/demo-{instance.product.id}.zip"

def download_file_path(instance, filename):
    return f"products/downloads/download-{instance.product.id}.zip"

class ProductDemo(models.Model):
    """Represents a demo for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='demos')
    name = models.CharField(max_length=255)
    demo_file = models.FileField(upload_to=demo_file_path, help_text="Path to the demo directory in S3")
    description = models.TextField(blank=True, null=True)

    # New field for product download file
    download_file = models.FileField(upload_to=download_file_path, help_text="Path to the downloadable file in S3")

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def get_demo_path(self):
        """
        Returns the demo file's base path to render it as an application.
        """
        return self.demo_file.name

    def get_absolute_url(self):
        """
        Returns the URL to view the demo (public).
        """
        return reverse('view_demo', args=[str(self.id)])
    
    def get_html_file_path(self, screenshot_path):
        """
        Maps a screenshot to its corresponding HTML file in the demo zip.
        """
        screenshot_name = os.path.basename(screenshot_path).split('.')[0]  # Extract 'p-02' from 'img/screen-shots/p-02.jpg'
        product_id = self.product.id
        return f"{screenshot_name}-{product_id}.html"
    
def screenshot_path(instance, filename):
    return f"products/screenshots/{instance.product.id}/"

class ProductScreenshot(models.Model):
    """Represents multiple screenshots for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='products/screenshots/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Screenshot for {self.product.name}"


