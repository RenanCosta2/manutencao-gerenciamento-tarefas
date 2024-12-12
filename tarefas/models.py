"""
Importações do Django
"""
from django.db import models


class TarefaModel(models.Model):
    """
    Model de Tarefa
    """
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()

    def __str__(self):
        return f'{self.titulo}'

    class Meta:
        """
        Nomes de Tarefas
        """
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
