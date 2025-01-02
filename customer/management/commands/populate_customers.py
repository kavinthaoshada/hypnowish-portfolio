from django.core.management.base import BaseCommand
from faker import Faker
from customer.models import Customer
import random
from phonenumber_field.modelfields import PhoneNumberField

class Command(BaseCommand):
    help = "Generate fake customers"

    def handle(self, *args, **kwargs):
        faker = Faker()

        for _ in range(10):  # Change the range for the number of customers you want to generate
            username = faker.user_name()
            email = faker.unique.email()
            phone_number = faker.numerify("##########")
            address = faker.address()
            is_email_verified = random.choice([True, False])

            # Create the customer object
            Customer.objects.create_user(
                username=username,
                email=email,
                password="password123",  # Default password for all fake customers
                phone_number=phone_number,
                address=address,
                is_email_verified=is_email_verified,
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated fake customers!"))
