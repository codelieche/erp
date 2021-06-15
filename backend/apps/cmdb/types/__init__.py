# -*- coding:utf-8 -*-
import json
from .base import (
    type_classes_cache, type_instance_cache,
    BaseType,
)
from .chart import ChartField, TextField
from .int import IntField
from .float import FloatField
from .ip import IPAddressField
from .datetime import DateField, DateTimeField
from .dict import JsonField


def get_class(type_: str):
    """
    获取CMDB模型字段类型的类
    """
    # 1. 从缓存中获取类
    cls = type_classes_cache.get(type_)
    if cls:
        return cls

    # 2. 如果没有就需要判断是否需要注入类
    raise TypeError('未找到{}类型的类'.format(type_))


def get_instance(type_: str, option: dict):
    """
    获取CMDB类型的实例
    """
    # 1. 先获取到类型的类
    cls = get_class(type_)

    if cls:
        # 2. 对类和选项实例化这个类型
        if isinstance(option, str):
            try:
                option = json.loads(option)
            except:
                print('传入的Option有误：{}'.format(option))
                option = {}
        instance_key = ','.join("{}={}".format(k, v) for k, v in sorted(option.items()))
        instance_key = "{}__{}".format(type_, instance_key)

        # 从缓存中获取类实例
        instance = type_instance_cache.get(instance_key)
        if instance:
            return instance
        else:
            # 实例化类的实例，并缓存类的实例
            instance = cls(option)
            type_instance_cache[instance_key] = instance
            return instance
    else:
        raise ValueError("类型{}不存在".format(type_))


def inject_class():
    """
    程序一启动就注入类到type_classes_cache中
    """
    # print(globals())
    for name, value in globals().items():
        if type(value) == type and issubclass(value, BaseType) and name != 'BaseType':
            # print(name, value)
            type_classes_cache[name] = value
            # cmdb.type.IPAddressField
            type_classes_cache["{}.{}".format(__name__, name)] = value


# 执行类的注入
inject_class()


def test_instance():

    obj = {
        "type": "IntField",
        "value": "999",
        "option": {
            "max": 10000,
            "min": 0
        }
    }
    instance = get_instance(obj['type'], obj['option'])
    print('instance:', instance)
    print(
        instance.stringify(obj['value']),
        instance.destringify(obj['value'])
    )
    return instance
