# -*- coding:utf-8 -*-
import json

from cmdb.types import BaseType


class JsonField(BaseType):
    """
    Dict/Json 类型
    """

    def stringify(self, value):
        return json.dumps(self.validate(data=value))

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        if isinstance(data, str):
            if data:
                value = json.loads(data)
            else:
                value = {}
        elif isinstance(data, dict):
            value = data
        elif isinstance(data, list):
            value = data
        else:
            value = {}

        # 对数据进行校验
        # _max = self.option.get('max')
        # if _max is not None and value > _max:
        #     raise ValueError("{}大于{}".format(value, _max))
        # _min = self.option.get('min')
        # if _min is not None and value < _min:
        #     raise ValueError("{}小于{}".format(value, _min))
        return value
