# -*- coding:utf-8 -*-
"""
作业流程的没一个过程
Flow配置的一个Step对应一个Process，可以转交的话，就对应多个了
"""
from django.db import models

from codelieche.models import BaseModel
from workflow.models.workflow import WorkFlow
from workflow.models.step import Step


class Process(BaseModel):
    """
    流程中的过程
    """
    flow = models.IntegerField(verbose_name="流程", blank=True, null=True)
    workflow = models.ForeignKey(verbose_name="流程实例", to=WorkFlow, blank=True, on_delete=models.CASCADE)
    step = models.ForeignKey(verbose_name="步骤", blank=True, on_delete=models.CASCADE)
    plugin_id = models.IntegerField(verbose_name="插件实例的ID", blank=True, null=True)
    status = models.CharField(verbose_name="状态", blank=True, default="todo", max_length=20)

    class Meta:
        verbose_name = "过程"
        verbose_name_plural = verbose_name
