# -*- coding:utf-8 -*-
"""
具体的流程实例
"""
import json

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
        ("refuse", "拒绝"),
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
        "error": 30,   # 出错、拒绝、成功、完成应该是一个级别的
        "refuse": 30,
        "cancel": 50,
        "deliver": 15,
        "agree": 15,
        "done": 30,
    }
    flow = models.ForeignKey(verbose_name="流程", to=Flow, on_delete=models.CASCADE)
    # 标题是必填的
    title = models.CharField(verbose_name="流程标题", max_length=256)
    user = models.ForeignKey(verbose_name="创建者", to=User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(verbose_name="状态", blank=True, default="todo", max_length=20)
    status_code = models.SmallIntegerField(verbose_name="状态码", blank=True, default=0)
    current = models.IntegerField(verbose_name="当前步骤", blank=True, null=True)
    # 当前流程的数据，后续插件都会来这里取数据：step_id: {}  集合 step.data 组合实例化Plugin
    data = models.JSONField(verbose_name="流程数据", blank=True, null=True)

    def get_next_step(self, current=None):
        """
        获取下一个步骤，当current为None的时候就是取第一个
        :param current:
        :return:
        """
        if not current:
            return self.flow.steps.first()
        else:
            # 获取当前步骤的下一个，默认order是不相等的，且都是正确排好序的
            next_step = self.flow.step_set.filter(order__gt=current.order).order_by("order").first()
            return next_step

    @staticmethod
    def get_plugin_data(step, data):
        """
        获取插件的数据
        :param step: 其实是Step的对象
        :param data: 是一个json对象
        :return:
        """
        # 2-2：取出初始化插件的数据
        # 2-2-1：先准备个dict
        plugin_data = {}

        # 2-2-2：从step配置的数据中获取
        if step.data:
            if isinstance(step.data, str):
                try:
                    step_plugin_data = json.loads(step.data)
                    plugin_data.update(step_plugin_data)
                except Exception as e:
                    msg = "步骤(id:{})配置的初始化数据有误".format(step.id)
                    return False, msg
            elif isinstance(step.data, dict):
                plugin_data.update(step.data)
        # 2-2-3：从传递的data中获取
        step_data_key = "step_{}".format(step.id)
        step_data = data.get(step_data_key)
        if step_data:
            if isinstance(step_data, str):
                try:
                    step_plugin_data = json.loads(step.data)
                    plugin_data.update(step_plugin_data)
                except Exception as e:
                    msg = "步骤(id:{})配置的初始化数据有误".format(step_data_key)
                    return False, msg
            elif isinstance(step_data, dict):
                plugin_data.update(step_data)

        # 返回插件数据
        return True, plugin_data

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
