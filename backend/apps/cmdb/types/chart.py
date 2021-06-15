# -*- coding:utf-8 -*-
from cmdb.types.base import BaseType


class ChartField(BaseType):
    """
    字符类型
    """

    def validate(self, data):
        # 1. 处理值
        # 1-1：默认值处理
        default = self.option.get('default')
        if default and not data:
            data = default

        # 1-2: 把值变成字符
        if isinstance(data, str):
            # 判断是否是字符类型
            value = data
        else:
            value = str(data)
        # 2. 对数据进行校验

        # 2-1. 前缀的判断
        prefix = self.option.get('prefix')
        if prefix and not value.startwith(prefix):
            raise ValueError("{}不是以{}开头".format(value, prefix))
        # 2-2：后缀判断
        suffix = self.option.get('suffix')
        if suffix is not None and not value.endwith(suffix):
            raise ValueError("{}不是以{}结尾".format(value, suffix))
        # 2-3: 最大长度
        max_length = self.option.get('max_length')
        if max_length and len(value) > max_length:
            raise ValueError('字符串的长度大于{}'.format(max_length))
        return value


class TextField(BaseType):
    """
    文本类型
    """

    def stringify(self, value):
        return str(self.validate(data=value))

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        # 1. 处理值
        # 1-1：默认值处理
        default = self.option.get('default')
        if default and not data:
            data = default

        # 1-2: 把值变成字符
        if isinstance(data, str):
            value = data
        else:
            value = str(data)
        # 2. 对数据进行校验
        # 2-1. 前缀的判断
        prefix = self.option.get('prefix')
        if prefix and not value.startwith(prefix):
            raise ValueError("{}不是以{}开头".format(value, prefix))
        # 2-2：后缀判断
        suffix = self.option.get('suffix')
        if suffix is not None and not value.endwith(suffix):
            raise ValueError("{}不是以{}结尾".format(value, suffix))
        return value
