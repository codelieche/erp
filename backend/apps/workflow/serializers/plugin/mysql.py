# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.plugin.mysql import MySQLPlugin


class MySQLPluginPluginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySQLPlugin
        fields = ("id", "server", "database", "sql", "status", "core_task_executed", "time_executed")
