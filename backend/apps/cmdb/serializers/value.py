# -*- coding:utf-8 -*-
from rest_framework import serializers

from cmdb.models import Model, Field, Value
from cmdb.tools.field import validate_field_value


class ValueModelSerializer(serializers.ModelSerializer):
    """
    模型实例值 Model Serializer
    """
    model = serializers.SlugRelatedField(slug_field='code', queryset=Model.objects.filter(deleted=False))
    field = serializers.SlugRelatedField(slug_field='code', queryset=Field.objects.filter(deleted=False))

    def validate(self, attrs):
        # 1. 获取到Field，然后校验Field的值
        field = attrs['field']
        instance = attrs['instance']
        if instance.model != attrs['model']:
            raise serializers.ValidationError('传入的Model不匹配')

        # 2. 对值进行校验
        try:
            value = attrs['value']
            # 因为是要保存到数据库Text的类型的，所以使用stringify来校验
            attrs['value'] = validate_field_value(field, value, stringify=True)
        except Exception as e:
            # raise e
            raise serializers.ValidationError('{}'.format(str(e)))

        # 3. 判断Fild是否是唯一的
        if field.unique:
            value = Value.objects.filter(field=field, value=str(value)).first()
            if value and value.instance != instance:
                raise serializers.ValidationError('值为"{}"已经存在，需要唯一'.format(value))
        #
        return attrs

    def create(self, validated_data):
        # 判断是否已经创建了相关的值了
        field = validated_data['field']
        instance = validated_data['instance']

        if not field.multi:
            count = Value.objects.filter(instance=instance, field=field).count()
            if count > 0:
                raise serializers.ValidationError('对象已经创建了字段为{}的值了'.format(field.code))

        value_instance = super().create(validated_data=validated_data)
        return value_instance

    class Meta:
        model = Value
        fields = (
            'id', 'instance', 'model', 'field', 'value',
            'deleted', 'time_added',
        )
