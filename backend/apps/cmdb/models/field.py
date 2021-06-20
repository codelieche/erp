# -*- coding:utf-8 -*-
from django.db import models

from account.models import User
# from cmdb.types import get_instance
from cmdb.models import Model


class Field(models.Model):
    """
    资产模型的字段
    """

    code = models.SlugField(verbose_name="字段", max_length=40)
    name = models.CharField(verbose_name="字段(中文名)", max_length=60, blank=True, null=True)
    model = models.ForeignKey(verbose_name="模型", related_name="fields", to=Model, on_delete=models.CASCADE)
    # 字段的类型：
    # 比如是：ChartField，TextField
    # 数值类型：IntField、FloatField、
    # 其它类型：BooleanField、IPField、DateField、DateTimeField
    type = models.CharField(verbose_name="字段类型", default="ChartField", max_length=20, blank=True)
    # 是否允许空值
    allow_null = models.BooleanField(verbose_name="允许空值", default=False, blank=True)
    # 是否创建索引、是否唯一、是否多值
    db_index = models.BooleanField(verbose_name="使用索引", default=False, blank=True)
    unique = models.BooleanField(verbose_name="是否唯一", default=False, blank=True)
    multi = models.BooleanField(verbose_name="是否多值", blank=True, default=False)
    # 字段类型的自定义配置选项
    # 比如：IntField的：min、max；ChartField的prefix、suffix
    option = models.JSONField(verbose_name="选项设置", blank=True, null=True)
    # 还其它的元数据信息，联合索引，默认排序等都可写入到这里
    meta = models.JSONField(verbose_name="元数据信息", blank=True, null=True)
    description = models.CharField(verbose_name="描述", blank=True, null=True, max_length=256)
    user = models.ForeignKey(verbose_name="用户", to=User, blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)

    # 会循环引入模块了，故把校验抽离出去
    # def validate_value(self, value, stringify=False):
    #     """
    #     校验字段的值，并返回其类型的值
    #     """
    #     instance = get_instance(self.type, self.option)
    #     if instance:
    #         if stringify:
    #             v = instance.stringify(value=value)
    #         else:
    #             v = instance.destringify(value=value)
    #         return v
    #     else:
    #         return ValueError('校验字段的值出错：未找到类型实例')

    class Meta:
        verbose_name = "资产模型字段"
        verbose_name_plural = verbose_name
        unique_together = ('model', 'code')

    def delete(self, using=None, keep_parents=False):
        if self.deleted:
            return
        else:
            self.deleted = True
            self.save(update_fields=('deleted',))
