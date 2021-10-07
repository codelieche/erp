# -*- coding:utf-8 -*-
"""
流程日志
"""
from django.db import models

from codelieche.models import BaseModel
from workflow.models.workflow import WorkFlow


class WorkFlowLog(BaseModel):
    """
    流程实例日志
    """
    CATEGORY_CHOICES = (
        ("info", "信息"),
        ("success", "成功"),
        ("error", "错误"),
        ("default", "默认"),
    )
    workflow = models.ForeignKey(verbose_name="流程实例", to=WorkFlow, on_delete=models.CASCADE)
    category = models.CharField(verbose_name="类型", max_length=20, choices=CATEGORY_CHOICES,
                                blank=True, default="info",)
    content = models.CharField(verbose_name="日志内容", blank=True, null=True, max_length=256)

    class Meta:
        verbose_name = "流程实例日志"
        verbose_name_plural = verbose_name
