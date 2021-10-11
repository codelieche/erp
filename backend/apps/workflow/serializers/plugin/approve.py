# -*- coding:utf-8 -*-
"""
审批插件：核心插件之一
"""
from rest_framework import serializers

from workflow.models.plugin.approve import ApprovePlugin


class ApprovePluginModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovePlugin
        fields = ("id", "users", "user", "content", "status", "core_task_executed", "time_executed")


# class ApprovePlugin(Plugin):
#     """
#     审批插件
#     """
#     PLUGIN_INFO = {
#         "code": "approve_plugin",  # 推荐唯一处理，继承Plugin的时候，自行配置
#         "name": "审批插件",
#         "description": "审批相关的插件"
#     }
#
#     users = models.ManyToManyField(verbose_name="可审批的用户", to=User, related_name="can_approve_users", blank=True)
#     user = models.ForeignKey(verbose_name="审批用户", to=User, on_delete=models.SET_NULL,
#                              related_name="approved_user", blank=True, null=True)
#     content = models.CharField(verbose_name="审批内容", blank=True, null=True, max_length=256)
#
#     # 状态：cancel, error, success
#     def core_task(self, workfow: WorkFlow):
#         print("workflow:{}开始执行审批任务".format(workfow))
#         return True, "执行成功"
#
#     class Meta:
#         verbose_name = "审批插件"
#         verbose_name_plural = verbose_name
