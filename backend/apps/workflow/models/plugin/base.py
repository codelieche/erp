# -*- coding:utf-8 -*-
"""
基础插件
"""
from django.db import models

from codelieche.models import BaseModel


class Plugin(BaseModel):
    """
    插件，所有插件都继承自Plugin
    工作流的原子性是插件
    """
    # code = models.SlugField(verbose_name="插件名称", max_length=64, unique=True)
    # name = models.CharField(verbose_name="插件名称(中文)", max_length=128, blank=True, null=True)

    STATUS_CHOICES = (
        ("todo", "Todo"),
        ("doing", "进行中"),
        ("success", "成功"),
        ("error", "出错"),
        ("cancel", "取消"),
        ("deliver", "转交"),
        ("agree", "通过"),
        ("done", "完成"),
    )

    # 插件名称
    code = "plugin"   # 推荐唯一处理，继承Plugin的时候，自行配置
    name = "插件"
    extra_methods = []   # 额外的方法，插件额外可执行的方法

    # 状态
    status = models.CharField(verbose_name="状态", max_length=20, choices=STATUS_CHOICES,
                              blank=True, default="todo")

    def core_task(self):
        raise NotImplementedError("请实现Core Task方法")

    class Meta:
        abstract = True
