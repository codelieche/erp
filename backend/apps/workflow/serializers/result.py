# -*- coding:utf-8 -*-
from rest_framework import serializers

from workflow.models.result import ProcessResult


class ProcessResultModelSerializer(serializers.ModelSerializer):
    """
    过程执行的结果
    """

    class Meta:
        model = ProcessResult
        fields = (
            "id", "process_id", "success", "content", "time_added"
        )
