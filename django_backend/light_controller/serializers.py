from rest_framework.serializers import ModelSerializer
from light_controller import models

class CreateChangeSerializer(ModelSerializer):
    class Meta:
        model = models.ColorChange
        fields = [
            'time','red','green','blue'
        ]

class GetChangesSerializer(ModelSerializer):
    class Meta:
        model = models.ColorChange
        fields = ('__all__')


class DeleteChangeSerializer(ModelSerializer):
    class Meta:
        model = models.ColorChange
        fields = ['id']