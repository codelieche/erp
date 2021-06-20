# -*- coding:utf-8 -*-

"""
外键关联相关的选项：
- model: 关联的资产Model
- field：关联的字段，这个字段必须是unique，默认可选择id
- on_delete: 当关联的外键删除的时候的操作：cascade | set_null | disable
- on_update: 当关联的外键修改的时候: cascade | disable

这些功能/约束，都是用代码逻辑来实现的，其实尽量不要使用外键：
少用的话，其实可以把约束放到业务代码中
"""

from cmdb.types.base import BaseType
# 注意别循环引用了
from cmdb.models import Model, Field, Instance, Value


class ForeignKey(BaseType):
    """
    外键类型
    """

    def stringify(self, value):
        return str(self.validate(data=value))

    def destringify(self, value):
        return self.validate(data=value)

    def validate(self, data):
        """
        验证数据
        :param data:
        :return:
        """
        # 如果是唯一的那么就需要加锁(因为校验一般是插入/更新的时候才校验)

        # 1. 先校验Model
        model_code = self.option.get('model', None)
        if not model_code:
            raise ValueError('ForeinKey需要关联Model')
        model = Model.objects.filter(code=model_code).first()
        if not model:
            raise ValueError("没有{}类型的Model".format(model_code))

        # 2. 校验Field
        field_code = self.option.get('field', None)
        if not field_code:
            raise ValueError('ForeinKey需要设置关联的field')
        if field_code == 'id':
            value = Instance.objects.filter(model=model, id=int(data), deleted=False).first()
            if not value:
                raise ValueError("对象({})不存在".format(data))
            else:
                return data
        else:
            # 获取ID
            field = Field.objects.filter(model=model, code=field_code).first()
            if not field:
                raise ValueError('{}不存在字段{}'.format(model_code, field_code))

        # 3. 开始校验值
        value = Value.objects.filter(model=model, field=field, value=str(data)).first()
        if not value:
            raise ValueError('值为{}的{}不存在'.format(data, model_code))
        else:
            return data
