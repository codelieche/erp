# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.process import Process
from workflow.serializers.step import StepModelSerializer


class ProcessModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Process
        fields = ("id", "step", "workflow_id", "status", "auto_execute", "time_executed")


class ProcessInfoModelSerializer(serializers.ModelSerializer):

    step = StepModelSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Process
        fields = ("id", "step", "workflow_id", "status", "auto_execute", "time_executed")
