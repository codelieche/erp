# -*- coding:utf-8 -*-
"""
流程实例的过程的执行结果
"""
from django.db import models
from codelieche.models import BaseModel


class ProcessResult(BaseModel):
    """
    过程执行结果
    建议一个proces只写一条结果
    """
    process_id = models.IntegerField(verbose_name="过程")
    success = models.BooleanField(verbose_name="成功", blank=True, default=False)
    content = models.JSONField(verbose_name="执行结果", blank=True, null=True)

    class Meta:
        verbose_name = "过程结果"
        verbose_name_plural = verbose_name
