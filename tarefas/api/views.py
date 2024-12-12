"""
Importações do Django REST framework e das Tarefas
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from tarefas.models import TarefaModel
from tarefas.api.serializers import TarefaSerializer


class TarefaViewSet(ModelViewSet):
    """
    ViewSet para gerenciamento de Tarefas
    """

    serializer_class = TarefaSerializer
    permission_classes = [AllowAny]
    queryset = TarefaModel.objects.all()

    def create(self, request, *args, **kwargs):

        try:
            serializer = TarefaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            hora_inicio = serializer.validated_data['hora_inicio']
            hora_fim = serializer.validated_data['hora_fim']

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
                    titulo=serializer.validated_data['titulo'],
                    descricao=serializer.validated_data['descricao'],
                    hora_inicio=serializer.validated_data['hora_inicio'],
                    hora_fim=serializer.validated_data['hora_fim'],
                )
                nova_tarefa.save()

                serializer_saida = TarefaSerializer(nova_tarefa)
                return Response(
                    {"Info": "Tarefa criada!", "data": serializer_saida.data},
                    status=status.HTTP_201_CREATED
                    )

            return Response(
                {"Info": "Horário indisponível"},
                status=status.HTTP_409_CONFLICT
                )
        except ValueError:
            return Response(
                {"Erro": "Dados inválidos!"},
                status=status.HTTP_409_CONFLICT
                )
        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST
                )
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissão para isso."},
                status=status.HTTP_403_FORBIDDEN
                )
        except NotAuthenticated:
            return Response(
                {"Erro": "Você não está autenticado."},
                status=status.HTTP_401_UNAUTHORIZED
                )
