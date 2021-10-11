# -*- coding:utf-8 -*-
"""
Gitlab插件
"""
from rest_framework import serializers

from workflow.models.plugin.gitflow import GitFlowPlugin


class GitflowPluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitFlowPlugin
        fields = ("id", "gitlabl", "project", "branch", "commit", "status", "core_task_executed", "time_executed")

