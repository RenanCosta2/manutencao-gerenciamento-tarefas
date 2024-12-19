"""
Importações do Django REST framework e das Tarefas
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.exceptions import NotFound
from tarefas.models import TarefaModel
from tarefas.api.serializers import TarefaSerializer
from tarefas import services

DADOS_INVALIDOS = "Dados inválidos!"
DADO_INCORRETO = "Algum dado faltando ou errado."
PERMISSAO = "Você não possui permissão para isso."
AUTENTICACAO = "Você não está autenticado."


class TarefaViewSet(ModelViewSet):
    """
    ViewSet para gerenciamento de Tarefas
    """

    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]
    queryset = TarefaModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = TarefaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:

            nova_tarefa = services.create(serializer.validated_data)

            if nova_tarefa:
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
                {"Erro": DADOS_INVALIDOS},
                status=status.HTTP_409_CONFLICT
                )
        except KeyError:
            return Response(
                {"Erro": DADO_INCORRETO},
                status=status.HTTP_400_BAD_REQUEST
                )
        except PermissionDenied:
            return Response(
                {"Erro": PERMISSAO},
                status=status.HTTP_403_FORBIDDEN
                )
        except NotAuthenticated:
            return Response(
                {"Erro": AUTENTICACAO},
                status=status.HTTP_401_UNAUTHORIZED
                )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"Erro": DADOS_INVALIDOS},
                status=status.HTTP_409_CONFLICT
                )
        except KeyError:
            return Response(
                {"Erro": DADO_INCORRETO},
                status=status.HTTP_400_BAD_REQUEST
                )
        except PermissionDenied:
            return Response(
                {"Erro": PERMISSAO},
                status=status.HTTP_403_FORBIDDEN
                )
        except NotAuthenticated:
            return Response(
                {"Erro": AUTENTICACAO},
                status=status.HTTP_401_UNAUTHORIZED
                )
        except NotFound:
            return Response(
                {"Erro": "Tarefa não encontrada."},
                status=status.HTTP_404_NOT_FOUND
                )

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
                )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"Erro": DADOS_INVALIDOS},
                status=status.HTTP_409_CONFLICT
                )
        except KeyError:
            return Response(
                {"Erro": DADO_INCORRETO},
                status=status.HTTP_400_BAD_REQUEST
                )
        except PermissionDenied:
            return Response(
                {"Erro": PERMISSAO},
                status=status.HTTP_403_FORBIDDEN
                )
        except NotAuthenticated:
            return Response(
                {"Erro": AUTENTICACAO},
                status=status.HTTP_401_UNAUTHORIZED
                )
        except NotFound:
            return Response(
                {"Erro": "Tarefa não encontrada."},
                status=status.HTTP_404_NOT_FOUND
                )
