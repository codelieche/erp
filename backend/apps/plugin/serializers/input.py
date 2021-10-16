# -*- coding:utf-8 -*-
"""
输入输出插件
"""
from rest_framework import serializers

from plugin.models.input import InputOutputPlugin


class InputOutputPluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputOutputPlugin
        fields = ("id", "value", "status", "core_task_executed", "time_executed")

