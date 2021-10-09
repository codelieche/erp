# -*- coding:utf-8 -*-
"""
执行Shell命令的插件
"""
from django.db import models

from workflow.models.workflow import WorkFlow
from .base import Plugin


class ShellExecutePlugin(Plugin):
    """
    执行Shell命令的插件
    """

    PLUGIN_INFO = {
        "code": "shell_execute_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
        "name": "执行Shell命令插件",
        "description": "执行Shell命令的插件"
    }

    command = models.TextField(verbose_name="执行的shell命令")

    def entry_task(self, workflow, process, step):
        print("进入Mysql流程，我们直接进入下一步")
        process.entry_next_process()

    def core_task(self, workflow: WorkFlow, process, step):
        print("workflow:{},开始执行shell命令:{}".format(workflow, self.command))
        return True, "执行成功"

    class Meta:
        verbose_name = "执行Shell命令插件"
        verbose_name_plural = verbose_name
