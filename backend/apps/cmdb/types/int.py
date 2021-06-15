# -*- coding:utf-8 -*-
from cmdb.types.base import BaseType


class IntField(BaseType):
    """
    Int 类型
    """

    def stringify(self, value):
        return str(self.validate(data=value))

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        value = int(data)
        # 对数据进行校验
        _max = self.option.get('max')
        if _max is not None and value > int(_max):
            raise ValueError("{}大于{}".format(value, _max))
        _min = self.option.get('min')
        if _min is not None and value < int(_min):
            raise ValueError("{}小于{}".format(value, _min))
        return value
