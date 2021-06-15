# -*- coding:utf-8 -*-
import datetime

from cmdb.types import BaseType


class DateTimeField(BaseType):
    """
    时间日期类型
    """

    def stringify(self, value):
        value = self.validate(data=value)
        if value:
            return value.strftime('%F %T')
        else:
            return ''

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        if self.option.get('auto_now'):
            value = datetime.datetime.now()
        else:
            if data:
                value = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
            else:
                auto_now_add = self.option.get('auto_now_add')
                if auto_now_add:
                    value = datetime.datetime.now()
                else:
                    # 默认值
                    default = self.option.get('default')
                    if default:
                        try:
                            value = datetime.datetime.strptime(default, '%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            return None
                    else:
                        return None

        # 对数据进行校验
        _max = self.option.get('max')
        if _max is not None and value > datetime.datetime.strptime(_max, '%Y-%m-%d %H:%M:%S'):
            raise ValueError("{}大于{}".format(value, _max))
        _min = self.option.get('min')
        if _min is not None and value < datetime.datetime.strptime(_min, '%Y-%m-%d %H:%M:%S'):
            raise ValueError("{}小于{}".format(value, _min))
        return value


class DateField(BaseType):
    """
    日期类型
    """

    def stringify(self, value):
        value = self.validate(data=value)
        if value:
            return value.strftime('%F')
        else:
            return ''

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        if self.option.get('auto_now'):
            value = datetime.date.today()
        else:
            if data:
                value = datetime.datetime.strptime(data, '%Y-%m-%d')
            else:
                auto_now_add = self.option.get('auto_now_add')
                if auto_now_add:
                    value = datetime.datetime.today()
                else:
                    # 默认值
                    default = self.option.get('default')
                    if default:
                        try:
                            value = datetime.datetime.strptime(default, '%Y-%m-%d')
                        except Exception as e:
                            return None
                    else:
                        return None

        # 对数据进行校验
        _max = self.option.get('max')
        if _max is not None and value > datetime.datetime.strptime(_max, '%Y-%m-%d'):
            raise ValueError("{}大于{}".format(value.strftime('%F'), _max))
        _min = self.option.get('min')
        if _min is not None and value < datetime.datetime.strptime(_min, '%Y-%m-%d'):
            raise ValueError("{}小于{}".format(value.strftime('%F'), _min))
        return value