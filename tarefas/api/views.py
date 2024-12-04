from rest_framework import viewsets
from tarefas.models import TarefaModel
from tarefas.api.serializers import TarefaSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class TarefaViewSet(ModelViewSet):
    serializer_class = TarefaSerializer
    permission_classes = [AllowAny]
    queryset = TarefaModel.objects.all()

    def create(self, request):
        serializer = TarefaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hora_inicio = serializer.validated_data['hora_inicio']
        hora_fim = serializer.validated_data['hora_fim']

        # Verificar se o horário da nova tarefa já está ocupado
        in_database = TarefaModel.objects.filter(
            hora_inicio__lt=hora_fim,  # Conflito se o horário de início de alguma tarefa for antes de a nova terminar
            hora_fim__gt=hora_inicio   # Conflito se o horário de fim de alguma tarefa for depois de a nova começar
        ).exists()

        if not in_database:
            
            nova_tarefa = TarefaModel(
                titulo=serializer.validated_data['titulo'],
                descricao=serializer.validated_data['descricao'],
                hora_inicio=serializer.validated_data['hora_inicio'],
                hora_fim=serializer.validated_data['hora_fim'],
            )
            nova_tarefa.save()

            
            serializer_saida = TarefaSerializer(nova_tarefa)
            return Response({"Info": "Tarefa criada!", "data": serializer_saida.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Info": "Horário indisponível"}, status=status.HTTP_409_CONFLICT)
