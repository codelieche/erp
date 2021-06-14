# -*- coding:utf-8 -*-
from django.db import models

from cmdb.models import Model


class Instance(models.Model):
    """
    资产模型实例
    """
    model = models.ForeignKey(verbose_name="资产模型", to=Model, on_delete=models.CASCADE)
    # 存储到MongoDB中对象的ID
    object_id = models.CharField(verbose_name="对象ID", max_length=128, blank=True, null=True, db_index=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    class Meta:
        verbose_name = "资产实例"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        if self.deleted:
            return
        else:
            self.deleted = True
            self.save(update_fields=('deleted',))
