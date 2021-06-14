# -*- coding:utf-8 -*-
from django.db import models

from cmdb.models import Instance, Model, Field


class Value(models.Model):
    """
    资产模型的值
    """
    instance = models.ForeignKey(verbose_name="资产实例", to=Instance,
                                 related_name="values", on_delete=models.CASCADE)
    model = models.ForeignKey(verbose_name="资产模型", to=Model, on_delete=models.SET_NULL, blank=True, null=True)
    field = models.ForeignKey(verbose_name="信息字段", to=Field, on_delete=models.CASCADE)
    # 对于值的类型、各种约束的限制，信息值在add和update的时候通过代码逻辑控制处理
    value = models.TextField(verbose_name="信息值", blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    class Meta:
        verbose_name = "信息值"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        if self.deleted:
            return
        else:
            self.deleted = True
            self.save(update_fields=('deleted',))
