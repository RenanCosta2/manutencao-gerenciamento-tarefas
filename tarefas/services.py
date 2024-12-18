from .models import TarefaModel

def create(data):
    hora_inicio = data['hora_inicio']
    hora_fim = data['hora_fim']

    # Verificar se o horário da nova tarefa já está ocupado
    in_database = TarefaModel.objects.filter(
        # Conflito se o horário de início de alguma tarefa
        # for antes de a nova terminar
        hora_inicio__lt=hora_fim,
        # Conflito se o horário de fim de alguma tarefa
        # for depois de a nova começar
        hora_fim__gt=hora_inicio
    ).exists()

    if not in_database:

        nova_tarefa = TarefaModel(
            titulo=data['titulo'],
            descricao=data['descricao'],
            hora_inicio=data['hora_inicio'],
            hora_fim=data['hora_fim'],
        )
        nova_tarefa.save()

        return nova_tarefa
