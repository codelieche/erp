# -*- coding:utf-8 -*-
"""
流程日志
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType

from codelieche.models import BaseModel


class WorkLog(BaseModel):
    """
    流程实例日志
    """
    CATEGORY_CHOICES = (
        ("info", "信息"),
        ("success", "成功"),
        ("error", "错误"),
        ("action", "操作"),
        ("default", "默认"),
    )
    # 这里直接记录用户的username
    user = models.CharField(verbose_name="用户", blank=True, null=True, max_length=64)
    work_id = models.IntegerField(verbose_name="流程实例")
    category = models.CharField(verbose_name="类型", max_length=20, choices=CATEGORY_CHOICES,
                                blank=True, default="info",)
    content = models.CharField(verbose_name="日志内容", blank=True, null=True, max_length=256)

    @property
    def work(self):
        ct = ContentType.objects.get(app_label="workflow", model="work")
        return self.get_relative_object_by_model(model=ct.model_class(), value=self.work_id)

    class Meta:
        verbose_name = "流程实例日志"
        verbose_name_plural = verbose_name
