from datetime import timedelta
import random 
from faker import Faker

from .models import TarefaModel

fake = Faker('pt_BR')

class TarefaFactory:

    def create(self):
        titulo = fake.sentence(nb_words=6),
        descricao = fake.text(max_nb_chars=300),
        hora_inicio = fake.date_time_this_month(before_now=True, after_now=False),
        hora_fim = hora_inicio + timedelta(hours=random.randint(1, 3))
        
        nova_tarefa = TarefaModel.objects.create(
            titulo = titulo,
            descricao = descricao,
            hora_inicio = hora_inicio,
            hora_fim = hora_fim
        )

        return nova_tarefa

    def create_multiple(self, num):
        for _ in range(0,num):
            self.create()