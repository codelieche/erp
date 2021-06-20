# -*- coding:utf-8 -*-
from cmdb.types import get_instance
from cmdb.models.value import Value


def validate_field_value(field, value, stringify=False):
        """
        校验字段的值，并返回其类型的值
        """
        # 1. 获取类型的实例
        instance = get_instance(field.type, field.option)
        if not instance:
            return ValueError('校验字段的值出错：未找到类型实例')

        # 2. 获取校验后的值
        if stringify:
            v = instance.stringify(value=value)
        else:
            v = instance.destringify(value=value)

        # 3. 对多值进行判断
        # if field.unique:
        #     value = Value.objects.filter(field=field, value=str(v)).first()
        #     if value:
        #         raise ValueError('值为"{}"已经存在，需要唯一'.format(v))

        # 最后返回校验后的值
        return v
