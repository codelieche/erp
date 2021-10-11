# -*- coding:utf-8 -*-
"""
流程
流程由多个Step组合而成
"""
from django.db import models

from codelieche.models import BaseModel


class Flow(BaseModel):
    """
    流程中心的流程
    """
    delete_tasks = ("delete_task_change_code",)

    code = models.SlugField(verbose_name="流程的Code", blank=True, unique=True, max_length=108)
    name = models.CharField(verbose_name="流程", blank=True, max_length=128, null=True)
    user = models.CharField(verbose_name="创建者", blank=True, null=True, max_length=100)

    def delete_task_change_code(self):
        self.code = "{}_del_{}".format(self.code, self.strftime())
        self.save()

    @property
    def steps(self):
        return self.step_set.filter(deleted=False).order_by("order")

    class Meta:
        verbose_name = "流程"
        verbose_name_plural = verbose_name

