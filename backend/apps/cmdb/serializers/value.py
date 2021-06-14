# -*- coding:utf-8 -*-
from rest_framework import serializers

from cmdb.models import Model, Field, Value


class ValueModelSerializer(serializers.ModelSerializer):
    """
    模型实例值 Model Serializer
    """
    model = serializers.SlugRelatedField(slug_field='code', queryset=Model.objects.filter(deleted=False))
    field = serializers.SlugRelatedField(slug_field='code', queryset=Field.objects.filter(deleted=False))

    class Meta:
        model = Value
        fields = (
            'id', 'instance', 'model', 'field', 'value',
            'deleted', 'time_added',
        )
