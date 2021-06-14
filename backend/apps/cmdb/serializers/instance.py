# -*- coding:utf-8 -*-
from rest_framework import serializers

from cmdb.models import Instance, Model


class InstanceModelSerializer(serializers.ModelSerializer):
    """
    模型实例 Model Serializer
    """

    model = serializers.SlugRelatedField(slug_field='code', queryset=Model.objects.filter(deleted=False))

    class Meta:
        model = Instance
        fields = (
            'id', 'model', 'object_id',
            'deleted', 'time_added',
        )
        read_only_fields = ('model', 'object_id')
