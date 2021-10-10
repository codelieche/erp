# -*- coding:utf-8 -*-
"""
发送消息的插件
"""
from django.db import models

from account.models import User
from .base import Plugin
# from workflow.models.workflow import WorkFlow


class MessagePlugin(Plugin):
    """
    发送消息的插件
    """
    PLUGIN_INFO = {
        "code": "message_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "消息插件",
        "description": "发送消息的插件"
    }

    users = models.ManyToManyField(verbose_name="接收用户", to=User, blank=True)
    content = models.CharField(verbose_name="消息内容", max_length=512, blank=True, null=True)

    # def entry_task(self, workflow, process, step):
    #     print("进入message流程")
    #     # process.entry_next_process()

    def execute_core_task(self):
        print("执行消息插件的核心方法：", self.content)
        return True, "执行成功"

    # def core_task(self, workflow: WorkFlow, process, step):
    #     print("Workflow:{}, 开始发送消息给{}".format(workflow, self.users))
    #     return True, "执行成功"

    class Meta:
        verbose_name = "消息插件"
        verbose_name_plural = verbose_name
