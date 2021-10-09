# -*- coding:utf-8 -*-

from rest_framework import serializers


class PluginInfoSerializer(serializers.Serializer):
    """
    插件信息Serailizer
    """
    code = serializers.CharField(help_text="插件Code")
    name = serializers.CharField(help_text="插件名称")
    description = serializers.CharField(help_text="插件描述")

