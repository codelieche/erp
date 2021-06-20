# -*- coding:utf-8 -*-
import json
from django.db import models

# 缓存类型和类型的实例
type_classes_cache = {
    # "IPField": 'xxxx'
}
type_instance_cache = {
    # "IPField_option_xxx": "xxx"
}
# models.EmailField
# models.OneToOneField


class BaseType:
    """
    基础类型
    """
    def __init__(self, option):
        # 在这里option需要是个字典
        if isinstance(option, dict):
            self.__dict__['option'] = option
        # elif isinstance(option, str):
        #     try:
        #         op = json.loads(option)
        #         self.__dict__['option'] = op
        #     except Exception as e:
        #         print('传递的option有误：{}'.format(op))
        #         self.__dict__['option'] = {}
        else:
            self.__dict__['option'] = {}

    def __getattr__(self, item):
        return self.option.get(item)

    def __setattr__(self, key, value):
        # 拒绝动态添加属性进来
        raise ValueError("不可设置值")

    def stringify(self, value):
        """校验值并返回字符串"""
        return str(self.validate(data=value))

    def destringify(self, value):
        """校验值并返回目标类型的值"""
        # raise NotImplementedError('请自行实现：destringify')
        return self.validate(data=value)

    def validate(self, data):
        """对传入的数据进行校验"""
        raise NotImplementedError()
