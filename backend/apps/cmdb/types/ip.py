# -*- coding:utf-8 -*-
import ipaddress

from cmdb.types.base import BaseType


class IPAddressField(BaseType):
    """
    IP 类型
    """

    def stringify(self, value):
        return str(self.validate(data=value))

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        value = ipaddress.ip_address(data)
        # 判断前缀
        prefix = self.option.get('prefix')
        if prefix and not str(value).startswith(prefix):
            raise ValueError("{}不是以{}开头".format(value, prefix))
        return value
