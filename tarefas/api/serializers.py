from rest_framework.serializers import ModelSerializer
from tarefas.models import TarefaModel

class TarefaSerializer(ModelSerializer):

    class Meta:
        model = TarefaModel
        fields = "__all__"