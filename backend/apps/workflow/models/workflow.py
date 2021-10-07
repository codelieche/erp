# -*- coding:utf-8 -*-
"""
具体的流程实例
"""

from django.db import models

from codelieche.models import BaseModel
from account.models import User
from workflow.models.flow import Flow


class WorkFlow(BaseModel):
    """
    工作流程，具体的每一条流程实例
    后续随着数据的增加，可实现分库分表，每类flow，放一张表中,workflow_flow_[code]的表
    这样的话code确定了之后就不可修改了
    """
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
    # 根据不同的状态，重新保存一下status_code
    STATUS_CODE_DICT = {
        "todo": 1,
        "doing": 5,
        "success": 15,
        "error": 15,
        "cancel": 50,
        "deliver": 15,
        "agree": 15,
        "done": 30,
    }
    flow = models.ForeignKey(verbose_name="流程", to=Flow, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="流程标题", blank=True, null=True, max_length=256)
    creator = models.ForeignKey(verbose_name="创建者", to=User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(verbose_name="状态", blank=True, default="todo", max_length=20)
    status_code = models.SmallIntegerField(verbose_name="状态码", blank=True, default=0)
    current = models.IntegerField(verbose_name="当前步骤", blank=True, null=True)
    # 当前流程的数据，后续插件都会来这里取数据：step_id: {}  集合 step.data 组合实例化Plugin
    data = models.TextField(verbose_name="流程数据", blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 校验status
        if not self.status:
            self.status = "todo"

        # 设置status_code
        if self.status_code != self.STATUS_CODE_DICT[self.status]:
            self.status_code = self.STATUS_CODE_DICT[self.status]
        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)

    class Meta:
        verbose_name = "流程实例"
        verbose_name_plural = verbose_name
        ordering = ("status_code", "-id")
