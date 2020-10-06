from rest_framework import serializers

from api.models import Number


class NumberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'operation_id', 'number']
