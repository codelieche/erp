# -*- coding:utf-8 -*-
import json

from rest_framework import serializers

from account.models import User
from cmdb.models import Model, Field
from cmdb.types import type_classes_cache


class FieldModelSerializer(serializers.ModelSerializer):
    """
    模型字段 Model Serializer
    """
    model = serializers.SlugRelatedField(slug_field='code', queryset=Model.objects.filter(deleted=False))
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(),
                                        required=False, allow_null=True, )

    def validate_type(self, value):
        if type_classes_cache.get(value):
            return value
        else:
            raise serializers.ValidationError('传入的类型{}不支持'.format(value))

    def check_json_field(self, value):
        if isinstance(value, str):
            if value:
                try:
                    v = json.loads(value)
                    return v
                except Exception as e:
                    raise serializers.ValidationError("传入的option不是json类型")
            else:
                return {}
        elif isinstance(value, dict):
            return value
        else:
            raise serializers.ValidationError("传入的option不是json类型")

    def validate_option(self, value):
        return self.check_json_field(value=value)

    def validated_meta(self, value):
        return self.check_json_field(value=value)

    def validate(self, attrs):
        # 情况判断：如果设置了
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Field
        fields = (
            'id', 'code', 'name', 'model', 'type', 'allow_null', 'db_index', 'unique', 'multi',
            'user', 'option', 'meta', 'description', 'deleted', 'time_added'
        )
        read_only = ('code', 'model')
