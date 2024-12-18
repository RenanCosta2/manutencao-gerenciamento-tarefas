from django.test import TestCase
from .models import TarefaModel
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class TarefaModelTest(TestCase):

    def setUp(self):
        titulo = "Tarefa Inicial"
        descricao = "Descrição da tarefa inicial."
        hora_inicio = timezone.now()
        hora_fim = hora_inicio + timedelta(hours=5)

        self.nova_tarefa = TarefaModel.objects.create(
            titulo=titulo,
            descricao=descricao,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

        self.new_user = User.objects.create_user(username="admin", password="adminadmin")
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_criar_tarefa(self):
        """
        Testa a criação de uma Tarefa
        """

        url = "http://localhost:8000/tarefas/"

        titulo = "Tarefa de Teste"
        descricao = "Descrição da tarefa de teste."
        hora_inicio = timezone.now() + timedelta(hours=10)
        hora_fim = hora_inicio + timedelta(hours=12)

        data = {
            "titulo": titulo,
            "descricao": descricao,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim
        }

        response = self.client.post(url, data)

        # Asserções para validar os campos
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TarefaModel.objects.filter(titulo=titulo).exists())

    def test_listar_tarefa(self):

        url = "http://localhost:8000/tarefas/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['titulo'], "Tarefa Inicial")

    def test_buscar_tarefa(self):

        url = f"http://localhost:8000/tarefas/{self.nova_tarefa.id}/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], "Tarefa Inicial")

    def test_atualizar_tarefa(self):

        url = f"http://localhost:8000/tarefas/{self.nova_tarefa.id}/"

        titulo = "Tarefa Atualizada"
        descricao = "Descrição da tarefa inicial."
        hora_inicio = timezone.now()
        hora_fim = hora_inicio + timedelta(hours=5)

        data = {
            "titulo": titulo,
            "descricao": descricao,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TarefaModel.objects.filter(titulo=titulo).exists())

    def test_atualizar_parcial_tarefa(self):

        url = f"http://localhost:8000/tarefas/{self.nova_tarefa.id}/"

        titulo = "Tarefa Atualizada Parcial"

        data = {
            "titulo": titulo
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TarefaModel.objects.filter(titulo=titulo).exists())

    def test_deletar_tarefa(self):

        url = f"http://localhost:8000/tarefas/{self.nova_tarefa.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TarefaModel.objects.filter(titulo="Tarefa Inicial").exists())
