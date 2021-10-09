# -*- coding:utf-8 -*-
"""
基础插件
"""
from django.db import models

from codelieche.models import BaseModel
from workflow.models.workflow import WorkFlow


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
        ("refuse", "拒绝"),
        ("cancel", "取消"),
        ("deliver", "转交"),
        ("agree", "通过"),
        ("done", "完成"),
    )

    # 插件信息
    PLUGIN_INFO = {
        "code": "plugin",   # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "插件",
        "description": "插件描述"
    }
    extra_methods = []   # 额外的方法，插件额外可执行的方法

    # 能执行核心任务的process状态，一般都是agree和sucess即可
    CAN_EXECUTE_CORE_TASK_STATUS = ["agree", "success"]

    # 核心任务是否已经执行完毕
    core_task_executed = models.BooleanField(verbose_name="核心任务是否已经执行", blank=True, default=False)
    # 状态
    status = models.CharField(verbose_name="状态", max_length=20, choices=STATUS_CHOICES,
                              blank=True, default="todo")

    def entry_task(self, workflow, process, step):
        """
        进入任务
        :param workflow: 工作流实例
        :param process: 工作流的过程
        :param step: 工作流的步骤
        :return:
        """
        print("现在进入entry_task，请自行实现:", workflow, process, step)
        raise NotImplementedError("请自行实现entry_task")

    def core_task(self, workflow: WorkFlow, process, step):
        raise NotImplementedError("请实现Core Task方法")

    class Meta:
        abstract = True
