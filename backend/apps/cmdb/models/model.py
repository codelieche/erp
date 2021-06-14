# -*- coding:utf-8 -*-
from django.db import models

from account.models import User


class Model(models.Model):
    """
    Model：各种资产可以定义一种Model
    """
    code = models.SlugField(verbose_name="Code", max_length=40, unique=True)
    name = models.CharField(verbose_name="名字", max_length=60, blank=True)
    description = models.CharField(verbose_name="描述", blank=True, null=True, max_length=256)
    # 添加用户/管理用户/user字段后续会用到
    user = models.ForeignKey(verbose_name="用户", to=User, blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "资产模型"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        if self.deleted:
            return
        else:
            self.deleted = True
            self.save(update_fields=('deleted',))
