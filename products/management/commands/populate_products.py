import os
import random
from faker import Faker
from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductDemo, ProductScreenshot

fake = Faker()

# Base directory for media files
BASE_THUMBNAIL_DIR = 'img/thumbnail/'
BASE_SCREENSHOT_DIR = 'img/screen-shots/'

class Command(BaseCommand):
    help = "Populate the database with dummy products and categories"

    def handle(self, *args, **kwargs):
        self.populate_categories()
        self.populate_products()

    def populate_categories(self):
        categories = ['E-commerce', 'Standalone', 'Mobile', 'Other']
        for category in categories:
            Category.objects.get_or_create(name=category, description=fake.text())

    def populate_products(self):
        categories = Category.objects.all()
        for _ in range(10):  # Create 10 products
            category = random.choice(categories)
            product = Product.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(),
                price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                category=category,
                image=f"{BASE_THUMBNAIL_DIR}{random.choice(['p-01.jpg', 'p-02.jpg', 'p-03.jpg', 'p-04.jpg', 'p-06.jpg', 'p-07.jpg'])}",
                icon=f"fa-{fake.word()}",
                rating=random.randint(1, 5),
            )
            self.populate_product_screenshots(product)
            self.populate_product_demos(product)

    def populate_product_screenshots(self, product):
        screenshot_files = ['p-01.jpg', 'p-02.jpg', 'p-03.jpg', 'p-04.jpg', 'p-05.jpg', 'p-06.jpg', 'p-07.jpg']
        for _ in range(random.randint(1, 3)):  # Create 1 to 3 screenshots
            ProductScreenshot.objects.create(
                product=product,
                image=f"{BASE_SCREENSHOT_DIR}{random.choice(screenshot_files)}",
                caption=fake.sentence(),
            )

    def populate_product_demos(self, product):
        for _ in range(random.randint(1, 2)):  # Create 1 to 2 demos
            ProductDemo.objects.create(
                product=product,
                name=f"{product.name} Demo",
                demo_file=f"products/demos/demo_file.zip",
                download_file=f"products/downloads/download_file.zip",
                description=fake.text(),
            )
