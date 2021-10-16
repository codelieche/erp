# -*- coding:utf-8 -*-
"""
Gitlab插件
"""
from rest_framework import serializers

from plugin.models.jenkins import JenkinsPlugin


class JenkinsPluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenkinsPlugin
        fields = ("id", "jenkins", "job", "params", "build_id", "status", "core_task_executed", "time_executed")

