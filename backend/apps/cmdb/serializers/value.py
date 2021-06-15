# -*- coding:utf-8 -*-
from rest_framework import serializers

from cmdb.models import Model, Field, Value


class ValueModelSerializer(serializers.ModelSerializer):
    """
    模型实例值 Model Serializer
    """
    model = serializers.SlugRelatedField(slug_field='code', queryset=Model.objects.filter(deleted=False))
    field = serializers.SlugRelatedField(slug_field='code', queryset=Field.objects.filter(deleted=False))

    def validate(self, attrs):
        # 1. 获取到Field，然后校验Field的值
        field = attrs['field']
        try:
            value = attrs['value']
            # 因为是要保存到数据库Text的类型的，所以使用stringify来校验
            attrs['value'] = field.validate_value(value, stringify=True)
        except Exception as e:
            # raise e
            raise serializers.ValidationError('{}'.format(str(e)))
        return attrs

    class Meta:
        model = Value
        fields = (
            'id', 'instance', 'model', 'field', 'value',
            'deleted', 'time_added',
        )
