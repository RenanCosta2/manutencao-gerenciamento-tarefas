import random
from faker import Faker
from django.contrib.auth.models import User
from users.models import UserProfileExample

fake = Faker('pt_BR')

class UserProfileExampleFactory:

    def create_user(self):
        new_user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password()
        )
        return new_user

    def create(self):
        user = self.create_user()
        user_profile = UserProfileExample.objects.create(
            phone_number=fake.phone_number(),
            address=fake.address(),
            birth_date=fake.date_of_birth(),
            user=user
        )
        return user_profile

    def create_multiple(self, num):
        for _ in range(0, num):
            self.create()
