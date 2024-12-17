from django.test import TestCase
from .models import TarefaModel
from django.utils import timezone
from datetime import timedelta

class TarefaModelTest(TestCase):
    def test_create_tarefa(self):
        """
        Testa a criação de uma TarefaModel
        """
        
        titulo = "Tarefa de Teste"
        descricao = "Descrição da tarefa de teste."
        hora_inicio = timezone.now()
        hora_fim = hora_inicio + timedelta(hours=2)

        tarefa = TarefaModel.objects.create(
            titulo=titulo,
            descricao=descricao,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

        # Recupera do banco
        tarefa_salva = TarefaModel.objects.get(id=tarefa.id)

        # Asserções para validar os campos
        self.assertEqual(tarefa_salva.titulo, titulo)
