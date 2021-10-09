# -*- coding:utf-8 -*-
"""
执行任务的插件：
这个插件的主要职责是，去执行core_task的任务
"""
from rest_framework import serializers

from workflow.models.plugin.do import DoCoreTaskPlugin


class DoCoreTaskPluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoCoreTaskPlugin
        fields = ("id", "auto_execute")


# class DoCoreTaskPlugin(Plugin):
#     """
#     执行核心任务的插件
#     """
#     PLUGIN_INFO = {
#         "code": "do_core_task_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
#         "name": "执行核心任务插件",
#         "description": "执行核心任务的插件"
#     }
#     # 执行任务可以是自动执行也可以是手动执行
#     auto_execute = models.BooleanField(verbose_name="自动执行", blank=True, default=False)
#
#     def core_task(self, workflow: WorkFlow):
#         # 获取Flow的所有步骤，由后向前执行其核心任务，每个插件有个核心任务的开关，执行完的就无需执行，未执行的就执行一下
#         print("执行workfow{}的核心任务".format(workflow))
#         return True, "执行成功"
#
#     class Meta:
#         verbose_name = "执行任务插件"
#         verbose_name_plural = verbose_name
