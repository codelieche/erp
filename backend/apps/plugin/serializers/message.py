# -*- coding:utf-8 -*-
"""
发送消息的插件
"""
from rest_framework import serializers

from plugin.models.message import MessagePlugin


class MessagePluginPluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagePlugin
        fields = ("id", "users", "content", "status", "core_task_executed", "time_executed")


# class MessagePlugin(Plugin):
#     """
#     发送消息的插件
#     """
#     PLUGIN_INFO = {
#         "code": "message_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
#         "name": "消息插件",
#         "description": "发送消息的插件"
#     }
#
#     users = models.ManyToManyField(verbose_name="接收用户", to=User, blank=True)
#
#     def core_task(self, workfow: Work):
#         print("work:{}, 开始发送消息给{}".format(workfow, self.users))
#         return True, "执行成功"
#
#     class Meta:
#         verbose_name = "消息插件"
#         verbose_name_plural = verbose_name
