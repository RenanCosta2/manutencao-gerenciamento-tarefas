from django.test import TestCase
from .models import UserProfileExample
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.utils import timezone


class UserProfileExampleTest(TestCase):

    def setUp(self):
        self.new_user = User.objects.create_user(username="admin", password="adminadmin")
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.user_profile = UserProfileExample.objects.create(
            phone_number="12345678901",
            address="Rua de Teste, 123",
            birth_date=timezone.now().date(),
            user=self.new_user
        )

        self.new_user2 = User.objects.create_user(username="admin2", password="adminadmin")

    def test_criar_perfil(self):
        """
        Testa a criação de um perfil de usuário
        """

        url = "http://localhost:8000/users/"

        phone_number = "98765432100"
        address = "Avenida Teste, 456"
        birth_date = timezone.now().date()

        data = {
            "phone_number": phone_number,
            "address": address,
            "birth_date": birth_date,
            "user": self.new_user2.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserProfileExample.objects.filter(phone_number=phone_number).exists())

    def test_listar_perfil(self):
        url = "http://localhost:8000/users/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['phone_number'], "12345678901")

    def test_buscar_perfil(self):
        url = f"http://localhost:8000/users/{self.user_profile.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], "12345678901")

    def test_atualizar_perfil(self):
        url = f"http://localhost:8000/users/{self.user_profile.id}/"

        phone_number = "11223344556"
        address = "Rua Atualizada, 789"
        birth_date = timezone.now().date()

        data = {
            "phone_number": phone_number,
            "address": address,
            "birth_date": birth_date,
            "user": self.new_user.id
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserProfileExample.objects.filter(phone_number=phone_number).exists())

    def test_atualizar_parcial_perfil(self):
        url = f"http://localhost:8000/users/{self.user_profile.id}/"

        phone_number = "22334455667"

        data = {
            "phone_number": phone_number
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserProfileExample.objects.filter(phone_number=phone_number).exists())

    def test_deletar_perfil(self):
        url = f"http://localhost:8000/users/{self.user_profile.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserProfileExample.objects.filter(phone_number="12345678901").exists())
