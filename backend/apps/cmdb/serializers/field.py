# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models import User
from cmdb.models import Model, Field


class FieldModelSerializer(serializers.ModelSerializer):
    """
    模型字段 Model Serializer
    """
    model = serializers.SlugRelatedField(slug_field='code', queryset=Model.objects.filter(deleted=False))
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                        required=False, allow_null=True, )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Field
        fields = (
            'id', 'code', 'name', 'model', 'type', 'db_index', 'unique', 'multi',
            'user', 'option', 'meta', 'description', 'deleted', 'time_added'
        )
        read_only = ('code', 'model')
