# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models import User
from cmdb.models import Model
from cmdb.serializers.field import FieldModelSerializer


class ModelSerializer(serializers.ModelSerializer):
    """
    资产模型 Model Serializer
    """
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                        required=False, allow_null=True,)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Model
        fields = (
            'id', 'code', 'name', 'user',
            'description', 'deleted', 'time_added'
        )


class ModelInfoSerializer(serializers.ModelSerializer):
    """
    资产模型 Info Serializer
    """

    fields = FieldModelSerializer(many=True, required=False, read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                        required=False, allow_null=True, )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Model
        fields = (
            'id', 'code', 'name', 'fields', 'user',
            'description', 'deleted', 'time_added'
        )
