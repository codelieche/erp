# -*- coding:utf-8 -*-
"""
执行Shell命令的插件
"""
from rest_framework import serializers

from workflow.models.plugin.shell import ShellExecutePlugin


class ShellExecutePluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShellExecutePlugin
        fields = ("id", "command", "status", "core_task_executed", "time_executed")


# class ShellExecutePlugin(Plugin):
#     """
#     执行Shell命令的插件
#     """
#
#     PLUGIN_INFO = {
#         "code": "shell_execute_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
#         "name": "执行Shell命令插件",
#         "description": "执行Shell命令的插件"
#     }
#
#     command = models.TextField(verbose_name="执行的shell命令")
#
#     def core_task(self, workfow: WorkFlow):
#         print("workflow:{},开始执行shell命令:{}".format(workfow, self.command))
#         return True, "执行成功"
#
#     class Meta:
#         verbose_name = "执行Shell命令插件"
#         verbose_name_plural = verbose_name
