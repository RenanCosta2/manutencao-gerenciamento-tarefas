from django.db import models

# Create your models here.

class TarefaModel(models.Model):

    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"