# -*- coding:utf-8 -*-
from django.db import models

from account.models import User
from django.contrib.auth.models import Group
from cmdb.models import Model, Instance


class Permission(models.Model):
    """
    资产权限:
    为了便于管理，不设置针对个人用户设置Model权限
    且推荐，是一个分组一个分组的设置
    """
    name = models.CharField(verbose_name="授权名称", max_length=128, unique=True)
    groups = models.ManyToManyField(verbose_name="用户组", to=Group)
    model = models.ManyToManyField(verbose_name="模型", to=Model)
    # 勾选了can_view_all，那么就可查看选中Model的所有权限
    can_view_all = models.BooleanField(verbose_name="能查看所有数据", blank=True, default=False)
    instances = models.ManyToManyField(verbose_name="对象", to=Instance, blank=True)
    description = models.CharField(verbose_name="描述", blank=True, max_length=256, null=True)
    user = models.ForeignKey(verbose_name="用户", to=User, blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)

    class Meta:
        verbose_name = "资产Model数据权限"
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        if self.deleted:
            return
        else:
            self.deleted = True
            self.save(update_fields=('deleted',))
