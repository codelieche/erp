# -*- coding:utf-8 -*-
"""
执行Shell命令的插件
"""
from django.db import models

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

    # def entry_task(self, work, process, step):
    #     if process.auto_execute:
    #         print("进入shell流程，我们直接执行当前这个任务：{}".format(self.command))
    #         self.core_task(work=work, process=process, step=step)
    #     else:
    #         print("进入shell流程，我们直接进入下一步")
    #         process.entry_next_process()

    def execute_core_task(self, work=None):
        print("我现在开始执行shell的任务：{}".format(self.command))
        return True, "执行成功", None

    # def core_task(self, work: Work, process, step):
    #     print("work:{},开始执行shell命令:{}".format(work, self.command))
    #     success, result = self.execute_core_task()
    #     self.core_task_executed = True
    #
    #     if success:
    #         self.status = "success"
    #         self.save()
    #     else:
    #         self.status = "error"
    #         self.save()
    #
    #     # 执行完毕，如果process.auto_execute，那么我们要触发process的执行结果
    #     if process.auto_execute:
    #         # 里面会直接进入下一步
    #         process.handle_execute_result(success, result)
    #
    #     # 最后记得返回一下: True/False, 提示内容
    #     return success, result

    class Meta:
        verbose_name = "执行Shell命令插件"
        verbose_name_plural = verbose_name
