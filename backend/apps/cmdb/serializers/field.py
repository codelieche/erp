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
        # 情况判断：如果设置的ForeignKey, ManyToManyField就需要判断option的model和field是否存在
        type_ = attrs['type']
        if type_ in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
            model_code = attrs['option'].get('model')
            code = attrs['code']
            if not model_code:
                raise serializers.ValidationError('{}字段的option需要设置model'.format(code))
            model = Model.objects.filter(code=model_code).first()
            if not model:
                raise serializers.ValidationError('{}字段设置的Model({})不存在'.format(code, model_code))

            # 现在校验Field
            field_code = attrs['option'].get('field')
            if not field_code:
                raise serializers.ValidationError('{}字段的option需要设置field'.format(code))
            if field_code != 'id':
                field = Field.objects.filter(model=model, code=field_code).first()
                if not field:
                    raise serializers.ValidationError('{}字段设置的Field({})不存在'.format(code, field_code))
                else:
                    # 校验这个字段是否可设置为外键
                    if not field.unique or field.multi:
                        raise serializers.ValidationError('{}字段设置的Field({})不可设置为关联外键'.format(code, field_code))

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
